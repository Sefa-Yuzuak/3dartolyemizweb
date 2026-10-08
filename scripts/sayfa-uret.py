"""Alt sayfa ureteci.

index.html tek sayfa olarak kalir ve kabuk (head, header, footer) icin
tek dogru kaynak odur. Bu betik o kabugu index.html'den okur, icerigi
degistirip alt sayfalari yazar. Boylece menu ya da footer degistiginde
tek yerde degistirmek yeterli olur: index.html, sonra bu betigi calistir.

Kullanim:  python scripts/sayfa-uret.py

Kural: uydurma bilgi yok. Buradaki her olgu (fiyat, sure, yas araligi,
malzeme, kutu icerigi) ya index.html'de, ya Instagram aciklamalarinda ya da
08.10.2026'da okunan Instagram mesajlarinda (sahibin musteriye verdigi fiyat,
sure ve surec) yaziyor; sahibin ayrica teyit ettikleri: Panora AVM atolyesi
bitti, egitim ve Ankara ici yazici tamiri suruyor, STL getirilirse basiliyor.

Urunler content/urunler.json, etiketler content/etiketler.json'dadir: katalog,
urun ve etiket sayfalari, ana sayfanin one cikanlari, fiyat tablolari,
llms.txt ve nginx'teki eski magaza yonlendirmeleri bu iki dosyadan uretilir.
"""
from __future__ import annotations

import io
import json
import re
from pathlib import Path
from urllib.parse import quote

import blog
from urun_icerik import urun_icerik

KOK = Path(__file__).resolve().parent.parent
ALAN = "https://artolyemiz.com"
TEL = "https://wa.me/905441885744?text=Merhaba%2C%20siteniz%20%C3%BCzerinden%20ula%C5%9F%C4%B1yorum"

# --------------------------------------------------------------------- urun verisi
# Fiyatlar araliktir (sahibin istegi: "araligi genis tut"). Aralik, 08.10.2026'da
# Instagram mesajlarinda musteriye verilen fiyatlardan genisletilerek yazildi;
# ornek: 20 cm kisiye ozel boyali figur kisi basi 2.400-3.750 TL, 20 cm plaka ve
# platform dahil motor/araba maketi 3.500-4.750 TL (Haz-Eki 2026).


def tl(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def urunleri_oku() -> list:
    urunler = json.load(io.open(KOK / "content" / "urunler.json", encoding="utf-8"))
    for u in urunler:
        alt_, ust = u["fiyat"]
        if not 0 < alt_ < ust:
            raise SystemExit(f"{u['slug']}: fiyat araligi gecersiz {u['fiyat']}")
        aralik_ = f"{tl(alt_)} – {tl(ust)} TL"
        u["fiyat_metni"] = f"Yaklaşık {aralik_}" + (" / adet" if u["adet"] else "")
        u["fiyat_kucuk"] = ("adet başına " if u["adet"] else "") + f"yaklaşık {aralik_}"
        u["kart_gorsel"] = u["gorsel"].replace(".webp", "-sm.webp")
        u["not"] = "Kesin fiyat ölçü ve detaya göre netleşir · görsel temsilidir"
        u["wa"] = ("https://wa.me/905441885744?text="
                   + quote(f"Merhaba, {u['ad']} için fiyat almak istiyorum."))
        for yol in (u["gorsel"], u["kart_gorsel"]):
            if not (KOK / yol.lstrip("/")).exists():
                raise SystemExit(f"{u['slug']}: gorsel yok {yol}")
    return urunler


URUNLER = urunleri_oku()
URUN = {u["slug"]: u for u in URUNLER}
ETIKETLER = json.load(io.open(KOK / "content" / "etiketler.json", encoding="utf-8"))
ETIKET = {e["slug"]: e for e in ETIKETLER}
for _u in URUNLER:
    for _e in _u["etiketler"]:
        if _e not in ETIKET:
            raise SystemExit(f"{_u['slug']}: bilinmeyen etiket '{_e}' (content/etiketler.json)")


def etiket_urunleri(slug: str) -> list:
    return [u for u in URUNLER if slug in u["etiketler"]]


def aralik(etiket: str) -> str:
    """Etiketteki urunlerin fiyat araligi: '1.000 – 4.750 TL'. Elle yazilmaz."""
    us = etiket_urunleri(etiket)
    return f"{tl(min(u['fiyat'][0] for u in us))} – {tl(max(u['fiyat'][1] for u in us))} TL"


# --------------------------------------------------------------------- icerik

SUREC = [
    "WhatsApp'tan yazın: ne istediğinizi, fotoğrafı ya da elinizdeki 3D dosyayı gönderin.",
    "Elinizde model yoksa biz modelliyoruz ve modelin videosunu size gönderiyoruz.",
    "Beğenirseniz kapora alıp baskıya geçiyoruz; değişiklik isterseniz bu aşamada yapıyoruz.",
    "Baskı ve elle boyama bitince ürünün videosunu tekrar atıyoruz; kalan tutar ödenince "
    "Ankara içinde elden teslim ediyor ya da kargoya veriyoruz.",
]
SURE = ("Genellikle 3-7 gün içinde hazırlanıp kargoya veriliyor. Elle boyanan işlerde süre "
        "üst sınıra yaklaşıyor; yoğun dönemlerde 10-14 güne çıkabiliyor. Kargo 2-3 gün sürüyor.")
SSS_ODEME = ("Ödeme nasıl yapılıyor, taksit var mı?",
             "Modelin videosunu onayladığınızda kapora alıp baskıya geçiyoruz; kalan tutarı ürün "
             "bitince, videosunu gördükten sonra ödüyorsunuz. Taksit imkânımız yok.")

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
            # Adimlarin her olgusu bu sayfada zaten yazili (lead, teslim bolumu, SSS);
            # muadil olcumu (Craftcloud/Protolabs/T3 Dizayn, 13.09.2026): surec akisi
            # her profesyonel atolye sayfasinda var, bizde yoktu.
            {"h2": "Nasıl çalışır?",
             "liste": SUREC},
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
             ],
             # Kartlardaki ayni bilgi karar tablosu olarak: "benim isim icin hangisi?"
             "tablo": {
                 "basliklar": ["İhtiyaç", "Önerdiğimiz malzeme"],
                 "satirlar": [
                     ["İnce detay: yüz hatları, küçük parçalar, büst", "SLA reçine"],
                     ["Dekor, hediyelik, maket; boyanacak yüzey", "PLA"],
                     ["Darbeye ve sıcağa dayanım", "PETG"],
                     ["Bükülüp eski hâline dönmesi gereken parça", "TPU"],
                 ]}},
            {"h2": "Ankara içi teslim, Türkiye geneli kargo",
             "p": ["Ankara içindeyseniz ürünü elden teslim edebiliyoruz. Atölyemiz Yenimahalle'de, "
                   "Nazım Hikmet Kültür Merkezi'nin yanında. Türkiye'nin her yerine de güvenli kargo ile "
                   "gönderim yapıyoruz.", SURE]},
            {"h2": "Ankara'da ne bastırabilirsiniz?",
             "liste": [
                 '<a href="/kisiye-ozel-3d-figur/">Kişi, evcil hayvan veya karakter fotoğrafından üretilen kişiye özel figür</a>',
                 '<a href="/3d-baski-maket/">Fotoğraftan modellenen araba ve motosiklet maketi, diorama</a>',
                 "Çerçeve, plaket, lamba ve stand gibi kişiye özel ev dekoru",
                 '<a href="/etiket/toplu-siparis/">Etkinlik ve firma hediyeliği olarak toplu anahtarlık üretimi</a>',
                 '<a href="/etiket/pasta-susu/">Pasta süsü, yaş rakamı ve doğum günü figürleri</a>',
                 '<a href="/stl-dosyasi-bastirma/">Elinizdeki STL ya da 3MF dosyasının baskısı</a>',
                 '<a href="/3d-yazici-egitimi/">3D yazıcı eğitimi</a> ve '
                 '<a href="/3d-yazici-tamiri-ankara/">Ankara içi 3D yazıcı tamiri</a>',
             ]},
            {"h2": "Yaklaşık fiyat aralıkları",
             "p": ["Aşağıdaki aralıklar katalogdaki çalışmalardan hesaplanıyor; ölçü, detay ve boyaya "
                   "göre değişir. Kesin fiyat için ürün görselini WhatsApp'tan gönderin, birlikte netleştirelim."],
             "etiket_fiyatlari": ["kisiye-ozel-figur", "araba-maketi", "motosiklet-maketi",
                                  "evcil-hayvan-figuru", "anahtarlik", "pasta-susu",
                                  "kendin-boya-seti", "ev-dekor"]},
        ],
        "sss": [
            ("Ankara'da elden teslim alabilir miyim?",
             "Evet. Ankara içindeyseniz ürünü elden teslim edebiliyoruz, ayrıntıyı WhatsApp'tan konuşuyoruz."),
            ("Teslimat ne kadar sürer?", SURE),
            ("Şehir dışına gönderim yapıyor musunuz?",
             "Evet, Türkiye'nin her yerine güvenli kargo ile gönderim yapıyoruz."),
            ("Elimde 3D model yok, yine de bastırabilir miyim?",
             "Bastırabilirsiniz. Kendi STL dosyanızı getirirseniz doğrudan basıyoruz; getirmezseniz "
             "fikri, fotoğrafı ya da ölçüyü alıp modeli biz çıkarıyoruz."),
            SSS_ODEME,
        ],
    },
    {
        "slug": "kisiye-ozel-3d-figur",
        "title": "Figür Yaptırma | Fotoğraftan Kişiye Özel 3D Figür | Ankara",
        "desc": "Fotoğraftan kişiye özel 3D figür: kişi, aile, evcil hayvan ve karakter. Elle boyama, "
                f"yaklaşık {aralik('kisiye-ozel-figur')}. Ankara'da üretim, Türkiye geneli kargo.",
        "h1": "Kişiye özel 3D figür yaptırma",
        "lead": "Bir fotoğraf yeterli. Kişiyi, evcil hayvanı ya da sevdiğiniz karakteri modelleyip "
                "basıyor, elle boyayıp gönderiyoruz.",
        "sema": "Service",
        "sema_ad": "Kişiye özel 3D figür üretimi",
        "bolumler": [
            {"h2": "Ne tür figürler yapıyoruz?",
             "kartlar": [
                 ("Evcil hayvan figürü",
                  "Köpeğinizin ya da kedinizin fotoğrafından, tüy rengine kadar boyanmış figür ya da "
                  'anahtarlık. <a href="/etiket/evcil-hayvan-figuru/">Evcil hayvan çalışmalarımız</a>.'),
                 ("Aile ve kişi figürü",
                  "ARTOPOP aile figürleri ve tek kişilik portre figürler; genelde 15-20 cm. Yıldönümü "
                  "ve doğum günü hediyesi olarak en çok istenenler."),
                 ("Karakter ve oyun figürü",
                  "Anime karakterleri, oyun figürleri ve koleksiyonluk büstler. İnce detay "
                  'gerektiği için genelde reçineyle basıyoruz. <a href="/etiket/karakter-figuru/">'
                  "Karakter figürleri</a>."),
                 ("Diorama ve set",
                  "Kamp ateşi dioraması ya da mini figür setleri gibi, birden çok parçanın "
                  "bir arada durduğu çalışmalar."),
             ]},
            {"h2": "Figür örneklerimiz",
             "p": ["Atölyede ürettiğimiz figürlerden bir seçki. Her birini farklı ölçü, renk ya da "
                   "kişiye özel detayla yeniden yapabiliyoruz."],
             "urun_kartlari": ["kisiye-ozel-artopop-aile-figuru", "kisiye-ozel-kopek-figuru",
                               "kisiye-ozel-kedi-figuru", "pop-tarzi-futbolcu-figuru",
                               "kisiye-ozel-anime-karakter-figuru", "evcil-hayvan-anahtarlik",
                               "artopop-kendin-boya-kutusu", "samuray-bustu-figuru"]},
            {"h2": "Katalogdan yaklaşık fiyat örnekleri",
             "p": ["Bunlar daha önce ürettiğimiz işlerin yaklaşık fiyatları. Ölçü, detay ve boya "
                   "miktarı değiştikçe tutar da değişiyor."],
             "fiyat_urunleri": ["artopop-kendin-boya-kutusu", "pop-tarzi-futbolcu-figuru",
                                "kisiye-ozel-artopop-aile-figuru", "kisiye-ozel-kopek-figuru",
                                "kisiye-ozel-kedi-figuru", "kisiye-ozel-anime-karakter-figuru",
                                "samuray-bustu-figuru", "minecraft-warden-figuru"]},
            {"h2": "Nasıl ilerliyoruz?",
             "liste": SUREC},
        ],
        "sss": [
            ("Fotoğraftan figür yapmak için nasıl bir fotoğraf gerekiyor?",
             "Yüzün ya da vücudun net göründüğü bir fotoğraf yeterli. Birden fazla açı varsa "
             "benzerlik daha yüksek çıkıyor."),
            ("Figürler boyalı mı geliyor?",
             "Evet, figürleri elle boyayıp gönderiyoruz. Kendiniz boyamak isterseniz boyanmamış "
             "hâliyle de hazırlayabiliyoruz."),
            ("Figür yaptırmak ne kadar tutar?",
             f"Kişiye özel figürler yaklaşık {aralik('kisiye-ozel-figur')} arasında. En çok istenen "
             "20 cm elle boyalı kişi figürü bu aralığın ortasında kalıyor; boyasız gönderip boyaları "
             "kutuya eklediğimiz seçenek daha uygun. Fiyat boyuta, detaya ve boya işçiliğine göre "
             "değişiyor; kesin tutarı görseli gönderdiğinizde netleştiriyoruz."),
            ("Figürler kaç santim oluyor?",
             "Kişi figürlerini genelde 15-20 cm yapıyoruz; anahtarlık boyu 5-7 cm. 3 cm gibi çok "
             "küçük ve detaylı işler reçineyle basılıyor, o da maliyeti artırıyor."),
            SSS_ODEME,
            ("Anime ya da oyun karakteri figürü yapıyor musunuz?",
             "Evet. Katalogda anime tarzı, chibi tarzı ve oyun karakteri figürleri var. İnce detay "
             "gerektiği için bu figürleri genelde reçineyle basıyoruz."),
        ],
    },
    {
        "slug": "3d-baski-maket",
        "title": "3D Baskı Maket | Araba, Motosiklet ve Diorama | Ankara",
        "desc": "Fotoğraftan araba ve motosiklet maketi, plakası ve platformuyla; diorama ve araç "
                f"standı. Elle boyama, yaklaşık {aralik('araba-maketi')}. Türkiye geneli kargo.",
        "h1": "3D baskı maket: araba, motosiklet ve diorama",
        "lead": "Arabanızın ya da motosikletinizin fotoğrafından maketini modelliyor, basıyor ve "
                "elle boyuyoruz. Sahne kurgulu dioramalar ve isimli masaüstü araç standları da yapıyoruz.",
        "sema": "Service",
        "sema_ad": "3D baskı maket üretimi",
        "bolumler": [
            # Olgular: katalog kartlari ve Instagram mesajlari (08.10.2026): maketler
            # 20 cm, plaka ve platform dahil; mimari maket ve olcekli calisma YOK
            # (sahibin mesajlardaki cevabi: "mimari modeli calismiyorum",
            # "olcekli calismiyoruz, toplam uzunluk 20 santim").
            {"h2": "Ne tür maketler yapıyoruz?",
             "kartlar": [
                 ("Araba maketi",
                  "Aracın fotoğrafından modellenen, plakası ve platformuyla elle boyanmış araba "
                  'maketi. <a href="/etiket/araba-maketi/">Araba maketi örnekleri</a>.'),
                 ("Motosiklet maketi",
                  "El boyaması, gerçekçi detaylı motosiklet maketi; isterseniz sürücü figürüyle. "
                  '<a href="/etiket/motosiklet-maketi/">Motosiklet maketi örnekleri</a>.'),
                 ("Diorama",
                  "Sahne kurgulu, çok parçalı çalışmalar: kamp ateşi dioraması gibi birden çok "
                  "figürün bir sahnede durduğu işler."),
                 ("İsimli araç standı",
                  "İsim yazılı, masaüstünde duran araba figürü standı. Hediye olarak da isteniyor."),
             ]},
            {"h2": "Maket örneklerimiz",
             "urun_kartlari": ["cub-motosiklet-maketi", "renault-megane-araba-maketi",
                               "off-road-arazi-araci-maketi", "naked-motosiklet-maketi",
                               "cupra-araba-maketi-dioramali", "doc-hudson-araba-maketi",
                               "chopper-motosiklet-maketi", "kisiye-ozel-araba-standi"]},
            {"h2": "Nasıl ilerliyoruz?",
             "liste": SUREC},
            {"h2": "Hangi malzemeyle basıyoruz?",
             "p": ['Maketlerin çoğunda PLA kullanıyoruz: boyayı iyi tutuyor, renk seçeneği geniş. '
                   'Malzemeyi yine de işin gereğine göre seçiyoruz; seçenekler '
                   '<a href="/ankara-3d-baski/">Ankara 3D baskı sayfasında</a> yazılı.']},
            {"h2": "Yaklaşık fiyatlar",
             "p": [f"20 cm araba ve motosiklet maketi, plaka ve platform dahil, yaklaşık "
                   f"{aralik('motosiklet-maketi')} arasında. Modeli çok detaylı araçlarda ve "
                   "dioramalarda üst sınıra çıkıyor. Aşağıdakiler katalogdaki çalışmaların yaklaşık "
                   "fiyatları."],
             "fiyat_urunleri": ["cub-motosiklet-maketi", "renault-megane-araba-maketi",
                                "off-road-arazi-araci-maketi", "cupra-araba-maketi-dioramali",
                                "nostaljik-klasik-araba-maketi", "detayli-motosiklet-maketi",
                                "kisiye-ozel-araba-standi"]},
        ],
        "sss": [
            ("Kendi arabamın maketini yaptırabilir miyim?",
             "Evet. Aracınızın fotoğrafından modeli hazırlıyor, basıyor ve detaylı boyuyoruz. "
             "Önizlemeyi onayladıktan sonra üretime geçiyoruz."),
            ("Araba maketi ne kadar?",
             f"20 cm araba ve motosiklet maketi, plaka ve platform dahil, yaklaşık "
             f"{aralik('araba-maketi')} arasında; katalogdaki maketlerin yaklaşık fiyatları bu "
             "sayfadaki tabloda. Fiyat aracın detayına göre değişiyor."),
            ("Mimari ya da ölçekli maket yapıyor musunuz?",
             "Hayır. Mimari proje maketi yapmıyoruz, ölçekli (1/24, 1/50 gibi) de çalışmıyoruz. "
             "Araba ve motosiklet maketlerini toplam boyu genelde 20 cm olacak şekilde üretiyoruz."),
            ("Maket ne kadar sürede hazır olur?", SURE),
            SSS_ODEME,
            ("Elimde 3D model var, sadece baskı yaptırabilir miyim?",
             "Evet. Hazır modeliniz varsa doğrudan basıyoruz; yoksa modeli biz tasarlıyoruz."),
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
            {"h2": "Elinizde dosya varsa",
             "p": ['Modeliniz hazırsa modelleme gerekmez: <a href="/stl-dosyasi-bastirma/">STL ya da '
                   "3MF dosyanızı doğrudan basıyoruz</a>. Dosyanız yoksa modelin videosunu size "
                   "gönderiyor, onayınızdan sonra baskıya geçiyoruz."]},
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
                   'hediyesi olarak da veriliyor. <a href="/etiket/kendin-boya-seti/">Kendin boya '
                   "setlerimiz</a>."],
             "urun_kartlari": ["kendin-boya-unicorn-seti", "artopop-kendin-boya-kutusu",
                               "toplu-boyama-figuru"]},
            {"h2": "Kafede, okulda, kurumda atölye",
             "p": ["Atölyeyi yalnız doğum günlerinde değil kafelerde, AVM'lerde, okul ve kurum "
                   "etkinliklerinde de yapıyoruz. Daha önce Podium AVM Ancyra Kafe, Grande Oyun Sokağı, "
                   "Ümitköy ve Escape Garden'da atölyeler düzenledik; bir dönem Panora AVM'de hafta "
                   "sonları figür boyama atölyesi yaptık.",
                   "İsterseniz figürleri ve boyaları kutulayıp size gönderiyoruz, etkinliği kendiniz "
                   "yapıyorsunuz; isterseniz birlikte yapıyoruz. Toplu boyama figürünün adet fiyatı "
                   "kişi sayısına göre netleşiyor."]},
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

SAYFALAR += [
    {
        "slug": "stl-dosyasi-bastirma",
        "title": "STL Dosyası Bastırma | Ankara 3D Baskı Hizmeti | 3dartolyemiz",
        "desc": "Elinizdeki STL, 3MF ya da OBJ dosyasını Ankara'da basıyoruz; dosyanız yoksa modeli "
                "biz çıkarıyoruz. Fiyat ağırlığa göre, boyama ayrıca. Türkiye geneli kargo.",
        "h1": "STL dosyası bastırma",
        "lead": "Kendi 3D dosyanızı getirirseniz doğrudan basıyoruz. Getirmezseniz sorun değil: "
                "fotoğraftan ya da fikirden modeli biz çıkarıyoruz.",
        "sema": "Service",
        "sema_ad": "STL dosyasından 3D baskı",
        "bolumler": [
            {"h2": "Dosyanız varsa",
             "p": ["STL, 3MF ya da OBJ dosyanızı WhatsApp'tan gönderin; boyutu, rengi ve boyalı mı "
                   "olacağını yazın. Dosyayı kontrol edip fiyatı ve süreyi söylüyoruz.",
                   "Fiyat baskının ağırlığına göre: gram başına yaklaşık 2,5 – 5 TL. Boyama "
                   "isterseniz boyama ücreti ayrıca ekleniyor. Çok küçük ve ince detaylı parçaları "
                   "reçineyle basıyoruz, o da maliyeti artırıyor."]},
            {"h2": "Dosyanız yoksa",
             "p": ['Elinizde yalnız bir fotoğraf ya da fikir varsa <a href="/3d-modelleme/">modeli '
                   "biz çıkarıyoruz</a>. Modelin videosunu gönderiyoruz, onaylarsanız baskıya "
                   "geçiyoruz. Kişiye özel figürlerin, maketlerin ve anahtarlıkların çoğu böyle "
                   "üretiliyor."]},
            {"h2": "Malzeme",
             "p": ['Dekor ve hediyelikte PLA, dayanım isteyen parçalarda PETG, esnek parçalarda TPU, '
                   "ince detayda reçine. Hangi işte hangisi, "
                   '<a href="/ankara-3d-baski/">Ankara 3D baskı sayfasındaki tabloda</a>.']},
            {"h2": "Nasıl ilerliyoruz?", "liste": SUREC},
        ],
        "sss": [
            ("Hangi dosya biçimlerini basıyorsunuz?",
             "STL, 3MF ve OBJ. Dosyanızı gönderdiğinizde baskıya uygun mu diye kontrol ediyoruz."),
            ("STL baskı fiyatı nasıl hesaplanıyor?",
             "Baskının ağırlığına göre, gram başına yaklaşık 2,5 – 5 TL. Boyama ve reçine baskı "
             "ayrıca fiyatlanıyor; kesin tutarı dosyayı gördüğümüzde söylüyoruz."),
            ("Dosyam yok, ne yapmalıyım?",
             "Fotoğrafı ya da fikri gönderin, modeli biz çıkaralım. Modelin videosunu onayınıza sunuyoruz."),
            ("Teslimat ne kadar sürer?", SURE),
        ],
    },
    {
        "slug": "3d-yazici-egitimi",
        "title": "3D Yazıcı Eğitimi | Online ve Ankara'da Yüz Yüze | 3dartolyemiz",
        "desc": "3D yazıcı kullanımı, baskı ayarları, boyama teknikleri ve 3D baskıyla iş kurma "
                "eğitimi. Online ya da Ankara'da yüz yüze; saatlik yaklaşık 1.250 – 3.000 TL.",
        "h1": "3D yazıcı eğitimi",
        "lead": "Yazıcıyı aldınız ama verim alamıyor musunuz, ya da 3D baskıyla iş kurmak mı "
                "istiyorsunuz? Kendi atölyemizde her gün yaptığımız işi birebir anlatıyoruz.",
        "sema": "Service",
        "sema_ad": "3D yazıcı eğitimi",
        "bolumler": [
            {"h2": "Hangi eğitimleri veriyoruz?",
             "kartlar": [
                 ("Hobi kullanımı",
                  "Yazıcının kurulumu, dilimleme (slicer) ayarları, ilk baskılar ve sık görülen "
                  "baskı hataları. Genelde 1 saat yetiyor."),
                 ("Ticari kullanım",
                  "3D baskıyla iş kurmak isteyenler için: hangi ürünler satıyor, fiyatlandırma, "
                  "piyasanın dinamikleri ve iş fikirleri. Genelde 2 saat."),
                 ("Boyama teknikleri",
                  "Figür boyamada farklı teknikler, uygulamalı. Grup hâlinde 2-2,5 saat süren "
                  "bir organizasyon olarak da yapıyoruz."),
             ]},
            {"h2": "Online mı, yüz yüze mi?",
             "p": ["İkisi de olur. Online eğitimi görüntülü görüşmeyle, gerekirse bilgisayarınıza "
                   "bağlanıp ekran üzerinden yapıyoruz. Ankara'daysanız yüz yüze de çalışabiliyoruz.",
                   "Kurum ve şirketlere de eğitim veriyoruz; kişi sayısını ve konuyu yazın, programı "
                   "birlikte çıkaralım."]},
            {"h2": "Yaklaşık ücretler",
             "tablo": {"basliklar": ["Eğitim", "Yaklaşık ücret"],
                       "satirlar": [["Birebir eğitim, saatlik", "1.250 – 3.000 TL"],
                                    ["Boyama teknikleri, grup organizasyonu (2-2,5 saat)",
                                     "5.000 – 10.000 TL"]]}},
        ],
        "sss": [
            ("Eğitim kaç saat sürüyor?",
             "Hobi amaçlı kullanım için genelde 1 saat, ticari kullanım için 2 saat yetiyor."),
            ("Online eğitim nasıl oluyor?",
             "Görüntülü görüşmeyle; gerekirse bilgisayarınıza bağlanıp ayarları sizin ekranınızda "
             "birlikte yapıyoruz."),
            ("YouTube'dan izleyerek öğrenemez miyim?",
             "Temel kullanımı öğrenebilirsiniz; ama ayar, boyama ve satış tarafı uygulamayla oturuyor. "
             "Eğitimde kendi atölyemizde kullandığımız yöntemleri anlatıyoruz."),
        ],
    },
    {
        "slug": "3d-yazici-tamiri-ankara",
        "title": "3D Yazıcı Tamiri Ankara | Bakım ve Arıza | 3dartolyemiz",
        "desc": "Ankara içinde 3D yazıcı tamiri ve bakımı. Yazıcınızın modelini ve sorunu "
                "WhatsApp'tan yazın, ne yapılabileceğini ve ücretini konuşalım.",
        "h1": "Ankara'da 3D yazıcı tamiri",
        "lead": "Atölyemizde her gün birden fazla 3D yazıcıyla üretim yapıyoruz. Ankara içinde "
                "arızalı ya da verimsiz çalışan yazıcıların tamirini ve bakımını da üstleniyoruz.",
        "sema": "Service",
        "sema_ad": "3D yazıcı tamiri",
        "bolumler": [
            {"h2": "Nasıl ilerliyoruz?",
             "liste": [
                 "Yazıcınızın markasını, modelini ve sorunu WhatsApp'tan yazın; varsa fotoğraf ya da "
                 "kısa bir video ekleyin.",
                 "Sorunu dinleyip ne yapılabileceğini ve yaklaşık ücreti söylüyoruz.",
                 "Ankara içinde yazıcıya bakıyor, onarımı ya da bakımı yapıyoruz.",
             ]},
            {"h2": "Hangi sorunlar için?",
             "p": ["Baskının tablaya tutmaması, tıkanan nozül, filament beslemesinin takılması, "
                   "kalibrasyon ve baskı kalitesi sorunları gibi. Parça değişimi gerekiyorsa bunu "
                   "baştan söylüyoruz."]},
            {"h2": "Bize yazmadan önce deneyebilecekleriniz",
             "p": ["Sorunların bir kısmı ayarla çözülüyor. Tablayı sabunlu suyla ya da izopropil "
                   "alkolle temizlemek, filamenti kurutmak ve ilk katman yüksekliğini (Z ofset) "
                   "kontrol etmek tablaya tutmama ve ince tel sorunlarının çoğunu gideriyor. Sık "
                   "görülen on sorunu ve çözümlerini <a href=\"/blog/3d-baski-hatalari-ve-cozumleri/\">"
                   "baskı hataları rehberimizde</a> topladık.",
                   "Ayarlarla düzelmeyen, sürekli tekrarlayan ya da yazıcının hiç çalışmadığı "
                   "durumlarda sorun çoğu zaman donanımdadır: aşınmış nozul, arızalı fan, gevşemiş "
                   "kayış, bozuk sensör. Bu noktada yazıcıya bakmamız gerekiyor."]},
            {"h2": "Ücret",
             "p": ["Arızaya göre değişiyor; yazıcıyı ve sorunu görmeden kesin fiyat veremiyoruz. "
                   "Sorunu yazdığınızda yaklaşık bir tutar söylüyoruz."]},
            {"h2": "Tamirden sonra",
             "p": ["Yazıcınızı kendiniz daha verimli kullanmak isterseniz <a href=\"/3d-yazici-egitimi/\">"
                   "3D yazıcı eğitimi</a> de veriyoruz: dilimleme ayarları, bakım ve sık görülen "
                   "hatalar. Yeni bir yazıcı almayı düşünüyorsanız <a href=\"/blog/3d-yazici-alirken-dikkat/\">"
                   "3D yazıcı alırken dikkat edilmesi gerekenler</a> yazımız yol gösterir."]},
        ],
        "sss": [
            ("Ankara dışına tamir hizmeti veriyor musunuz?",
             "Tamir hizmetimiz Ankara içinde. Kullanım ve ayar sorunları için online eğitim "
             "verebiliyoruz."),
            ("Tamir ne kadar tutar?",
             "Arızaya ve parça gerekip gerekmediğine göre değişiyor. Sorunu yazdığınızda yaklaşık "
             "tutarı söylüyoruz."),
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


# Bing Site Scan ve Google sonuc sayfasi siniri: baslik 70, aciklama 160
# karakteri asarsa kesiliyor (08.10.2026 denetiminde 33 baslik, 65 aciklama
# asiyordu). Sinir burada DENETLENIR; asan sayfa derlemeyi durdurur.
BASLIK_SINIR = 70
ACIKLAMA_SINIR = (70, 160)


def ilk_sigan(adaylar: list, sinir: int) -> str:
    """Uzundan kisaya dizilmis adaylardan sinira ilk sigani."""
    for a in adaylar:
        if len(a) <= sinir:
            return a
    raise SystemExit(f"Hicbir aday {sinir} karaktere sigmiyor: {adaylar[-1]}")


def ld(bloklar) -> str:
    return "".join('\n  <script type="application/ld+json">\n'
                   + json.dumps(b, ensure_ascii=False, indent=2) + "\n  </script>" for b in bloklar) + "\n"


def head_yap(baslik: str, aciklama: str, url: str, bloklar=(),
             og_baslik: str | None = None, og_gorsel: str | None = None, og_tur: str = "website") -> str:
    """Ana sayfanin head'inden alt sayfa head'i: baslik, aciklama, canonical, OG ve sema."""
    if len(baslik) > BASLIK_SINIR:
        raise SystemExit(f"Baslik {len(baslik)} karakter (> {BASLIK_SINIR}): {baslik}")
    if not ACIKLAMA_SINIR[0] <= len(aciklama) <= ACIKLAMA_SINIR[1]:
        raise SystemExit(f"Aciklama {len(aciklama)} karakter {ACIKLAMA_SINIR}: {url}")
    og_baslik = og_baslik or baslik
    # Nitelik degerine cift tirnak girerse meta etiketi kirilir (babalar gunu
    # anahtarliginda aciklama 25 karaktere dusmustu).
    for deger in (baslik, aciklama, og_baslik):
        if '"' in deger or "<" in deger:
            raise SystemExit(f"Baslik/aciklamada cift tirnak ya da < var: {deger}")
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{baslik}</title>", h, count=1, flags=re.S)
    for alan in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        h = re.sub(rf'({alan} content=")[^"]*(")', lambda m: m.group(1) + aciklama + m.group(2), h, count=1)
    for alan in ['property="og:title"', 'name="twitter:title"']:
        h = re.sub(rf'({alan} content=")[^"]*(")', lambda m: m.group(1) + og_baslik + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:type" content=")[^"]*(")', lambda m: m.group(1) + og_tur + m.group(2), h, count=1)
    if og_gorsel:
        h = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                   lambda m: m.group(1) + ALAN + og_gorsel + m.group(2), h, count=1)
    h = h.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    # ana sayfanin semalari alt sayfaya tasinmasin
    h = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", h, flags=re.S)
    # Sema </head> ICINE girer: eskiden head kapandiktan sonra yaziliyordu ve
    # arkasindan basibos bir <body> geliyordu (26 sayfada gecersiz isaretleme).
    return h.replace("</head>", ld(bloklar) + "\n</head>", 1)


def head_uret(s: dict) -> str:
    return head_yap(s["title"], s["desc"], f"{ALAN}/{s['slug']}/", sema_bloklari(s))


def sema_bloklari(s: dict) -> list:
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
    return bloklar


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
    if b.get("urun_kartlari"):
        p.append('    <div class="product-grid">')
        p += [urun_karti(URUN[sl]) for sl in b["urun_kartlari"]]
        p.append("    </div>")
    if b.get("etiket_fiyatlari"):
        b = dict(b, tablo={"basliklar": ["Ürün türü", "Yaklaşık fiyat"], "satirlar": [
            [f'<a href="/etiket/{e}/">{ETIKET[e]["ad"]}</a>',
             aralik(e) + (" / adet" if e == "anahtarlik" else "")] for e in b["etiket_fiyatlari"]]})
    if b.get("fiyat_urunleri"):
        # Fiyat TEK kaynaktan (content/urunler.json); burada elle yazilmaz.
        b = dict(b, tablo={"basliklar": ["Çalışma", "Yaklaşık fiyat"], "satirlar": [
            [f'<a href="/urun/{sl}/">{URUN[sl]["ad"]}</a>', URUN[sl]["fiyat_metni"].replace("Yaklaşık ", "")]
            for sl in b["fiyat_urunleri"]]})
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
        <li><a href="/urun/">Ürün kataloğu ve yaklaşık fiyatlar</a></li>
      </ul>
    </div>
  </section>''')
    return "\n".join(parcalar) + "\n"


# --------------------------------------------------------------------- urun sayfalari
# Google kurali: urun zengin sonucu YALNIZCA tek urune odakli sayfada gecerli.
# Birden cok urunu listeleyen sayfada Product isaretlemesi "gecersiz oge" sayiliyor
# (Search Console bunu bildirdi). Bu yuzden her katalog urunu kendi sayfasini alir,
# ana sayfadaki ItemList ise ozet bicime duser: yalnizca @type, position ve url.

def urun_sayfasi(u: dict) -> str:
    url = f"{ALAN}/urun/{u['slug']}/"
    semalar = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": ALAN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ürünler", "item": ALAN + "/urun/"},
            {"@type": "ListItem", "position": 3, "name": u["ad"], "item": url}]},
        {"@context": "https://schema.org", "@type": "Product",
         "name": u["ad"], "description": u["aciklama"], "url": url,
         "image": ALAN + u["gorsel"], "category": u["kategori"],
         "brand": {"@type": "Brand", "name": "3dartolyemiz"},
         # 04.09 bildirimi "genel tanimlayici verilmemis" diyordu; marka vardi,
         # eksik olan urun tanimlayicisiydi. Slug urunun kendi kimligi.
         "sku": u["slug"],
         # Fiyat aralik oldugu icin Offer degil AggregateOffer (low/highPrice).
         "offers": {"@type": "AggregateOffer", "lowPrice": u["fiyat"][0],
                    "highPrice": u["fiyat"][1], "priceCurrency": "TRY", "offerCount": 1,
                    # 21.09.2026: Search Console iki raporda birden
                    # "availability alaninda gecersiz enum degeri" bildirdi.
                    # Onceki deger schema.org/MadeToOrder idi: schema.org'da
                    # gecerli ama Google'in DESTEKLEDIGI listede yok
                    # (InStock, BackOrder, PreOrder, OutOfStock, SoldOut...).
                    # InStock secildi: urun siparis edilebilir ve sayfa
                    # "3-7 is gunu icinde kargoya veriliyor" diyor. BackOrder
                    # ("stok bitti") durumu oldugundan kotu gosterirdi.
                    # Siparise gore uretim bilgisi sayfada GORUNUR kaliyor.
                    "availability": "https://schema.org/InStock",
                    "seller": {"@type": "Organization", "name": "3dartolyemiz"}}},
    ]
    fk = u["fiyat_metni"].replace("Yaklaşık ", "")
    baslik = ilk_sigan([f"{u['ad']} | Yaklaşık {fk} | 3dartolyemiz", f"{u['ad']} | Yaklaşık {fk}",
                        f"{u['ad']} | 3dartolyemiz", u["ad"]], BASLIK_SINIR)
    aciklama = ilk_sigan([
        f"{u['ad']}: {u['aciklama']} Fiyatı {u['fiyat_kucuk']}. Ankara'da üretim, Türkiye geneli kargo.",
        f"{u['ad']}: {u['aciklama']} Fiyatı {u['fiyat_kucuk']}.",
        f"{u['aciklama']} Fiyatı {u['fiyat_kucuk']}.",
        f"{u['ad']}, fiyatı {u['fiyat_kucuk']}. Ankara'da üretim, Türkiye geneli kargo."], ACIKLAMA_SINIR[1])
    h = head_yap(baslik, aciklama, url, semalar, og_baslik=u["ad"], og_gorsel=u["gorsel"])

    govde = (
        '<main id="main">\n'
        '  <section class="hero hero--sayfa">\n    <div class="container">\n'
        '      <nav class="kirinti" aria-label="Konum"><a href="/">Ana sayfa</a> <span>/</span> '
        '<a href="/urun/">Ürünler</a> <span>/</span> <span>' + u["ad"] + '</span></nav>\n'
        '      <h1>' + u["ad"] + '</h1>\n'
        '      <p class="lead">' + u["aciklama"] + '</p>\n'
        '    </div>\n  </section>\n\n'
        '  <section>\n    <div class="container">\n      <div class="urun-detay">\n'
        '        <img class="urun-gorsel" src="' + u["gorsel"] + '" alt="' + u["alt"] + '" '
        'width="900" height="1200" loading="eager" decoding="async">\n'
        '        <div class="urun-bilgi">\n'
        '          <span class="tag">' + u["kategori"] + '</span>\n'
        '          <div class="price-badge">' + u["fiyat_metni"] + '</div>\n'
        '          <span class="price-note">' + u["not"] + '</span>\n'
        '          <p>Ankara\'daki atölyemizde üretiliyor. Ankara içi elden teslim, Türkiye geneli '
        'kargo. Genellikle 3-7 gün içinde hazırlanıyor.</p>\n'
        '          <p>Aynı ürünü farklı ölçü, renk ya da kişiye özel detayla da yapabiliyoruz. '
        'Ne istediğinizi yazın, birlikte netleştirelim.</p>\n'
        '          <a class="btn btn-primary" href="' + u["wa"] + '" target="_blank" rel="noopener">'
        'WhatsApp\'tan sipariş ver</a>\n'
        '          <ul class="etiketler" aria-label="Etiketler">'
        + "".join(f'<li><a href="/etiket/{e}/">{ETIKET[e]["ad"]}</a></li>' for e in u["etiketler"])
        + '</ul>\n'
        '        </div>\n      </div>\n    </div>\n  </section>\n'
        # 21.09.2026: urun sayfalarinin ~230 kelimesi 21 urunde AYNIYDI
        # ve Google hicbirini dizine almadi. Ture ozgu uretim anlatimi +
        # SSS burada eklenir; olgular sitenin kendi sayfalarindan gelir.
        + urun_icerik(u) +
        '\n  <section class="section--alt">\n    <div class="container">\n'
        '      <div class="section-head reveal"><h2>Devamı</h2></div>\n'
        '      <ul class="sayfa-liste reveal">\n'
        + ('        <li><a href="/3d-baski-maket/">3D baskı maket: araba, motosiklet ve diorama</a></li>\n'
           if u["tur"] in ("maket", "set") or u["slug"] == "kisiye-ozel-araba-standi" else
           '        <li><a href="/kisiye-ozel-3d-figur/">Kişiye özel 3D figür yaptırma</a></li>\n') +
        '        <li><a href="/ankara-3d-baski/">Ankara\'da 3D baskı hizmeti</a></li>\n'
        '        <li><a href="/urun/">Tüm ürün kataloğu ve yaklaşık fiyatlar</a></li>\n'
        '      </ul>\n    </div>\n  </section>\n')
    return h + bas + govde + son


def urun_karti(u: dict) -> str:
    return (
        '        <div class="product-card reveal">\n'
        '          <div class="product-media">\n'
        '            <img src="' + u["kart_gorsel"] + '" alt="' + u["alt"] + '" width="450" '
        'height="600" loading="lazy" decoding="async">\n'
        '            <span class="tag">' + u["kategori"] + '</span>\n'
        '          </div>\n'
        '          <div class="product-body">\n'
        '            <h3><a href="/urun/' + u["slug"] + '/">' + u["ad"] + '</a></h3>\n'
        '            <p>' + u["aciklama"] + '</p>\n'
        '            <div class="price-badge">' + u["fiyat_metni"] + '</div>\n'
        '            <span class="price-note">' + u["not"] + '</span>\n'
        '          </div>\n'
        '        </div>')



def urun_dizini(urunler: list) -> str:
    """/urun/ liste sayfasi: 21 urun tek sayfada, her biri kendi sayfasina baglı.

    Eskiden /urun/ 403 donuyordu; urunlere yalnizca ana sayfadaki katalog
    izgarasindan tek baglanti gidiyordu ve urun kirintisinin "Ürünler" basamagi
    bir capaya (/#urunler) isaret ediyordu.
    """
    url = f"{ALAN}/urun/"
    semalar = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": ALAN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ürünler", "item": url}]},
        {"@context": "https://schema.org", "@type": "ItemList",
         "name": "3dartolyemiz ürün kataloğu", "url": url,
         "numberOfItems": len(urunler),
         "itemListElement": [
             {"@type": "ListItem", "position": i, "url": f"{ALAN}/urun/{u['slug']}/"}
             for i, u in enumerate(urunler, 1)]},
    ]
    baslik = f"3D Baskı Ürünleri ve Fiyatları | {len(urunler)} Çalışma | 3dartolyemiz"
    aciklama = (f"Ankara'da ürettiğimiz {len(urunler)} 3D baskı çalışması: figür, maket, anahtarlık, "
                "pasta süsü, boyama seti ve ev dekoru, yaklaşık fiyatlarıyla.")
    h = head_yap(baslik, aciklama, url, semalar, og_baslik=f"3D baskı ürünleri ({len(urunler)} çalışma)")


    # 08.10.2026: 149 urunun hepsi tek izgarada sayfayi 155 KB / 207 baglantiya
    # cikariyordu (Bing Site Scan siniri 125 KB). Liste etiket bazinda onizlemeye
    # dondu: her etiketten en fazla 4 kart + "tumu" baglantisi. Her urun en az
    # bir etiket sayfasinda tam listeleniyor (asagida denetlenir).
    eksik = [u["slug"] for u in urunler if not any(e in ETIKET for e in u["etiketler"])]
    if eksik:
        raise SystemExit(f"Etiketsiz urun /urun/ sayfasindan erisilemez: {eksik}")
    gosterilen, gruplar = set(), []
    for e in ETIKETLER:
        us = etiket_urunleri(e["slug"])
        sec = [u for u in us if u["slug"] not in gosterilen][:4]
        gosterilen |= {u["slug"] for u in sec}
        adet = " / adet" if e["slug"] == "anahtarlik" else ""
        gruplar.append(
            f'      <div class="section-head reveal katalog-grup"><h2>{e["ad"]}</h2>'
            f'<p>{len(us)} çalışma · yaklaşık {aralik(e["slug"])}{adet}</p></div>\n'
            '      <div class="product-grid">\n' + "\n".join(urun_karti(u) for u in sec) + '\n      </div>\n'
            f'      <p class="katalog-tumu"><a class="btn btn-secondary" href="/etiket/{e["slug"]}/">'
            f'Tümünü gör: {e["ad"]} ({len(us)})</a></p>')

    govde = (
        '<main id="main">\n'
        '  <section class="hero hero--sayfa">\n    <div class="container">\n'
        '      <nav class="kirinti" aria-label="Konum"><a href="/">Ana sayfa</a> <span>/</span> '
        '<span>Ürünler</span></nav>\n'
        '      <h1>3D baskı ürünleri ve fiyatları</h1>\n'
        '      <p class="lead">Ankara Yenimahalle\'deki atölyemizde ürettiğimiz '
        + str(len(urunler)) + ' çalışma. Hepsi siparişe göre üretiliyor; ölçü, renk ve '
        'kişiselleştirme isteğe göre değişebilir. Fiyatlar yaklaşıktır ve ürünün kendi '
        'sayfasında yazılı; kesin tutar ölçü ve detaya göre netleşir.</p>\n'
        '    </div>\n  </section>\n\n'
        '  <section>\n    <div class="container">\n'
        '      <div class="section-head reveal"><h2>En çok sorulanlar</h2></div>\n'
        + etiket_dugmeleri() + '\n'
        + "\n".join(gruplar) + '\n'
        '    </div>\n  </section>\n\n'
        # Eski magazanin 61 adresi buraya 301'leniyor ve o aramalarin hepsi
        # TEKIL urun aramasi ("ronaldo funko pop" 168 gosterim, konum 6-9;
        # "garfield figur"; "sanji figure"). Listede o urun yok; arayan kisi
        # bos donmesin diye siparise gore uretim burada soyleniyor. Yeni bir
        # iddia degil: urun sayfalari ve /kisiye-ozel-3d-figur/ zaten boyle diyor.
        '  <section>\n    <div class="container">\n'
        '      <div class="section-head reveal"><h2>Aradığınız ürün listede yok mu?</h2></div>\n'
        '      <p class="lead reveal">Listedeki çalışmalar atölyede ürettiklerimizden bir '
        'seçki; üretebildiklerimizin tamamı değil. İstediğiniz figürü, maketi ya da '
        'hediyeliği de yapıyoruz: elinizde hazır bir model varsa basıyoruz, yoksa '
        'fotoğraftan veya tarifinizden sıfırdan tasarlıyoruz. Ölçü, renk ve fiyatı '
        'yazışırken netleştiriyoruz.</p>\n'
        '      <div class="hero-ctas reveal"><a class="btn btn-primary" href="' + TEL + '" '
        'target="_blank" rel="noopener">Ne istediğinizi WhatsApp\'tan yazın</a></div>\n'
        '    </div>\n  </section>\n\n'
        '  <section class="section--alt">\n    <div class="container">\n'
        '      <div class="section-head reveal"><h2>Hizmetler</h2></div>\n'
        '      <ul class="sayfa-liste reveal">\n'
        '        <li><a href="/ankara-3d-baski/">Ankara\'da 3D baskı hizmeti</a></li>\n'
        '        <li><a href="/kisiye-ozel-3d-figur/">Kişiye özel 3D figür</a></li>\n'
        '        <li><a href="/3d-baski-maket/">3D baskı maket</a></li>\n'
        '        <li><a href="/3d-modelleme/">3D modelleme</a></li>\n'
        '        <li><a href="/dogum-gunu-boyama-atolyesi/">Doğum günü boyama atölyesi</a></li>\n'
        '        <li><a href="/stl-dosyasi-bastirma/">STL dosyası bastırma</a></li>\n'
        '        <li><a href="/3d-yazici-egitimi/">3D yazıcı eğitimi</a></li>\n'
        '        <li><a href="/3d-yazici-tamiri-ankara/">Ankara\'da 3D yazıcı tamiri</a></li>\n'
        '      </ul>\n    </div>\n  </section>\n')
    return h + bas + govde + son


OK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def etiket_dugmeleri(aktif: str | None = None) -> str:
    """En cok sorulan urun turleri; sira content/etiketler.json'daki sira (Instagram
    mesajlarinda en cok sorulandan aza: 08.10.2026 olcumu)."""
    return ('      <ul class="etiketler">'
            + "".join(f'<li><a href="/etiket/{e["slug"]}/"'
                      + (' aria-current="page"' if e["slug"] == aktif else "")
                      + f'>{e["ad"]}<small>{len(etiket_urunleri(e["slug"]))}</small></a></li>'
                      for e in ETIKETLER) + "</ul>")


def etiket_sayfasi(e: dict) -> str:
    url = f"{ALAN}/etiket/{e['slug']}/"
    us = etiket_urunleri(e["slug"])
    semalar = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": ALAN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ürünler", "item": ALAN + "/urun/"},
            {"@type": "ListItem", "position": 3, "name": e["ad"], "item": url}]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": e["h1"], "url": url,
         "numberOfItems": len(us),
         "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{ALAN}/urun/{u['slug']}/"}
                             for i, u in enumerate(us, 1)]},
    ]
    fiyat = aralik(e["slug"]) + (" / adet" if e["slug"] == "anahtarlik" else "")
    baslik = ilk_sigan([f"{e['ad']} | {len(us)} Model, Yaklaşık {fiyat} | 3dartolyemiz",
                        f"{e['ad']} | {len(us)} Model, Yaklaşık {fiyat}",
                        f"{e['ad']} | {len(us)} Model ve Fiyatları | Ankara",
                        f"{e['ad']} Modelleri ve Fiyatları"], BASLIK_SINIR)
    ilk_cumle = e["giris"].split(". ")[0].rstrip(".") + "."
    aciklama = ilk_sigan([f"{e['giris']} Yaklaşık {fiyat}.", f"{ilk_cumle} {len(us)} model, yaklaşık {fiyat}.",
                          f"{e['ad']}: {len(us)} model, yaklaşık {fiyat}. Ankara'da üretim, Türkiye geneli kargo."],
                         ACIKLAMA_SINIR[1])
    h = head_yap(baslik, aciklama, url, semalar, og_baslik=e["h1"], og_gorsel=us[0]["gorsel"])
    hizmet = DIGER_AD.get(e["hizmet"].strip("/"), "Ankara'da 3D baskı hizmeti")
    govde = (
        '<main id="main">\n'
        '  <section class="hero hero--sayfa">\n    <div class="container">\n'
        '      <nav class="kirinti" aria-label="Konum"><a href="/">Ana sayfa</a> <span>/</span> '
        '<a href="/urun/">Ürünler</a> <span>/</span> <span>' + e["ad"] + '</span></nav>\n'
        '      <h1>' + e["h1"] + '</h1>\n'
        '      <p class="lead">' + e["giris"] + '</p>\n'
        '      <p class="lead">' + str(len(us)) + ' çalışma · yaklaşık ' + fiyat
        + '. Fiyatlar yaklaşıktır; kesin tutar ölçü ve detaya göre netleşir.</p>\n'
        '      <div class="hero-ctas"><a class="btn btn-primary" href="' + TEL + '" target="_blank" '
        'rel="noopener">WhatsApp\'tan yaz</a></div>\n'
        '    </div>\n  </section>\n\n'
        '  <section>\n    <div class="container">\n'
        + etiket_dugmeleri(e["slug"]) + '\n'
        '      <div class="product-grid">\n' + "\n".join(urun_karti(u) for u in us) + '\n      </div>\n'
        '    </div>\n  </section>\n\n'
        '  <section class="section--alt">\n    <div class="container">\n'
        '      <div class="section-head reveal"><h2>Aradığınız model yok mu?</h2></div>\n'
        '      <p class="sayfa-metin reveal">Buradakiler atölyede ürettiklerimizden bir seçki. '
        'İstediğiniz modelin görselini gönderin; dosyası varsa basıyoruz, yoksa modelliyoruz.</p>\n'
        '      <ul class="sayfa-liste reveal">\n'
        f'        <li><a href="{e["hizmet"]}">{hizmet}</a></li>\n'
        '        <li><a href="/urun/">Tüm ürün kataloğu ve yaklaşık fiyatlar</a></li>\n'
        '      </ul>\n    </div>\n  </section>\n')
    return h + bas + govde + son


# Ana sayfa SSS: gorunur metin ve FAQPage semasi AYNI listeden uretilir.
ANASAYFA_SSS = [
    ("Teslimat ne kadar sürer?", SURE),
    ("Şehir dışına gönderim yapıyor musunuz?",
     "Evet, Türkiye'nin her yerine güvenli kargo ile gönderim yapıyoruz. Ankara içinde elden de teslim ediyoruz."),
    ("Nasıl sipariş verebilirim?",
     "WhatsApp'tan görseli ya da fikrinizi gönderin. Modelleme bitince videosunu atıyoruz; onaylarsanız "
     "kapora alıp baskıya geçiyoruz. Ürün bitince yine video atıyor, kalan tutardan sonra gönderiyoruz."),
    ("Sitedeki fiyatlar kesin mi?",
     "Hayır, yaklaşıktır ve aralık olarak yazılı. Boy, detay ve boya işçiliği tutarın aralığın neresinde "
     "olacağını belirliyor. Kesin fiyatı görseli WhatsApp'tan gönderdiğinizde netleştiriyoruz."),
    ("Kendi STL dosyamı bastırabilir miyim?",
     "Evet. STL, 3MF ya da OBJ dosyanızı getirirseniz doğrudan basıyoruz; dosyanız yoksa modeli biz çıkarıyoruz."),
    ("Mimari ya da ölçekli maket yapıyor musunuz?",
     "Hayır. Mimari proje maketi yapmıyoruz, ölçekli de çalışmıyoruz. Araba ve motosiklet maketlerini "
     "genelde 20 cm boyunda, plaka ve platformuyla üretiyoruz."),
    ("Taksit imkânı var mı?",
     "Hayır, taksit imkânımız yok. Ödeme kapora ve kalan tutar olarak iki parçada alınıyor."),
    ("Doğum günü etkinliği hangi yaş grubuna uygun?",
     "Boyama atölyemiz genellikle 5-12 yaş arası çocuklar için idealdir, farklı yaş gruplarına göre de "
     "uyarlayabiliyoruz."),
]
OK_OK = ('<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>')


def isaret_doldur(metin: str, ad: str, icerik: str) -> str:
    bas, son = f"<!-- {ad} -->", f"<!-- /{ad} -->"
    i, j = metin.index(bas) + len(bas), metin.index(son)
    return metin[:i] + "\n" + icerik + "\n" + metin[j:]


def anasayfa_guncelle() -> None:
    """index.html'in uretilen alanlari: one cikan urunler, etiket dugmeleri, SSS,
    kategori kartlarindaki fiyat araliklari ve JSON-LD (LocalBusiness, FAQPage, ItemList)."""
    yol = KOK / "index.html"
    metin = io.open(yol, encoding="utf-8").read()
    one = [u for u in URUNLER if u["one_cikan"]]
    katalog = (etiket_dugmeleri() + '\n      <div class="product-grid">\n'
               + "\n".join(urun_karti(u) for u in one) + '\n      </div>\n'
               f'      <p class="katalog-tumu"><a class="btn btn-secondary" href="/urun/">Tüm {len(URUNLER)} '
               'ürünü ve fiyatlarını gör</a></p>')
    metin = isaret_doldur(metin, "KATALOG", katalog)
    sss = ('      <div class="faq reveal">\n'
           + "\n".join(f'        <details class="faq-item">\n          <summary>{q}{OK_OK}</summary>\n'
                       f'          <p>{c}</p>\n        </details>' for q, c in ANASAYFA_SSS)
           + '\n      </div>')
    metin = isaret_doldur(metin, "SSS", sss)
    metin = re.sub(r'(<div class="price-badge" data-etiket="([\w-]+)">)[^<]*(</div>)',
                   lambda m: m.group(1) + "Yaklaşık " + aralik(m.group(2))
                   + (" / adet" if m.group(2) == "anahtarlik" else "") + m.group(3), metin)

    fiyatlar = [u["fiyat"] for u in URUNLER if not u["adet"]]
    for b in reversed(list(re.finditer(r'(<script[^>]+ld\+json[^>]*>)(.*?)(</script>)', metin, re.S))):
        veri = json.loads(b.group(2))
        tur = veri.get("@type")
        if tur == "ItemList":
            veri["itemListElement"] = [{"@type": "ListItem", "position": i, "url": f"{ALAN}/urun/{u['slug']}/"}
                                       for i, u in enumerate(one, 1)]
            veri["numberOfItems"] = len(one)
        elif tur == "FAQPage":
            veri["mainEntity"] = [{"@type": "Question", "name": q,
                                   "acceptedAnswer": {"@type": "Answer", "text": c}} for q, c in ANASAYFA_SSS]
        elif tur == "LocalBusiness":
            veri["priceRange"] = (f"Yaklaşık {tl(min(f[0] for f in fiyatlar))} – "
                                  f"{tl(max(f[1] for f in fiyatlar))} TL")
            hizmet = {
                "Araba ve Motosiklet Maketi": (
                    "Fotoğraftan modellenen, plakası ve platformuyla elle boyanmış 20 cm araba veya "
                    f"motosiklet maketi. Yaklaşık {aralik('araba-maketi')}.", "/3d-baski-maket/"),
                "Kişiye Özel 3D Figür": (
                    "Kişi, aile, evcil hayvan veya karakter fotoğrafından modellenip elle boyanan figür. "
                    f"Yaklaşık {aralik('kisiye-ozel-figur')}.", "/kisiye-ozel-3d-figur/"),
                "Eğitim ve Atölye": (
                    "3D yazıcı kullanımı, baskı ayarları, boyama teknikleri ve 3D baskıyla iş kurma "
                    "eğitimi; online ya da Ankara'da yüz yüze. Çocuklar için boyama atölyesi.",
                    "/3d-yazici-egitimi/"),
                "3D Yazıcı Tamiri": (
                    "Ankara içinde 3D yazıcı tamiri ve bakımı.", "/3d-yazici-tamiri-ankara/"),
                "STL Dosyasından Baskı": (
                    "STL, 3MF ya da OBJ dosyasından baskı; dosya yoksa modelleme.", "/stl-dosyasi-bastirma/"),
            }
            mevcut = {o["itemOffered"]["name"]: o for o in veri["hasOfferCatalog"]["itemListElement"]}
            for ad, (aciklama, yol_) in hizmet.items():
                o = mevcut.get(ad) or {"@type": "Offer", "itemOffered": {
                    "@type": "Service", "name": ad, "areaServed": {"@type": "City", "name": "Ankara"}}}
                o["itemOffered"]["description"] = aciklama
                o["itemOffered"]["url"] = ALAN + yol_
                if ad not in mevcut:
                    veri["hasOfferCatalog"]["itemListElement"].append(o)
            for k in ("3D yazıcı eğitimi", "3D yazıcı tamiri", "STL dosyası baskısı", "anahtarlık",
                      "pasta süsü", "evcil hayvan figürü"):
                if k not in veri["knowsAbout"]:
                    veri["knowsAbout"].append(k)
        else:
            continue
        metin = metin[:b.start(2)] + "\n" + json.dumps(veri, ensure_ascii=False, indent=2) + "\n  " + metin[b.end(2):]
    io.open(yol, "w", encoding="utf-8").write(metin)


def nginx_yonlendirmeleri() -> int:
    """Eski WooCommerce adreslerini urunun kendi sayfasina 301'ler (urunler.json 'eski').
    Eslesmeyenler nginx.conf'taki genel /magaza/ -> /urun/ kuralina duser."""
    yol = KOK / "nginx.conf"
    metin = io.open(yol, encoding="utf-8").read()
    satirlar = [f"    location = {e} {{ return 301 /urun/{u['slug']}/; }}"
                for u in URUNLER for e in u["eski"]]
    bas, son = "    # URUN-YONLENDIRMELERI (scripts/sayfa-uret.py uretir, elle duzenleme)", "    # /URUN-YONLENDIRMELERI"
    if bas not in metin:
        a = "    location ^~ /magaza/oyun-oyuncu/anahtarlik/"
        metin = metin.replace(a, bas + "\n" + son + "\n" + a, 1)
    i, j = metin.index(bas) + len(bas), metin.index(son)
    metin = metin[:i] + "\n" + "\n".join(satirlar) + "\n" + metin[j:]
    io.open(yol, "w", encoding="utf-8").write(metin)
    return len(satirlar)


def gizlilik_sayfasi() -> str:
    """KVKK aydinlatma ve gizlilik metni.

    Icerik OLCUME dayali (21.09.2026): sitede form yok, cerez kullanilmiyor,
    ucuncu taraf betik yok. Metin yalnizca bunu soyluyor; saklama suresi gibi
    bilinmeyen hicbir sey yazilmiyor. Iletisim WhatsApp uzerinden yurudugu
    icin o kanaldaki veri ayrica anlatiliyor.
    """
    url = f"{ALAN}/gizlilik/"
    baslik = "Gizlilik ve KVKK Aydınlatma Metni | 3dartolyemiz"
    aciklama = ("3dartolyemiz sitesi hangi verileri işler: sitede form ve çerez "
                "yok; iletişim WhatsApp üzerinden yürür.")
    h = head_yap(baslik, aciklama, url, og_baslik="Gizlilik ve KVKK")

    govde = """<main id="main">
  <section class="hero hero--sayfa">
    <div class="container">
      <nav class="kirinti" aria-label="Konum"><a href="/">Ana sayfa</a> <span>/</span> <span>Gizlilik ve KVKK</span></nav>
      <h1>Gizlilik ve KVKK aydınlatma metni</h1>
      <p class="lead">Bu sitede hangi verilerin işlendiği aşağıda açıkça yazılıdır.</p>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="sayfa-metin">
        <h2>Sitede veri toplanmıyor</h2>
        <p>artolyemiz.com statik bir tanıtım sitesidir. Sitede <strong>form yoktur</strong>,
           üyelik alınmaz ve ziyaretiniz sırasında <strong>çerez kullanılmaz</strong>.
           Sayfalarda üçüncü taraf ölçümleme veya reklam betiği çalışmaz; yüklenen
           bütün dosyalar sitenin kendi alan adından gelir.</p>

        <h2>Sunucu kayıtları</h2>
        <p>Her web sitesinde olduğu gibi, sayfayı açtığınızda sunucu tarafında teknik
           kayıt (IP adresi, tarih, istenen adres, tarayıcı bilgisi) oluşur. Bu kayıtlar
           sitenin çalışmasını sürdürmek ve kötüye kullanımı engellemek için tutulur;
           pazarlama amacıyla kullanılmaz ve üçüncü kişilerle paylaşılmaz.</p>

        <h2>WhatsApp üzerinden iletişim</h2>
        <p>Sipariş ve fiyat görüşmeleri WhatsApp üzerinden yürür. Bize yazdığınızda
           ilettiğiniz bilgiler (adınız, telefon numaranız, gönderdiğiniz görseller ve
           sipariş ayrıntıları) yalnızca talebinizi karşılamak için kullanılır. Bu
           yazışma WhatsApp'ın kendi altyapısında gerçekleşir ve WhatsApp'ın kendi
           gizlilik koşullarına tabidir.</p>

        <h2>Haklarınız</h2>
        <p>6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında; işlenen
           verileriniz hakkında bilgi talep etme, düzeltilmesini veya silinmesini
           isteme haklarınız vardır. Bu talepleriniz için sayfanın altındaki
           iletişim kanalından bize ulaşabilirsiniz.</p>

        <h2>Değişiklikler</h2>
        <p>Sitede çerez kullanımı, form ya da reklam gibi bir değişiklik olursa bu
           metin güncellenir.</p>
      </div>
    </div>
  </section>

  <section class="section--alt">
    <div class="container">
      <div class="section-head reveal"><h2>Devamı</h2></div>
      <ul class="sayfa-liste reveal">
        <li><a href="/urun/">Tüm ürün kataloğu ve fiyatlar</a></li>
        <li><a href="/ankara-3d-baski/">Ankara'da 3D baskı hizmeti</a></li>
      </ul>
    </div>
  </section>
"""
    return h + bas + govde + son


# --------------------------------------------------------------------- yaz

uretilen = []
for s in SAYFALAR:
    hedef = KOK / s["slug"]
    hedef.mkdir(exist_ok=True)
    icerik = head_uret(s) + bas + govde_uret(s) + son
    io.open(hedef / "index.html", "w", encoding="utf-8").write(icerik)
    uretilen.append(s["slug"])
    print(f"  yazildi: /{s['slug']}/  ({len(icerik)} bayt)")

(KOK / "gizlilik").mkdir(exist_ok=True)
io.open(KOK / "gizlilik" / "index.html", "w", encoding="utf-8").write(gizlilik_sayfasi())
print("  yazildi: /gizlilik/")

for u in URUNLER:
    hedef = KOK / "urun" / u["slug"]
    hedef.mkdir(parents=True, exist_ok=True)
    io.open(hedef / "index.html", "w", encoding="utf-8").write(urun_sayfasi(u))
(KOK / "urun").mkdir(exist_ok=True)
io.open(KOK / "urun" / "index.html", "w", encoding="utf-8").write(urun_dizini(URUNLER))
print(f"  {len(URUNLER)} urun sayfasi + /urun/ liste sayfasi uretildi")
for e in ETIKETLER:
    if not etiket_urunleri(e["slug"]):
        raise SystemExit(f"Etiket bos: {e['slug']}")
    hedef = KOK / "etiket" / e["slug"]
    hedef.mkdir(parents=True, exist_ok=True)
    io.open(hedef / "index.html", "w", encoding="utf-8").write(etiket_sayfasi(e))
print(f"  {len(ETIKETLER)} etiket sayfasi uretildi")
anasayfa_guncelle()
print("  ana sayfa: one cikanlar, etiketler, SSS, fiyat araliklari, JSON-LD guncellendi")
print(f"  nginx.conf: {nginx_yonlendirmeleri()} eski magaza adresi urun sayfasina yonlendirildi")

# blog ve atolye (scripts/blog.py)
BAGLAM = {"ALAN": ALAN, "TEL": TEL, "URUN": URUN, "aralik": aralik, "SURE": SURE, "SUREC": SUREC,
          "head_yap": head_yap, "bas": bas, "son": son}
blog.hazirla(BAGLAM)
for y in blog.YAZILAR:
    hedef = KOK / "blog" / y["slug"]
    hedef.mkdir(parents=True, exist_ok=True)
    io.open(hedef / "index.html", "w", encoding="utf-8").write(blog.yazi_sayfasi(y, BAGLAM))
io.open(KOK / "blog" / "index.html", "w", encoding="utf-8").write(blog.blog_dizini(BAGLAM))
io.open(KOK / "blog" / "rss.xml", "w", encoding="utf-8").write(blog.rss(BAGLAM))
(KOK / "atolyemiz").mkdir(exist_ok=True)
io.open(KOK / "atolyemiz" / "index.html", "w", encoding="utf-8").write(blog.atolye_sayfasi(BAGLAM))
ana = io.open(KOK / "index.html", encoding="utf-8").read()
ana = isaret_doldur(ana, "BLOG", '      <div class="blog-grid">\n'
                    + "\n".join(blog.yazi_karti(y) for y in blog.YAZILAR[:3]) + "\n      </div>")


def vitrin_seridi(us: list, ters: bool) -> str:
    """Kayan serit: urunler iki kez yazilir (sonsuz dongu); ikinci kopya ekran okuyucudan gizli."""
    def kart(u, kopya):
        ek = ' class="kopya" aria-hidden="true" tabindex="-1"' if kopya else ""
        return (f'<a href="/urun/{u["slug"]}/"{ek}><img src="{u["kart_gorsel"]}" alt="{"" if kopya else u["alt"]}" '
                f'width="450" height="600" loading="lazy" decoding="async"><span>{u["ad"]}</span></a>')
    return (f'    <div class="vitrin-serit{" vitrin-serit--ters" if ters else ""}">'
            + "".join(kart(u, False) for u in us) + "".join(kart(u, True) for u in us) + "</div>")


# en yeni 32 urun (urunler.json'a sona eklenir) iki serit hâlinde
yeniler = URUNLER[-32:][::-1]
ana = isaret_doldur(ana, "VITRIN", vitrin_seridi(yeniler[:16], False) + "\n" + vitrin_seridi(yeniler[16:], True))
io.open(KOK / "index.html", "w", encoding="utf-8").write(ana)
print(f"  {len(blog.YAZILAR)} blog yazisi + /blog/ + /atolyemiz/ uretildi")

# sitemap
girdiler = [f"  <url>\n    <loc>{ALAN}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>"]
girdiler += [f"  <url>\n    <loc>{ALAN}/{sl}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
             for sl in uretilen]
girdiler.append(f"  <url>\n    <loc>{ALAN}/gizlilik/</loc>\n    <changefreq>yearly</changefreq>\n    <priority>0.2</priority>\n  </url>")
girdiler.append(f"  <url>\n    <loc>{ALAN}/atolyemiz/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>")
girdiler.append(f"  <url>\n    <loc>{ALAN}/blog/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>")
girdiler += [f"  <url>\n    <loc>{ALAN}/blog/{y['slug']}/</loc>\n    <lastmod>{y.get('guncelleme', y['tarih'])}</lastmod>\n    <priority>0.7</priority>\n  </url>"
             for y in blog.YAZILAR]
girdiler.append(f"  <url>\n    <loc>{ALAN}/urun/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>")
girdiler += [f"  <url>\n    <loc>{ALAN}/etiket/{e['slug']}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
             for e in ETIKETLER]
girdiler += [f"  <url>\n    <loc>{ALAN}/urun/{u['slug']}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
             for u in URUNLER]
io.open(KOK / "sitemap.xml", "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(girdiler) + "\n</urlset>\n")
print(f"  sitemap.xml: {len(girdiler)} adres")


def llms_uret() -> str:
    """llms.txt: yapay zeka asistanlarinin (GEO) okudugu ozet. Elle yazilmaz;
    fiyat ve sayfa listesi sitenin kendi kaynagindan uretilir ki sayfalarla
    celismesin. Burada yazan her olgu sitede gorunur."""
    s = {x["slug"]: x for x in SAYFALAR}
    satir = [
        "# 3dartolyemiz — Ankara'da 3D baskı atölyesi (artolyemiz.com)",
        "",
        "Ankara Yenimahalle'de kendi atölyesinde 3D baskı yapan küçük işletme: fotoğraftan "
        "kişiye özel figür, araba ve motosiklet maketi, evcil hayvan figürü, anahtarlık ve "
        "toplu anahtarlık, pasta süsü, kendin boya setleri, ev dekoru, 3D modelleme, STL "
        "dosyasından baskı, 3D yazıcı eğitimi, Ankara içi 3D yazıcı tamiri ve çocuklar için "
        "boyama atölyesi. Ürünler siparişe göre üretilir; Ankara içi elden teslim, Türkiye "
        "geneli kargo. " + SURE,
        "",
        "## İletişim ve konum",
        "- Adres: Mehmet Akif Ersoy Mahallesi 266. Cad No:4, Yenimahalle, Ankara",
        "- Telefon / WhatsApp: 0544 188 57 44",
        "- Instagram: https://www.instagram.com/3dartolyemiz/",
        "",
        "## Hizmetler",
    ]
    for sl, x in s.items():
        satir.append(f"- [{x['h1']}]({ALAN}/{sl}/): {x['desc']}")
    satir += ["", "## Yaklaşık fiyatlar",
              "Sitedeki tüm fiyatlar yaklaşıktır; ölçü, detay ve boyaya göre değişir. Kesin fiyat "
              "WhatsApp'tan görsel gönderilerek netleşir.",
              *[f"- {e['ad']}: yaklaşık {aralik(e['slug'])}"
                + (" (adet başına)" if e["slug"] == "anahtarlik" else "") + f" — {ALAN}/etiket/{e['slug']}/"
                for e in ETIKETLER],
              "- STL dosyasından baskı: gram başına yaklaşık 2,5 – 5 TL, boyama ayrıca",
              "- 3D yazıcı eğitimi: saatlik yaklaşık 1.250 – 3.000 TL",
              "",
              "## Sipariş süreci",
              *[f"- {x}" for x in SUREC],
              "- Taksit yok; ödeme kapora ve kalan tutar olarak iki parça.",
              "",
              f"## Ürün kataloğu ({len(URUNLER)} çalışma)",
              f"- Liste: {ALAN}/urun/"]
    satir += [f"- [{u['ad']}]({ALAN}/urun/{u['slug']}/): {u['aciklama']} {u['fiyat_metni']}."
              for u in URUNLER]
    satir += ["", "## Atölye ve blog",
              f"- [Atölyemiz: yazıcılarımız ve üretimden videolar]({ALAN}/atolyemiz/)",
              f"- [Blog: 3D baskı rehberleri]({ALAN}/blog/)"]
    satir += [f"- [{y['h1']}]({ALAN}/blog/{y['slug']}/): {y['aciklama']}" for y in blog.YAZILAR]
    satir += ["", "## Sık sorulanlar"]
    for x in SAYFALAR:
        for q, c in x.get("sss", []):
            satir.append(f"- {q} {c}")
    satir += ["", "## Notlar",
              "- Malzeme işin gereğine göre seçilir: ince detayda SLA reçine, dekor/hediyelik/maketin "
              "çoğunda PLA, dayanımda PETG, esnek parçada TPU.",
              "- Mimari proje maketi yapılmaz, ölçekli çalışılmaz; araç maketleri genelde 20 cm.",
              "- Ana sayfadaki sayılar (9.000+ basılan parça, 790+ müşteri, 410+ modelleme, 340+ figür) "
              "yaklaşıktır: Instagram mesajlarından ölçülen siparişlerin, telefonla alınan işler için "
              "işletme sahibinin beyanıyla iki katı. Puan ve yorum sayısı yayımlanmaz.", ""]
    return "\n".join(satir)


io.open(KOK / "llms.txt", "w", encoding="utf-8").write(llms_uret())
print("  llms.txt yazildi")
print(f"{len(uretilen)} hizmet sayfasi + {len(URUNLER)} urun sayfasi uretildi.")
