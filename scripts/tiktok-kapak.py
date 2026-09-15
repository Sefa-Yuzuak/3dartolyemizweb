"""TikTok kapak gorseli: oEmbed'den kucuk resmi indirip yerel WebP olarak kaydeder.

Kullanim:  python scripts/tiktok-kapak.py <video adresi> [<video adresi> ...]
Ornek:     python scripts/tiktok-kapak.py https://www.tiktok.com/@3dartolyemiz/video/7511359621169302802

Neden var: TikTok gomusu sayfaya otomatik yuklendiginde ana sayfa 207 istek / 28 MB
oluyordu (PSI 13.09.2026). Sayfada artik yalnizca hafif bir kart duruyor; iframe
dugmeye basilinca geliyor. Kartin kapagi bu betikle DERLEME zamaninda indirilir,
ziyaretci TikTok CDN'ine hic gitmez. Cikti: assets/img/tiktok-<video id>.webp (520 px genislik).
Betik ayrica oEmbed basligini yazar; karttaki metin oradan alinir, uydurulmaz.
Profil (creator) gomusu icin oEmbed kucuk resim vermiyor; o kartta markanin
kendi isareti (assets/img/logo-mark.webp) kullaniliyor.
"""
from __future__ import annotations

import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

KOK = Path(__file__).resolve().parent.parent
GENISLIK = 520
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def indir(url: str) -> bytes:
    istek = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(istek, timeout=30) as y:
        return y.read()


def kapak_al(video_url: str) -> None:
    m = re.search(r"/video/(\d+)", video_url)
    if not m:
        print(f"  atlandi (video kimligi yok): {video_url}")
        return
    kimlik = m.group(1)
    oembed = "https://www.tiktok.com/oembed?url=" + urllib.parse.quote(video_url, safe="")
    veri = json.loads(indir(oembed).decode("utf-8"))
    ham = indir(veri["thumbnail_url"])
    im = Image.open(io.BytesIO(ham)).convert("RGB")
    w, h = im.size
    im = im.resize((GENISLIK, round(h * GENISLIK / w)), Image.LANCZOS)
    hedef = KOK / "assets" / "img" / f"tiktok-{kimlik}.webp"
    im.save(hedef, "WEBP", quality=72, method=6)
    print(f"  yazildi: {hedef.relative_to(KOK).as_posix()}  {im.size[0]}x{im.size[1]}  {hedef.stat().st_size} bayt")
    print(f"  baslik : {veri.get('title', '')[:120]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for u in sys.argv[1:]:
        kapak_al(u)
