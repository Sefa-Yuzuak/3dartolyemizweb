"""Statik iletişim bağlantıları: JavaScript olmadan da sayfa bağlamı korunur."""
import html
import re
from urllib.parse import parse_qs, quote, urlsplit

INSTAGRAM = "https://www.instagram.com/3dartolyemiz/"
WHATSAPP = "https://wa.me/905441885744"


def wa_link(konu: str, url: str) -> str:
    return WHATSAPP + "?text=" + quote(f"Merhaba, {konu} hakkında bilgi almak istiyorum.\n{url}", safe="")


def instagram_dugmesi() -> str:
    return (f'<a class="btn btn-secondary" href="{INSTAGRAM}" target="_blank" '
            'rel="noopener">Instagram’da işlerimizi gör</a>')


def baglantilari_hazirla(metin: str, url: str, konu: str) -> str:
    """Genel bağlantıya sayfa konusu, özel talebe ilgili URL ekler; tekrar çalışabilir."""
    def degistir(m):
        etiket = m.group(0)
        href = re.search(r'\bhref="([^"]+)"', etiket)
        if not href:
            return etiket
        hedef = html.unescape(href.group(1))
        ayrik = urlsplit(hedef)
        if ayrik.netloc != "wa.me":
            return etiket
        if ayrik.path != "/905441885744":
            raise ValueError("Beklenmeyen WhatsApp alıcısı")
        mesaj = parse_qs(ayrik.query).get("text", [""])[0]
        genel = ('data-contact="page"' in etiket or not mesaj
                 or "siteniz üzerinden ulaşıyorum" in mesaj)
        if genel:
            hedef = wa_link(konu, url)
            if 'data-contact="page"' not in etiket:
                etiket = etiket.replace("<a ", '<a data-contact="page" ', 1)
        else:
            # Ürün kartının kendi ürün URL'si varsa ana sayfa URL'siyle değiştirme.
            if not re.search(r'https://artolyemiz\.com(?:/|\b)', mesaj):
                mesaj += "\n" + url
            hedef = WHATSAPP + "?text=" + quote(mesaj, safe="")
        return re.sub(r'\bhref="[^"]+"', lambda _: f'href="{html.escape(hedef, quote=True)}"', etiket, count=1)
    return re.sub(r'<a\b[^>]*>', degistir, metin)
