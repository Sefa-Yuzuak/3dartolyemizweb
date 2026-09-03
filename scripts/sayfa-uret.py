"""Alt sayfa ureteci.

index.html tek sayfa olarak kalir ve kabuk (head, header, footer) icin
tek dogru kaynak odur. Bu betik o kabugu index.html'den okur, icerigi
degistirip alt sayfalari yazar. Boylece menu ya da footer degistiginde
tek yerde degistirmek yeterli olur: index.html, sonra bu betigi calistir.

Kullanim:  python scripts/sayfa-uret.py

Kural: uydurma bilgi yok. Buradaki her olgu (fiyat, sure, yas araligi,
malzeme, kutu icerigi) ya index.html'de ya da Instagram aciklamalarinda
zaten yaziyor.
"""
from __future__ import annotations

import io
import json
import re
import unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ALAN = "https://artolyemiz.com"
TEL = "https://wa.me/905441885744?text=Merhaba%2C%20siteniz%20%C3%BCzerinden%20ula%C5%9F%C4%B1yorum"

# --------------------------------------------------------------------- icerik

SAYFALAR = [
    {
        "slug": "ankara-3d-baski",
        "title": "Ankara 3D Baskı | Reçine, PLA, PETG, TPU | 3dartolyemiz",
        "desc": "Ankara'da 3D baskı hizmeti. SLA reçine, PLA, PETG ve TPU baskı, "
                "3D modelleme. Ankara içi elden teslim, Türkiye geneli kargo.",
        "h1": "Ankara'da 3D baskı hizmeti",
        "lead": "Ankara'daki atölyemizde kişiye özel figür, hediyelik, ev dekoru ve maket üretiyoruz. "
                "Elinde hazır model varsa basıyoruz, yoksa modeli sıfırdan tasarlıyoruz.",
        "sema": "Service",
        "sema_ad": "3D baskı hizmeti",
        "bolumler": [
            {"h2": "Hangi malzemeyle basıyoruz?",
             "p": ["Malzemeyi işin gereğine göre seçiyoruz. Aynı ürünü her malzemeden basmak mümkün ama "
                   "sonuç aynı olmuyor, o yüzden baştan konuşuyoruz."],
             "kartlar": [
                 ("SLA, yani reçine",
                  "İnce detay isteyen figür ve büstlerde kullanıyoruz. Katman izi neredeyse görünmüyor, "
                  "yüz hatları ve küçük parçalar net çıkıyor."),
                 ("PLA",
                  "Dekor, hediyelik ve maketlerin çoğunda tercih ettiğimiz malzeme. Boyayı iyi tutuyor, "
                  "renk seçeneği geniş."),
                 ("PETG",
                  "Dayanım isteyen parçalarda kullanıyoruz. Darbeye ve sıcağa PLA'dan daha dirençli."),
                 ("TPU",
                  "Esnek olması gereken parçalar için. Bükülüp eski hâline dönmesi gereken yerlerde "
                  "bu malzemeye geçiyoruz."),
             ]},
            {"h2": "Ankara içi teslim, Türkiye geneli kargo",
             "p": ["Ankara içindeyseniz ürünü elden teslim edebiliyoruz. Türkiye'nin her yerine de "
                   "güvenli kargo ile gönderim yapıyoruz.",
                   "Siparişler, ürünün karmaşıklığına göre değişmekle birlikte genellikle 3 ila 7 iş günü "
                   "içinde kargoya teslim ediliyor. Boyama ve elle rötuş gerektiren figürlerde bu süre "
                   "üst sınıra yaklaşıyor."]},
            {"h2": "Ankara'da ne bastırabilirsiniz?",
             "liste": [
                 "Kişi, evcil hayvan veya karakter fotoğrafından üretilen kişiye özel figür",
                 "Fotoğraftan modellenen araba ve motosiklet maketi",
                 "Çerçeve, plaket, lamba ve stand gibi kişiye özel ev dekoru",
                 "Etkinlik ve firma hediyeliği olarak toplu anahtarlık üretimi",
                 "Pasta süsü setleri ve doğum günü figürleri",
             ]},
            {"h2": "Başlangıç fiyatları",
             "p": ["Aşağıdaki tutarlar ölçü, detay ve boyaya göre değişen başlangıç aralıklarıdır. "
                   "Kesin fiyat için ürün görselini WhatsApp'tan gönderin, birlikte netleştirelim."],
             "tablo": {
                 "basliklar": ["Ürün", "Başlangıç fiyatı"],
                 "satirlar": [
                     ["Kişiye özel 3D figür", "1.750 TL"],
                     ["Araç ve motosiklet maketi", "2.500 TL"],
                     ["Anahtarlık, adet başına", "150 TL – 350 TL"],
                     ["Hediyelik ve ev dekoru", "Modele göre değişken"],
                 ]}},
        ],
        "sss": [
            ("Ankara'da elden teslim alabilir miyim?",
             "Evet. Ankara içindeyseniz ürünü elden teslim edebiliyoruz, ayrıntıyı WhatsApp'tan konuşuyoruz."),
            ("Teslimat ne kadar sürer?",
             "Ürünün karmaşıklığına göre değişmekle birlikte siparişler genellikle 3-7 iş günü içinde "
             "kargoya teslim edilir."),
            ("Şehir dışına gönderim yapıyor musunuz?",
             "Evet, Türkiye'nin her yerine güvenli kargo ile gönderim yapıyoruz."),
            ("Elimde 3D model yok, yine de bastırabilir miyim?",
             "Bastırabilirsiniz. Fikri, fotoğrafı ya da ölçüyü alıp baskıya hazır modeli biz tasarlıyoruz."),
        ],
    },
    {
        "slug": "kisiye-ozel-3d-figur",
        "title": "Kişiye Özel 3D Figür | Fiyat ve Süreç | 3dartolyemiz",
        "desc": "Fotoğraftan kişiye özel 3D figür. Evcil hayvan, aile ve karakter figürleri, "
                "elle boyama. Ankara'da üretim, Türkiye geneli kargo.",
        "h1": "Kişiye özel 3D figür",
        "lead": "Bir fotoğraf yeterli. Kişiyi, evcil hayvanı ya da sevdiğiniz karakteri modelleyip "
                "basıyor, elle boyayıp gönderiyoruz.",
        "sema": "Service",
        "sema_ad": "Kişiye özel 3D figür üretimi",
        "bolumler": [
            {"h2": "Ne tür figürler yapıyoruz?",
             "kartlar": [
                 ("Evcil hayvan figürü",
                  "Köpeğinizin ya da kedinizin fotoğrafından, tüy rengine kadar boyanmış figür. "
                  "Chihuahua ve Fransız bulldog gibi çalışmalarımız galeride duruyor."),
                 ("Aile ve kişi figürü",
                  "ARTOPOP aile figürleri ve tek kişilik portre figürler. Yıldönümü ve doğum günü "
                  "hediyesi olarak en çok istenenler."),
                 ("Karakter ve oyun figürü",
                  "Anime karakterleri, oyun figürleri ve koleksiyonluk büstler. İnce detay "
                  "gerektiği için genelde reçineyle basıyoruz."),
                 ("Diorama ve set",
                  "Kamp ateşi dioraması ya da mini figür setleri gibi, birden çok parçanın "
                  "bir arada durduğu çalışmalar."),
             ]},
            {"h2": "Katalogdan fiyat örnekleri",
             "p": ["Bunlar daha önce ürettiğimiz işlerin fiyatları. Ölçü, detay ve boya miktarı "
                   "değiştikçe tutar da değişiyor."],
             "tablo": {
                 "basliklar": ["Çalışma", "Fiyat"],
                 "satirlar": [
                     ["Kişiye özel uluyan kurt figürü", "750 TL"],
                     ["Kişiye özel chihuahua figürü", "950 TL"],
                     ["Kişiye özel mini figür seti", "1.400 TL"],
                     ["Sprinku figürü", "1.750 TL"],
                     ["Kişiye özel ARTOPOP aile figürü", "1.900 TL"],
                     ["Samuray büstü figürü", "1.950 TL"],
                     ["Maşa ile Koca Ayı figürü", "2.400 TL"],
                     ["Minecraft Warden figürü", "2.750 TL"],
                 ]}},
            {"h2": "Nasıl ilerliyoruz?",
             "liste": [
                 "Fikrinizi ve fotoğrafı WhatsApp'tan gönderiyorsunuz.",
                 "Size özel hazırladığımız tasarım önizlemesini birlikte gözden geçirip onaylıyoruz.",
                 "Üretim ve boyama tamamlanınca özenle paketleyip adrese gönderiyoruz.",
             ]},
        ],
        "sss": [
            ("Fotoğraftan figür yapmak için nasıl bir fotoğraf gerekiyor?",
             "Yüzün ya da vücudun net göründüğü bir fotoğraf yeterli. Birden fazla açı varsa "
             "benzerlik daha yüksek çıkıyor."),
            ("Figürler boyalı mı geliyor?",
             "Evet, figürleri elle boyayıp gönderiyoruz. Kendiniz boyamak isterseniz boyanmamış "
             "hâliyle de hazırlayabiliyoruz."),
            ("Fiyat neye göre değişiyor?",
             "Boyuta, detay yoğunluğuna ve boya işçiliğine göre değişiyor. Kesin fiyat için "
             "görseli gönderdiğinizde netleştiriyoruz."),
        ],
    },
    {
        "slug": "3d-modelleme",
        "title": "3D Modelleme Hizmeti | Ankara | 3dartolyemiz",
        "desc": "Elinizde model yoksa sıfırdan tasarlıyoruz. Fikir, fotoğraf ya da ölçüden "
                "baskıya hazır 3D model. Ankara'da 3D modelleme hizmeti.",
        "h1": "3D modelleme hizmeti",
        "lead": "Baskı almak için önce bir modele ihtiyaç var. Elinizde yoksa o kısmı biz üstleniyoruz.",
        "sema": "Service",
        "sema_ad": "3D modelleme",
        "bolumler": [
            {"h2": "Ne zaman modelleme gerekir?",
             "p": ["Hazır bir dosyanız varsa doğrudan baskıya geçebiliyoruz. Ama çoğu iş öyle "
                   "başlamıyor. Aklınızda bir fikir, elinizde bir fotoğraf ya da bir ölçü oluyor. "
                   "Modelleme tam olarak bu aradaki adım."],
             "kartlar": [
                 ("Fikirden",
                  "Anlattığınız şeyi çiziyor, ölçülendirip baskıya hazır hâle getiriyoruz."),
                 ("Fotoğraftan",
                  "Kişi, evcil hayvan ya da araç fotoğrafından model çıkarıyoruz. "
                  "Kişiye özel figürlerin çoğu böyle üretiliyor."),
                 ("Ölçüden",
                  "Belirli bir yere oturması gereken parçalarda ölçüyü alıp modeli ona göre kuruyoruz."),
             ]},
            {"h2": "Modelleme sonunda ne alıyorsunuz?",
             "p": ["Baskıya hazır bir model ve onun basılmış hâli. Model üzerinde değişiklik "
                   "isterseniz önizleme aşamasında birlikte düzeltiyoruz, üretim onayınızdan sonra "
                   "başlıyor."]},
        ],
        "sss": [
            ("Sadece modelleme yaptırıp baskıyı başka yerde aldırabilir miyim?",
             "Bunu WhatsApp'tan konuşalım, işin kapsamına göre değerlendiriyoruz."),
            ("Modelleme fiyatı nasıl belirleniyor?",
             "İşin karmaşıklığına göre değişiyor. Fikri anlattığınızda net bir teklif veriyoruz."),
        ],
    },
    {
        "slug": "dogum-gunu-boyama-atolyesi",
        "title": "Doğum Günü Boyama Atölyesi | Ankara | 3dartolyemiz",
        "desc": "Çocuk doğum günlerine gelen 3D figür boyama atölyesi. Tüm boya ve figürler dahil, "
                "8-10 kişilik gruplara uygun, ortalama 45 dakika. Ankara.",
        "h1": "Doğum günü boyama atölyesi",
        "lead": "Evinize ya da parti alanınıza geliyoruz. Minik davetliler kendi figürlerini boyuyor "
                "ve boyadıkları figür onlarda kalıyor.",
        "sema": "Service",
        "sema_ad": "Doğum günü boyama atölyesi",
        "bolumler": [
            {"h2": "Atölye nasıl işliyor?",
             "p": ["Kurulumu biz yapıyoruz, siz hiçbir şey hazırlamıyorsunuz. Çocuklar 3D "
                   "yazıcıdan çıkmış boyanmamış figürleri alıyor ve kendi renkleriyle boyuyor. "
                   "Atölye bitince herkes kendi figürüyle evine gidiyor."],
             "kartlar": [
                 ("Tüm malzeme bizden",
                  "Boyalar ve figürler dahil. Ek bir malzeme almanız gerekmiyor."),
                 ("8-10 çocuklu gruplara uygun",
                  "Bu sayıda herkes rahat rahat masaya sığıyor ve ilgilenebiliyoruz."),
                 ("Ortalama 45 dakika",
                  "Doğum günü programını bölmeyecek, çocukların da sıkılmayacağı bir süre."),
                 ("5-12 yaş için ideal",
                  "Farklı yaş gruplarına göre de uyarlayabiliyoruz, önceden konuşmamız yeterli."),
             ]},
            {"h2": "Kendin Boya Seti",
             "p": ["Atölyeye gelemiyorsanız aynı deneyimin kutulu hâli var. Kutunun içinde "
                   "boyanmamış figür, beş renkli mini boya ve iki fırça çıkıyor. Doğum günü "
                   "hediyesi olarak da veriliyor."]},
        ],
        "sss": [
            ("Doğum günü etkinliği hangi yaş grubuna uygun?",
             "Boyama atölyemiz genellikle 5-12 yaş arası çocuklar için idealdir, farklı yaş "
             "gruplarına göre de uyarlayabiliyoruz."),
            ("Etkinlik ne kadar sürüyor?",
             "Ortalama 45 dakika sürüyor. Grup kalabalıksa biraz uzayabiliyor."),
            ("Boya ve figürleri biz mi temin ediyoruz?",
             "Hayır, tüm boya ve figürler bize ait. Siz sadece yeri ayarlıyorsunuz."),
            ("Etkinlik için nasıl yer ayırtabilirim?",
             "WhatsApp üzerinden tarih ve kişi sayısını yazmanız yeterli, uygunluğu birlikte netleştiriyoruz."),
        ],
    },
]

DIGER_AD = {s["slug"]: s["h1"] for s in SAYFALAR}

# --------------------------------------------------------------------- kabuk

kaynak = io.open(KOK / "index.html", encoding="utf-8").read()

bas = kaynak[kaynak.index("<body"):kaynak.index("<main")]
son = kaynak[kaynak.index("</main>"):]
head = kaynak[:kaynak.index("<body")]


def koke_cevir(parca: str) -> str:
    """Alt sayfada calisan mutlak yollar."""
    parca = parca.replace('href="#top"', 'href="/"')
    parca = re.sub(r'href="#(?!main\b)([\w-]+)"', r'href="/#\1"', parca)
    parca = parca.replace('src="assets/', 'src="/assets/')
    parca = parca.replace('href="assets/', 'href="/assets/')
    return parca


bas = koke_cevir(bas)
son = koke_cevir(son)


def head_uret(s: dict) -> str:
    url = f"{ALAN}/{s['slug']}/"
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{s['title']}</title>", h, count=1, flags=re.S)
    for alan in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        h = re.sub(rf'({alan} content=")[^"]*(")', lambda m: m.group(1) + s["desc"] + m.group(2), h, count=1)
    for alan in ['property="og:title"', 'name="twitter:title"']:
        h = re.sub(rf'({alan} content=")[^"]*(")', lambda m: m.group(1) + s["title"] + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = h.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    # ana sayfanin semalari alt sayfaya tasinmasin
    h = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", h, flags=re.S)
    return h + sema_uret(s)


def sema_uret(s: dict) -> str:
    url = f"{ALAN}/{s['slug']}/"
    bloklar = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": ALAN + "/"},
            {"@type": "ListItem", "position": 2, "name": s["h1"], "item": url},
        ]}, {
        "@context": "https://schema.org", "@type": "Service",
        "name": s["sema_ad"], "description": s["desc"], "url": url,
        "serviceType": s["sema_ad"],
        "areaServed": [{"@type": "City", "name": "Ankara"}, {"@type": "Country", "name": "Türkiye"}],
        "provider": {"@type": "LocalBusiness", "name": "3dartolyemiz", "url": ALAN + "/",
                     "telephone": "+905441885744",
                     "address": {"@type": "PostalAddress",
                                 "streetAddress": "Mehmet Akif Ersoy Mahallesi 266.Cad No:4",
                                 "addressLocality": "Yenimahalle", "addressRegion": "Ankara",
                                 "postalCode": "06200", "addressCountry": "TR"}},
    }]
    if s.get("sss"):
        bloklar.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": c}} for q, c in s["sss"]]})
    return "".join(
        '\n  <script type="application/ld+json">\n'
        + json.dumps(b, ensure_ascii=False, indent=2) + "\n  </script>" for b in bloklar) + "\n"


def bolum_uret(b: dict) -> str:
    p = [f'    <div class="section-head reveal"><h2>{b["h2"]}</h2></div>']
    for metin in b.get("p", []):
        p.append(f'    <p class="sayfa-metin reveal">{metin}</p>')
    if b.get("liste"):
        p.append('    <ul class="sayfa-liste reveal">')
        p += [f"      <li>{x}</li>" for x in b["liste"]]
        p.append("    </ul>")
    if b.get("kartlar"):
        p.append('    <div class="card-grid">')
        for ad, metin in b["kartlar"]:
            p.append(f'      <div class="card reveal"><h3>{ad}</h3><p>{metin}</p></div>')
        p.append("    </div>")
    if b.get("tablo"):
        t = b["tablo"]
        p.append('    <div class="fiyat-tablo reveal"><table>')
        p.append("      <thead><tr>" + "".join(f"<th>{x}</th>" for x in t["basliklar"]) + "</tr></thead>")
        p.append("      <tbody>")
        for satir in t["satirlar"]:
            p.append("        <tr>" + "".join(f"<td>{x}</td>" for x in satir) + "</tr>")
        p.append("      </tbody></table></div>")
    return "\n".join(p)


def govde_uret(s: dict) -> str:
    parcalar = [f'''<main id="main">
  <section class="hero hero--sayfa">
    <div class="container">
      <nav class="kirinti" aria-label="Konum"><a href="/">Ana sayfa</a> <span>/</span> <span>{s["h1"]}</span></nav>
      <h1>{s["h1"]}</h1>
      <p class="lead">{s["lead"]}</p>
      <div class="hero-ctas"><a class="btn btn-primary" href="{TEL}" target="_blank" rel="noopener">WhatsApp'tan yaz</a></div>
    </div>
  </section>

  <section>
    <div class="container">''']
    parcalar += [bolum_uret(b) for b in s["bolumler"]]
    parcalar.append("    </div>\n  </section>")

    if s.get("sss"):
        sss = "\n".join(
            f'        <details class="faq-item"><summary>{q}</summary><p>{c}</p></details>'
            for q, c in s["sss"])
        parcalar.append(f'''
  <section class="section--alt">
    <div class="container">
      <div class="section-head reveal"><span class="eyebrow">Merak Edilenler</span><h2>Sıkça sorulan sorular</h2></div>
      <div class="faq reveal">
{sss}
      </div>
    </div>
  </section>''')

    digerleri = "\n".join(
        f'        <li><a href="/{sl}/">{ad}</a></li>'
        for sl, ad in DIGER_AD.items() if sl != s["slug"])
    parcalar.append(f'''
  <section>
    <div class="container">
      <div class="section-head reveal"><h2>Diğer hizmetlerimiz</h2></div>
      <ul class="sayfa-liste reveal">
{digerleri}
        <li><a href="/#urunler">Ürün kataloğu ve fiyatlar</a></li>
      </ul>
    </div>
  </section>''')
    return "\n".join(parcalar) + "\n"


# --------------------------------------------------------------------- urun sayfalari
# Google kurali: urun zengin sonucu YALNIZCA tek urune odakli sayfada gecerli.
# Birden cok urunu listeleyen sayfada Product isaretlemesi "gecersiz oge" sayiliyor
# (Search Console bunu bildirdi). Bu yuzden her katalog urunu kendi sayfasini alir,
# ana sayfadaki ItemList ise ozet bicime duser: yalnizca @type, position ve url.

TR_MAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def sluglastir(metin: str) -> str:
    metin = metin.replace("&amp;", "ve").translate(TR_MAP)
    metin = unicodedata.normalize("NFKD", metin).encode("ascii", "ignore").decode()
    metin = re.sub(r"[^a-zA-Z0-9]+", "-", metin).strip("-").lower()
    return re.sub(r"-{2,}", "-", metin)


KART = re.compile(
    r'<div class="product-card[^"]*">\s*<div class="product-media">\s*'
    r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>\s*<span class="tag">([^<]*)</span>'
    r'.*?<h3>([^<]+)</h3>\s*<p>([^<]*)</p>\s*<div class="price-badge">([^<]+)</div>\s*'
    r'<span class="price-note">([^<]*)</span>\s*<a[^>]+href="([^"]+)"', re.S)


def urunleri_oku(metin: str) -> list:
    """Yalnizca katalog basligindan SONRAKI, tek sabit fiyatli kartlar."""
    kesim = metin.find("Ürün Kataloğu")
    cikti = []
    for m in KART.finditer(metin[kesim:]):
        fiyat_metni = m.group(6).strip()
        sayilar = re.findall(r"(\d[\d.]*)\s*TL", fiyat_metni)
        if len(sayilar) != 1 or "başlayan" in fiyat_metni:
            continue  # kategori karti, tekil urun degil
        ad = m.group(4).replace("&amp;", "&").strip()
        cikti.append({
            "ad": ad, "slug": sluglastir(ad),
            "gorsel": "/" + m.group(1).lstrip("/"),
            "alt": m.group(2).strip(),
            "etiket": m.group(3).replace("&amp;", "&").strip(),
            "aciklama": m.group(5).strip(),
            "fiyat_metni": fiyat_metni,
            "fiyat": int(sayilar[0].replace(".", "")),
            "not": m.group(7).strip(),
            "wa": m.group(8),
        })
    return cikti


def urun_sayfasi(u: dict) -> str:
    url = f"{ALAN}/urun/{u['slug']}/"
    semalar = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": ALAN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ürünler", "item": ALAN + "/#urunler"},
            {"@type": "ListItem", "position": 3, "name": u["ad"], "item": url}]},
        {"@context": "https://schema.org", "@type": "Product",
         "name": u["ad"], "description": u["aciklama"], "url": url,
         "image": ALAN + u["gorsel"], "category": u["etiket"],
         "brand": {"@type": "Brand", "name": "3dartolyemiz"},
         "offers": {"@type": "Offer", "price": u["fiyat"], "priceCurrency": "TRY",
                    "availability": "https://schema.org/InStock", "url": url,
                    "seller": {"@type": "Organization", "name": "3dartolyemiz"}}},
    ]
    sema = "".join('\n  <script type="application/ld+json">\n'
                   + json.dumps(b, ensure_ascii=False, indent=2)
                   + "\n  </script>" for b in semalar) + "\n"

    baslik = f"{u['ad']} | {u['fiyat_metni']} | 3dartolyemiz"
    aciklama = (f"{u['ad']}: {u['aciklama']} Fiyat {u['fiyat_metni']}. "
                "Ankara'da üretim, Türkiye geneli kargo.")
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{baslik}</title>", h, count=1, flags=re.S)
    for alan in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        h = re.sub(rf'({alan} content=")[^"]*(")', lambda m: m.group(1) + aciklama + m.group(2), h, count=1)
    for alan in ['property="og:title"', 'name="twitter:title"']:
        h = re.sub(rf'({alan} content=")[^"]*(")', lambda m: m.group(1) + u["ad"] + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
               lambda m: m.group(1) + ALAN + u["gorsel"] + m.group(2), h, count=1)
    h = h.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    h = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", h, flags=re.S)

    govde = (
        '<main id="main">\n'
        '  <section class="hero hero--sayfa">\n    <div class="container">\n'
        '      <nav class="kirinti" aria-label="Konum"><a href="/">Ana sayfa</a> <span>/</span> '
        '<a href="/#urunler">Ürünler</a> <span>/</span> <span>' + u["ad"] + '</span></nav>\n'
        '      <h1>' + u["ad"] + '</h1>\n'
        '      <p class="lead">' + u["aciklama"] + '</p>\n'
        '    </div>\n  </section>\n\n'
        '  <section>\n    <div class="container">\n      <div class="urun-detay">\n'
        '        <img class="urun-gorsel" src="' + u["gorsel"] + '" alt="' + u["alt"] + '" '
        'width="900" height="1200" loading="eager" decoding="async">\n'
        '        <div class="urun-bilgi">\n'
        '          <span class="tag">' + u["etiket"] + '</span>\n'
        '          <div class="price-badge">' + u["fiyat_metni"] + '</div>\n'
        '          <span class="price-note">' + u["not"] + '</span>\n'
        '          <p>Ankara\'daki atölyemizde üretiliyor. Ankara içi elden teslim, Türkiye geneli '
        'kargo. Siparişler genellikle 3-7 iş günü içinde kargoya veriliyor.</p>\n'
        '          <p>Aynı ürünü farklı ölçü, renk ya da kişiye özel detayla da yapabiliyoruz. '
        'Ne istediğinizi yazın, birlikte netleştirelim.</p>\n'
        '          <a class="btn btn-primary" href="' + u["wa"] + '" target="_blank" rel="noopener">'
        'WhatsApp\'tan sipariş ver</a>\n'
        '        </div>\n      </div>\n    </div>\n  </section>\n\n'
        '  <section class="section--alt">\n    <div class="container">\n'
        '      <div class="section-head reveal"><h2>Devamı</h2></div>\n'
        '      <ul class="sayfa-liste reveal">\n'
        '        <li><a href="/kisiye-ozel-3d-figur/">Kişiye özel 3D figür sayfası</a></li>\n'
        '        <li><a href="/ankara-3d-baski/">Ankara\'da 3D baskı hizmeti</a></li>\n'
        '        <li><a href="/#urunler">Tüm ürün kataloğu ve fiyatlar</a></li>\n'
        '      </ul>\n    </div>\n  </section>\n')
    return h + sema + bas + govde + son


OK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def kartlara_baglanti_ekle(urunler: list) -> bool:
    """Katalog kartlarindan urun sayfasina gorunur baglanti. Idempotent."""
    yol = KOK / "index.html"
    metin = io.open(yol, encoding="utf-8").read()
    degisti = False
    for u in urunler:
        if f'href="/urun/{u["slug"]}/"' in metin:
            continue
        i = metin.find("<h3>" + u["ad"].replace("&", "&amp;") + "</h3>")
        if i < 0:
            i = metin.find("<h3>" + u["ad"] + "</h3>")
        if i < 0:
            print(f"  UYARI: kart bulunamadi -> {u['ad']}")
            continue
        j = metin.find("</a>", metin.find('class="btn', i))
        if j < 0:
            continue
        j += 4
        bag = f'\n            <a class="card-link" href="/urun/{u["slug"]}/">Ürün detayı {OK_SVG}</a>'
        metin = metin[:j] + bag + metin[j:]
        degisti = True
    if degisti:
        io.open(yol, "w", encoding="utf-8").write(metin)
    return degisti


def anasayfa_listesini_ozetle(urunler: list) -> bool:
    """Ana sayfadaki ItemList'i Google'in ozet-sayfa bicimine dusurur."""
    yol = KOK / "index.html"
    metin = io.open(yol, encoding="utf-8").read()
    degisti = False
    for b in reversed(list(re.finditer(r'(<script[^>]+ld\+json[^>]*>)(.*?)(</script>)', metin, re.S))):
        veri = json.loads(b.group(2))
        ogeler = veri if isinstance(veri, list) else [veri]
        bu_blok = False
        for x in ogeler:
            if x.get("@type") != "ItemList":
                continue
            yeni_ogeler = [{"@type": "ListItem", "position": i, "url": f"{ALAN}/urun/{u['slug']}/"}
                           for i, u in enumerate(urunler, 1)]
            if x.get("itemListElement") != yeni_ogeler:
                x["itemListElement"] = yeni_ogeler
                x["numberOfItems"] = len(yeni_ogeler)
                bu_blok = degisti = True
        if bu_blok:
            yeni = json.dumps(veri if isinstance(veri, list) else ogeler[0], ensure_ascii=False, indent=2)
            metin = metin[:b.start(2)] + "\n" + yeni + "\n  " + metin[b.end(2):]
    if degisti:
        io.open(yol, "w", encoding="utf-8").write(metin)
    return degisti


# --------------------------------------------------------------------- yaz

uretilen = []
for s in SAYFALAR:
    hedef = KOK / s["slug"]
    hedef.mkdir(exist_ok=True)
    icerik = head_uret(s) + bas + govde_uret(s) + son
    io.open(hedef / "index.html", "w", encoding="utf-8").write(icerik)
    uretilen.append(s["slug"])
    print(f"  yazildi: /{s['slug']}/  ({len(icerik)} bayt)")

URUNLER = urunleri_oku(kaynak)
for u in URUNLER:
    hedef = KOK / "urun" / u["slug"]
    hedef.mkdir(parents=True, exist_ok=True)
    io.open(hedef / "index.html", "w", encoding="utf-8").write(urun_sayfasi(u))
print(f"  {len(URUNLER)} urun sayfasi uretildi")
if kartlara_baglanti_ekle(URUNLER):
    print("  katalog kartlarina urun sayfasi baglantisi eklendi")
if anasayfa_listesini_ozetle(URUNLER):
    print("  ana sayfadaki ItemList ozet bicime dusuruldu")

# sitemap
girdiler = [f"  <url>\n    <loc>{ALAN}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>"]
girdiler += [f"  <url>\n    <loc>{ALAN}/{sl}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
             for sl in uretilen]
girdiler += [f"  <url>\n    <loc>{ALAN}/urun/{u['slug']}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
             for u in URUNLER]
io.open(KOK / "sitemap.xml", "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(girdiler) + "\n</urlset>\n")
print(f"  sitemap.xml: {len(girdiler)} adres")
print(f"{len(uretilen)} hizmet sayfasi + {len(URUNLER)} urun sayfasi uretildi.")
