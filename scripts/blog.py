"""Blog yazilari ve atolye sayfasi.

Yazilar content/blog/<slug>.html (yalniz govde), ust bilgileri content/blog.json'da.
Atolyenin fotograf ve videolari content/atolye.json'da; dosyalar
assets/img/atolye/ ve assets/video/ altinda (@3dartolyemiz'in kendi reels
videolarindan kesildi, kliplerde ses yok).

Yazi govdesinde fiyat ve sure ELLE yazilmaz; belirtecle cagrilir ki urun
verisi degisince blog eskimesin:
    {{aralik:<etiket>}}   etiketin yaklasik fiyat araligi (content/urunler.json'dan)
    {{sure}}              teslim suresi cumlesi (sayfa-uret.py SURE)
    {{urun:<slug>}}       urun sayfasina baglanti + yaklasik fiyat
    {{urungorsel:<slug>}} urun gorseli, altyazisi urun sayfasina bagli
    {{foto:<dosya>}}      atolye fotografi (content/atolye.json)
    {{video:<dosya>}}     atolye klibi (content/atolye.json)
Tanimsiz belirtec ya da olmayan dosya derlemeyi durdurur.
"""
from __future__ import annotations

import io
import json
import re
from pathlib import Path

from PIL import Image

KOK = Path(__file__).resolve().parent.parent
YAZILAR = json.load(io.open(KOK / "content" / "blog.json", encoding="utf-8"))
ATOLYE = json.load(io.open(KOK / "content" / "atolye.json", encoding="utf-8"))
FOTO = {f["dosya"]: f for f in ATOLYE["fotograflar"]}
VIDEO = {v["dosya"]: v for v in ATOLYE["videolar"]}
YAZAR = {"@type": "Organization", "name": "3dartolyemiz", "url": "https://artolyemiz.com/"}
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos",
         "Eylül", "Ekim", "Kasım", "Aralık"]


def boyut(yol: str) -> tuple[int, int]:
    dosya = KOK / yol.lstrip("/")
    if not dosya.exists():
        raise SystemExit(f"Dosya yok: {yol}")
    with Image.open(dosya) as im:
        return im.size


def tarih_metni(iso: str) -> str:
    y, a, g = map(int, iso.split("-"))
    return f"{g} {AYLAR[a - 1]} {y}"


def video_sure(dosya: str) -> int:
    """mp4'un suresi (sn): 'mvhd' kutusundan, ek arac gerektirmeden."""
    veri = (KOK / "assets" / "video" / f"{dosya}.mp4").read_bytes()
    i = veri.index(b"mvhd") + 4
    surum = veri[i]
    if surum == 1:
        olcek = int.from_bytes(veri[i + 20:i + 24], "big")
        sure = int.from_bytes(veri[i + 24:i + 32], "big")
    else:
        olcek = int.from_bytes(veri[i + 12:i + 16], "big")
        sure = int.from_bytes(veri[i + 16:i + 20], "big")
    return max(1, round(sure / olcek))


def foto_html(dosya: str) -> str:
    f = FOTO[dosya]
    yol = f"/assets/img/atolye/{dosya}-sm.webp"
    w, h = boyut(yol)
    return (f'<figure class="yazi-gorsel"><img src="{yol}" alt="{f["alt"]}" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async"><figcaption>{f["baslik"]}</figcaption></figure>')


def video_html(dosya: str) -> str:
    v = VIDEO[dosya]
    poster = f"/assets/img/atolye/klip-{dosya}.webp"
    w, h = boyut(poster)
    if not (KOK / "assets" / "video" / f"{dosya}.mp4").exists():
        raise SystemExit(f"Video yok: {dosya}.mp4")
    # Sessiz, dongulu; main.js gorunur oldugunda oynatir. preload=none: sayfa
    # acilirken video indirilmez.
    return (f'<figure class="yazi-video"><video class="klip" width="{w}" height="{h}" poster="{poster}" '
            f'muted loop playsinline preload="none" aria-label="{v["ad"]}">'
            f'<source src="/assets/video/{dosya}.mp4" type="video/mp4"></video>'
            f'<figcaption>{v["aciklama"]}</figcaption></figure>')


def video_sema(dosya: str, alan: str) -> dict:
    v = VIDEO[dosya]
    return {"@context": "https://schema.org", "@type": "VideoObject", "name": v["ad"],
            "description": v["aciklama"], "uploadDate": v["tarih"],
            "thumbnailUrl": f"{alan}/assets/img/atolye/klip-{dosya}.webp",
            "contentUrl": f"{alan}/assets/video/{dosya}.mp4",
            "duration": f"PT{video_sure(dosya)}S"}


def belirtec_coz(metin: str, k: dict) -> str:
    def coz(m):
        tur, _, arg = m.group(1).partition(":")
        if tur == "aralik":
            return k["aralik"](arg)
        if tur == "sure":
            return k["SURE"]
        if tur == "urun":
            u = k["URUN"][arg]
            return f'<a href="/urun/{arg}/">{u["ad"]}</a>: {u["fiyat_metni"].replace("Yaklaşık", "yaklaşık", 1)}'
        if tur == "urungorsel":
            u = k["URUN"][arg]
            return (f'<figure class="yazi-gorsel"><img src="{u["kart_gorsel"]}" alt="{u["alt"]}" '
                    f'width="450" height="600" loading="lazy" decoding="async">'
                    f'<figcaption><a href="/urun/{arg}/">{u["ad"]}</a></figcaption></figure>')
        if tur == "foto":
            return foto_html(arg)
        if tur == "video":
            return video_html(arg)
        raise SystemExit(f"Tanimsiz belirtec: {m.group(0)}")
    return re.sub(r"\{\{([^}]+)\}\}", coz, metin)


def videolar(govde: str) -> list:
    return re.findall(r"\{\{video:([^}]+)\}\}", govde)


def kirinti(*adimlar) -> str:
    parca = ['<a href="/">Ana sayfa</a>']
    for ad, yol in adimlar[:-1]:
        parca.append(f'<a href="{yol}">{ad}</a>')
    parca.append(f"<span>{adimlar[-1][0]}</span>")
    return '<nav class="kirinti" aria-label="Konum">' + " <span>/</span> ".join(parca) + "</nav>"


def kirinti_sema(alan: str, *adimlar) -> dict:
    ogeler = [("Ana sayfa", "/")] + list(adimlar)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": ad, "item": alan + yol}
        for i, (ad, yol) in enumerate(ogeler, 1)]}


def sss_html(sss: list) -> str:
    return "\n".join(f'        <details class="faq-item"><summary>{q}</summary><p>{c}</p></details>'
                     for q, c in sss)


def sss_sema(sss: list) -> dict:
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": c}}
        for q, c in sss]}


def yazi_karti(y: dict) -> str:
    w, h = boyut(y["kart"])
    return (f'        <article class="blog-kart reveal">\n'
            f'          <a class="blog-kart-gorsel" href="/blog/{y["slug"]}/" tabindex="-1" aria-hidden="true">'
            f'<img src="{y["kart"]}" alt="{y["h1"]}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>\n'
            f'          <div class="blog-kart-govde">\n'
            f'            <time datetime="{y["tarih"]}">{tarih_metni(y["tarih"])}</time>\n'
            f'            <h3><a href="/blog/{y["slug"]}/">{y["h1"]}</a></h3>\n'
            f'            <p>{y["aciklama"]}</p>\n'
            f'          </div>\n        </article>')


def hazirla(k: dict) -> None:
    """Yazi govdelerini okur, belirtecleri cozer, okuma suresini hesaplar."""
    for y in YAZILAR:
        ham = io.open(KOK / "content" / "blog" / f"{y['slug']}.html", encoding="utf-8").read()
        y["videolar"] = videolar(ham)
        y["govde"] = belirtec_coz(ham, k)
        kelime = len(re.sub(r"<[^>]+>", " ", y["govde"]).split())
        y["kelime"] = kelime
        y["dakika"] = max(1, round(kelime / 200))
        y["kart"] = y["gorsel"].replace(".webp", "-sm.webp")
        if not (KOK / y["kart"].lstrip("/")).exists():
            y["kart"] = y["gorsel"]


def yazi_sayfasi(y: dict, k: dict) -> str:
    alan = k["ALAN"]
    url = f"{alan}/blog/{y['slug']}/"
    gw, gh = boyut(y["gorsel"])
    bloklar = [
        kirinti_sema(alan, ("Blog", "/blog/"), (y["h1"], f"/blog/{y['slug']}/")),
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": y["h1"],
         "description": y["aciklama"], "url": url, "mainEntityOfPage": url,
         "image": {"@type": "ImageObject", "url": alan + y["gorsel"], "width": gw, "height": gh},
         "datePublished": y["tarih"], "dateModified": y.get("guncelleme", y["tarih"]),
         "inLanguage": "tr-TR", "wordCount": y["kelime"], "author": YAZAR,
         "publisher": dict(YAZAR, logo={"@type": "ImageObject",
                                         "url": alan + "/assets/img/icon-192.png"})},
        sss_sema(y["sss"]),
    ] + [video_sema(v, alan) for v in y["videolar"]]
    h = k["head_yap"](y["baslik"], y["aciklama"], url, bloklar, og_baslik=y["h1"],
                      og_gorsel=y["gorsel"], og_tur="article")
    digerleri = [x for x in YAZILAR if x["slug"] != y["slug"]][:4]
    govde = f'''<main id="main">
  <article class="yazi">
    <section class="hero hero--sayfa">
      <div class="container">
        {kirinti(("Blog", "/blog/"), (y["h1"], ""))}
        <h1>{y["h1"]}</h1>
        <p class="yazi-ust"><time datetime="{y["tarih"]}">{tarih_metni(y["tarih"])}</time> · {y["dakika"]} dakikalık okuma · 3dartolyemiz atölyesi</p>
      </div>
    </section>
    <section>
      <div class="container yazi-govde">
        <img class="yazi-kapak" src="{y["gorsel"]}" alt="{y["h1"]}" width="{gw}" height="{gh}" loading="eager" decoding="async">
{y["govde"]}
        <aside class="yazi-cta">
          <p><strong>Aklınızdaki işi konuşalım.</strong> Fotoğrafı, dosyayı ya da fikri WhatsApp'tan gönderin; yaklaşık fiyatı ve süreyi hemen söyleyelim.</p>
          <a class="btn btn-primary" href="{k["TEL"]}" target="_blank" rel="noopener">WhatsApp'tan yaz</a>
        </aside>
      </div>
    </section>
  </article>

  <section class="section--alt">
    <div class="container">
      <div class="section-head reveal"><span class="eyebrow">Merak Edilenler</span><h2>Sıkça sorulan sorular</h2></div>
      <div class="faq reveal">
{sss_html(y["sss"])}
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head reveal"><h2>Diğer yazılar</h2></div>
      <div class="blog-grid">
{chr(10).join(yazi_karti(x) for x in digerleri)}
      </div>
      <p class="katalog-tumu"><a class="btn btn-secondary" href="/blog/">Tüm yazılar</a></p>
    </div>
  </section>
'''
    return h + k["bas"] + govde + k["son"]


def blog_dizini(k: dict) -> str:
    alan = k["ALAN"]
    url = f"{alan}/blog/"
    bloklar = [
        kirinti_sema(alan, ("Blog", "/blog/")),
        {"@context": "https://schema.org", "@type": "Blog", "name": "3dartolyemiz blog", "url": url,
         "inLanguage": "tr-TR", "publisher": YAZAR,
         "blogPost": [{"@type": "BlogPosting", "headline": y["h1"], "url": f"{alan}/blog/{y['slug']}/",
                       "datePublished": y["tarih"]} for y in YAZILAR]},
    ]
    h = k["head_yap"]("3D Baskı Blogu: Rehberler ve Atölyeden Notlar | 3dartolyemiz",
                      "3D baskı nedir, fiyatlar neye göre değişir, hangi malzeme seçilir, figür nasıl "
                      "boyanır: Ankara'daki atölyemizden sade ve uygulamalı rehberler.",
                      url, bloklar, og_baslik="3dartolyemiz blog")
    govde = f'''<main id="main">
  <section class="hero hero--sayfa">
    <div class="container">
      {kirinti(("Blog", ""))}
      <h1>3D baskı rehberleri ve atölyeden notlar</h1>
      <p class="lead">Her gün yazıcı başında öğrendiklerimizi sade bir dille yazıyoruz: 3D baskının
        nasıl çalıştığı, fiyatların neye göre değiştiği, malzeme seçimi, sık yapılan hatalar ve
        kişiye özel figür ile maket siparişinde bilmeniz gerekenler.</p>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="blog-grid">
{chr(10).join(yazi_karti(y) for y in YAZILAR)}
      </div>
    </div>
  </section>

  <section class="section--alt">
    <div class="container">
      <div class="section-head reveal"><h2>Üretimi kendi gözünüzle görün</h2></div>
      <p class="sayfa-metin reveal">Yazıcılarımızı, baskı tablalarını ve üretimden kısa videoları
        <a href="/atolyemiz/">atölyemiz sayfasında</a> topladık. Ürünler ve yaklaşık fiyatları için
        <a href="/urun/">ürün kataloğu</a>.</p>
    </div>
  </section>
'''
    return h + k["bas"] + govde + k["son"]


def atolye_sayfasi(k: dict) -> str:
    alan = k["ALAN"]
    url = f"{alan}/atolyemiz/"
    vs = [v["dosya"] for v in ATOLYE["videolar"]]
    bloklar = [
        kirinti_sema(alan, ("Atölyemiz", "/atolyemiz/")),
        {"@context": "https://schema.org", "@type": "AboutPage", "name": "3dartolyemiz atölyesi",
         "url": url, "about": {"@type": "LocalBusiness", "name": "3dartolyemiz", "url": alan + "/"},
         "primaryImageOfPage": alan + "/assets/img/atolye/bambu-lab-yazici-ams.webp"},
    ] + [video_sema(v, alan) for v in vs]
    h = k["head_yap"]("Atölyemiz: 3D Yazıcılarımız ve Üretimden Videolar | 3dartolyemiz",
                      "Ankara Yenimahalle'deki atölyemizden kareler: 3D yazıcılarımız, toplu baskı "
                      "tablaları, modelleme ve üretimden kısa videolar.",
                      url, bloklar, og_baslik="3dartolyemiz atölyesi",
                      og_gorsel="/assets/img/atolye/bambu-lab-yazici-ams.webp")
    fotolar = "\n".join(f"        {foto_html(f['dosya'])}" for f in ATOLYE["fotograflar"]
                        if f.get("sayfada", True))
    klipler = "\n".join(f"        {video_html(v)}" for v in vs)
    govde = f'''<main id="main">
  <section class="hero hero--sayfa">
    <div class="container">
      {kirinti(("Atölyemiz", ""))}
      <h1>Atölyemiz: yazıcılarımız ve üretimden kareler</h1>
      <p class="lead">Sitede gördüğünüz her ürün Ankara Yenimahalle'deki atölyemizde modelleniyor,
        basılıyor ve elle boyanıyor. Bu sayfada o üretimin kendisini gösteriyoruz: makinelerimizi,
        baskı tablalarını ve Instagram'da paylaştığımız videolardan kısa kesitleri.</p>
      <div class="hero-ctas"><a class="btn btn-primary" href="{k["TEL"]}" target="_blank" rel="noopener">WhatsApp'tan yaz</a></div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head reveal"><h2>Hangi makinelerle çalışıyoruz?</h2></div>
      <p class="sayfa-metin reveal">Filamentli baskıyı Bambu Lab ve Creality yazıcılarda
        yapıyoruz. Bambu Lab yazıcılara takılı çok renkli besleme üniteleri (AMS) sayesinde
        logolu anahtarlık, yazılı tabela gibi işleri boyamaya gerek kalmadan birden fazla renkle
        basabiliyoruz. Yüz hatları, parmak, saç teli gibi çok ince detay isteyen küçük figürlerde
        reçine (SLA) baskı kullanıyoruz.</p>
      <p class="sayfa-metin reveal">Kapalı kasalı yazıcılar içerideki sıcaklığı sabit tuttuğu
        için uzun baskılarda çarpılmayı azaltıyor. Tek bir tabla bazen 30 saati aşkın sürüyor; makineler bu
        sırada gece gündüz çalışıyor. Malzeme seçiminin ayrıntıları
        <a href="/blog/pla-petg-tpu-recine-farki/">PLA, PETG, TPU ve reçine karşılaştırmasında</a>.</p>
      <div class="atolye-grid">
{fotolar}
      </div>
    </div>
  </section>

  <section class="section--alt">
    <div class="container">
      <div class="section-head reveal"><span class="eyebrow">Üretimden</span><h2>Kısa videolar</h2></div>
      <p class="sayfa-metin reveal">Instagram'da paylaştığımız videolardan kesitler: toplu baskı
        tablaları, katman katman baskı anı ve montaj. Daha fazlası
        <a href="https://www.instagram.com/3dartolyemiz/" target="_blank" rel="noopener">@3dartolyemiz</a> hesabında.</p>
      <div class="atolye-grid atolye-grid--video">
{klipler}
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head reveal"><h2>Bir sipariş atölyede nasıl ilerliyor?</h2></div>
      <ul class="sayfa-liste reveal">
{chr(10).join(f"        <li>{x}</li>" for x in k["SUREC"])}
      </ul>
      <p class="sayfa-metin reveal">{k["SURE"]}</p>
      <p class="sayfa-metin reveal">Atölyede eğitim de veriyoruz: <a href="/3d-yazici-egitimi/">3D yazıcı
        eğitimi</a> (online ya da yüz yüze) ve Ankara içinde <a href="/3d-yazici-tamiri-ankara/">3D yazıcı
        tamiri</a>. 3D baskının nasıl çalıştığını merak ediyorsanız <a href="/blog/">blogumuzda</a>
        rehberler var.</p>
    </div>
  </section>
'''
    return h + k["bas"] + govde + k["son"]


def rss(k: dict) -> str:
    """/blog/rss.xml: yeni yazilarin arama motorlarina ve okuyuculara duyurusu."""
    from email.utils import format_datetime
    from datetime import datetime, timezone
    from xml.sax.saxutils import escape
    alan = k["ALAN"]

    def zaman(iso):
        y, a, g = map(int, iso.split("-"))
        return format_datetime(datetime(y, a, g, 9, 0, tzinfo=timezone.utc))
    ogeler = "".join(
        f"  <item>\n    <title>{escape(y['h1'])}</title>\n    <link>{alan}/blog/{y['slug']}/</link>\n"
        f"    <guid>{alan}/blog/{y['slug']}/</guid>\n    <pubDate>{zaman(y['tarih'])}</pubDate>\n"
        f"    <description>{escape(y['aciklama'])}</description>\n  </item>\n" for y in YAZILAR)
    son = max(y.get("guncelleme", y["tarih"]) for y in YAZILAR)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
            f"  <title>3dartolyemiz blog</title>\n  <link>{alan}/blog/</link>\n"
            "  <description>Ankara'daki 3D baskı atölyemizden rehberler ve notlar.</description>\n"
            f"  <language>tr</language>\n  <lastBuildDate>{zaman(son)}</lastBuildDate>\n"
            + ogeler + "</channel>\n</rss>\n")
