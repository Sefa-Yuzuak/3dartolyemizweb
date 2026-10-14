"""Mevcut logo işaretini koruyan yazılı paylaşım kartını SVG'den PNG'ye üretir.

Gereksinim: ImageMagick; mevcut Windows Segoe UI yazı tipi.
Logo yeniden çizilmez: assets/img/logo.jpg olduğu gibi yerleşime gömülür.
"""
import base64
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
logo = base64.b64encode((ROOT / 'assets/img/logo.jpg').read_bytes()).decode('ascii')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="white"/>
<image x="65" y="150" width="330" height="330" xlink:href="data:image/jpeg;base64,{logo}"/>
<text x="430" y="320" font-family="Segoe UI" font-weight="700" font-size="72" fill="#342357">3D ARTÖLYEMİZ</text>
<text x="434" y="382" font-family="Segoe UI" font-size="36" fill="#52626e">artolyemiz.com</text>
</svg>'''
output = ROOT / 'assets/img/artolyemiz-paylasim-logo-v1.png'
subprocess.run(['magick', 'svg:-', '-strip', str(output)], input=svg.encode('utf-8'), check=True)
print(output.name)
