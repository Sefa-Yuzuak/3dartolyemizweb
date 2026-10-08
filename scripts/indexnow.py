"""Degisen sayfalari IndexNow ile bildirir (Bing ve IndexNow kullanan diger
arama motorlari). ChatGPT'nin web aramasi buyuk olcude Bing dizinine dayaniyor;
Bing 08.10.2026'da bu siteyi neredeyse hic taramamisti (tarama ve sorgu verisi
bostu).

Anahtar herkese acik bir dogrulama degeridir, gizli DEGILDIR: kokteki
<anahtar>.txt dosyasi sitenin bu anahtarin sahibi oldugunu kanitlar.

Kullanim:
  python scripts/indexnow.py                 # sitemap'teki tum adresler
  python scripts/indexnow.py index.html urun/x/index.html ...   # yalniz degisenler
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ALAN = "artolyemiz.com"
ANAHTAR = next(p.stem for p in KOK.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem))


def adresler(dosyalar: list[str]) -> list[str]:
    if not dosyalar:
        sm = (KOK / "sitemap.xml").read_text(encoding="utf-8")
        return re.findall(r"<loc>([^<]+)</loc>", sm)
    cikti = []
    for d in dosyalar:
        d = d.replace("\\", "/")
        if d == "index.html":
            cikti.append(f"https://{ALAN}/")
        elif d.endswith("/index.html") and not d.startswith((".", "scripts/", "assets/")):
            cikti.append(f"https://{ALAN}/{d[:-len('index.html')]}")
        elif d == "llms.txt":
            cikti.append(f"https://{ALAN}/llms.txt")
    return sorted(set(cikti))


def main() -> int:
    urls = adresler(sys.argv[1:])
    if not urls:
        print("IndexNow: bildirilecek sayfa degisikligi yok.")
        return 0
    govde = {"host": ALAN, "key": ANAHTAR,
             "keyLocation": f"https://{ALAN}/{ANAHTAR}.txt", "urlList": urls}
    req = urllib.request.Request("https://api.indexnow.org/indexnow",
                                 data=json.dumps(govde).encode(), method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            kod = r.status
    except urllib.error.HTTPError as e:
        kod = e.code
    # 200 kabul, 202 kabul (anahtar dogrulamasi suruyor); digerleri hata.
    print(f"IndexNow: {len(urls)} adres, HTTP {kod}")
    return 0 if kod in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main())
