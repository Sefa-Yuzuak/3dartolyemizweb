# -*- coding: utf-8 -*-
"""Galeri ızgarasını assets/js/gallery.js içindeki GALLERY dizisinden index.html'e
basar: python scripts/galeri-html.py

Neden: 41 atölye fotoğrafı yalnız JS dizisindeydi, HTML'de hiç <img> yoktu; JS
çalıştırmayan arama ve üretken motorlar görselleri ve başlıklarını görmüyordu.
Veri tek yerde (gallery.js) kalsın diye izgara buradan türetiliyor.
"""
import pathlib
import re

KOK = pathlib.Path(__file__).resolve().parent.parent


def kacir(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


js = (KOK / "assets/js/gallery.js").read_text("utf-8")
kayitlar = [m.groupdict() for m in re.finditer(
    r"\{ src:'(?P<src>[^']+)', w:(?P<w>\d+), h:(?P<h>\d+), title:'(?P<title>[^']*)', "
    r"alt:'(?P<alt>[^']*)', tag:'(?P<tag>[^']*)' \}", js)]
assert len(kayitlar) == js.count("{ src:"), "GALLERY ayrıştırması eksik"

parcalar = []
for i, k in enumerate(kayitlar):
    kucuk = k["src"].replace(".webp", "-sm.webp")
    parcalar.append(
        f'        <div class="gallery-item reveal">\n'
        f'          <div class="thumb">\n'
        f'            <button type="button" data-index="{i}" aria-label="{kacir(k["title"])} - büyüt">\n'
        f'              <img src="/{kucuk}" data-full="/{k["src"]}" alt="{kacir(k["alt"])}" '
        f'width="{k["w"]}" height="{k["h"]}" loading="lazy" decoding="async">\n'
        f'            </button>\n'
        f'            <span class="tag">{kacir(k["tag"])}</span>\n'
        f'          </div>\n'
        f'          <p class="gallery-item-title">{kacir(k["title"])}</p>\n'
        f'        </div>')

p = KOK / "index.html"
s = p.read_text("utf-8")
yeni = ('<div class="gallery-grid" id="gallery-grid">\n'
        '        <!-- 41 kart HTML\'e basılı: JS çalışmadan da okunur. Kaynak veri\n'
        '             assets/js/gallery.js; bu blok scripts/galeri-html.py ile üretilir. -->\n'
        + "\n".join(parcalar) + '\n      </div>')
s = re.sub(r'<div class="gallery-grid" id="gallery-grid">.*?</div>\n      </div>',
           yeni, s, count=1, flags=re.S)
p.write_text(s, "utf-8")
print(f"index.html: {len(kayitlar)} galeri kartı basıldı")
