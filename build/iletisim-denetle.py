"""Sitemap kapsamındaki gerçek çıktıların iletişim ve medya sözleşmesini denetler."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://artolyemiz.com"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, name, attrs):
        self.tags.append((name, dict(attrs)))


def main():
    urls = [x.text for x in ET.parse(ROOT / "sitemap.xml").iter() if x.tag.endswith("}loc")]
    errors = []
    counts = Counter()
    for url in urls:
        path = ROOT / urlsplit(url).path.lstrip("/") / "index.html"
        text = path.read_text(encoding="utf-8")
        page = Page()
        page.feed(text)
        docks = [a for t, a in page.tags if t == "nav" and a.get("class") == "contact-dock"]
        if len(docks) != 1:
            errors.append((url, "tam bir iletişim alanı bulunmalı"))
        page_links = 0
        ig_buttons = 0
        for tag, a in page.tags:
            if tag != "a":
                continue
            href = a.get("href", "")
            dest = urlsplit(href)
            if dest.netloc == "wa.me":
                counts["whatsapp"] += 1
                params = parse_qs(dest.query)
                message = params.get("text", [""])[0]
                if dest.path != "/905441885744" or len(params.get("text", [])) != 1:
                    errors.append((url, "WhatsApp alıcısı veya sorgusu hatalı"))
                links = re.findall(r'https://artolyemiz\.com/\S*', message)
                if len(links) != 1 or links[0] not in urls:
                    errors.append((url, "mesajda tek ve geçerli bir site sayfası olmalı"))
                if a.get("data-contact") == "page":
                    page_links += 1
                    if links != [url]:
                        errors.append((url, "ortak iletişim bağlantısı yanlış sayfayı taşıyor"))
                if "%20" in message or "siteniz üzerinden ulaşıyorum" in message:
                    errors.append((url, "genel veya çift kodlanmış mesaj"))
            if dest.netloc in ("instagram.com", "www.instagram.com"):
                counts["instagram"] += 1
                if href != "https://www.instagram.com/3dartolyemiz/":
                    errors.append((url, "doğrulanmamış Instagram hedefi"))
                if "btn" in a.get("class", "").split():
                    ig_buttons += 1
        if not page_links:
            errors.append((url, "sayfa bağlamlı WhatsApp bağlantısı eksik"))
        if ("/urun/" in url and url != BASE + "/urun/") or urlsplit(url).path in {
            "/ankara-3d-baski/", "/kisiye-ozel-3d-figur/", "/3d-baski-maket/",
            "/3d-modelleme/", "/dogum-gunu-boyama-atolyesi/", "/stl-dosyasi-bastirma/",
            "/3d-yazici-egitimi/", "/3d-yazici-tamiri-ankara/", "/atolyemiz/"}:
            if not ig_buttons:
                errors.append((url, "içerikte Instagram düğmesi yok"))
        for tag, a in page.tags:
            if tag not in ("img", "source", "script", "link"):
                continue
            attr = "href" if tag == "link" else "src"
            src = a.get(attr)
            if not src:
                continue
            resolved = urlsplit(urljoin(url, src))
            if resolved.netloc != "artolyemiz.com" or tag == "link" and a.get("rel") == "canonical":
                continue
            target = ROOT / resolved.path.lstrip("/")
            if not target.exists():
                errors.append((url, "eksik yerel kaynak: " + resolved.path))
        meta = {a.get("property", a.get("name")): a.get("content") for t, a in page.tags if t == "meta"}
        if meta.get("og:image") != meta.get("twitter:image"):
            errors.append((url, "sosyal paylaşım görselleri farklı"))
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            data = json.loads(block)
            if data.get("@type") == "Product":
                counts["products"] += 1
                if "offers" in data:
                    errors.append((url, "özel üretim bütçesi gerçek satış teklifi gibi işaretlenmiş"))
                img = next((a for t, a in page.tags if t == "img" and a.get("class") == "urun-gorsel"), {})
                if not img.get("srcset") or img.get("loading") != "eager":
                    errors.append((url, "ana ürün görseli mobil boyutlandırması eksik"))
        if 'class="fab"' in text or "C:/Users/" in text or "mesajlar.jsonl" in text:
            errors.append((url, "eski iletişim alanı veya özel kaynak bilgisi yayın çıktısına sızmış"))
        counts["pages"] += 1
    print(json.dumps(dict(counts), ensure_ascii=False))
    for url, error in errors:
        print(url, error)
    print(f"Hata: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
