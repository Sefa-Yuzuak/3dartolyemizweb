"""Reviewed archive selection; full-frame responsive images and descriptive captions."""
import json
from html import escape
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/gorsel-secimleri.json').read_text('utf-8'))

def serit(keys, title):
    if not keys:
        return ''
    cards = []
    for key in keys:
        p = DATA['fotograflar'][key]
        src = p['src']; small = src.replace('.webp', '-sm.webp')
        for path in (src, small):
            if not (ROOT / path.lstrip('/')).is_file():
                raise ValueError('Missing selected photo: ' + path)
        with Image.open(ROOT / small.lstrip('/')) as thumbnail:
            small_width = thumbnail.width
        cards.append(f'<figure><a href="{src}" target="_blank" rel="noopener" aria-label="{escape(p["alt"])} — büyük fotoğrafı aç">'
                     f'<img src="{small}" srcset="{small} {small_width}w, {src} {p["width"]}w" '
                     f'sizes="(min-width:760px) 350px, 85vw" width="{p["width"]}" height="{p["height"]}" '
                     f'alt="{escape(p["alt"])}" loading="lazy" decoding="async"></a>'
                     f'<figcaption>{escape(p["alt"])}</figcaption></figure>')
    return f'<div class="foto-secimi"><h2>{escape(title)}</h2><div class="foto-serit">'+''.join(cards)+'</div></div>'

def hizmet(slug):
    return serit(DATA['hizmetler'].get(slug), 'Atölyemizden kareler')

def urun(slug):
    title = ('Farklı köpek figürü çalışmalarımız' if slug == 'kisiye-ozel-kopek-figuru'
             else 'Kutu içeriğinden bir örnek' if slug == 'artopop-kendin-boya-kutusu'
             else 'Bu çalışmaya yakından bakın')
    content = serit(DATA['urunler'].get(slug), title)
    return '<section><div class="container">'+content+'</div></section>' if content else ''
