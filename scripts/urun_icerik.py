# -*- coding: utf-8 -*-
"""Ürün sayfalarına türe özgü üretim anlatımı ve SSS üretir.

NEDEN VAR: 21.09.2026'da ölçüldü — her ürün sayfasında benzersiz metin yalnızca
ürün adı, tek satır açıklama ve fiyattı; kalan ~230 kelime 21 ürünün hepsinde
harfi harfine AYNIYDI. Google ürün sayfalarının hiçbirini dizine almadı, URL
İnceleme API'si "URL Google tarafından bilinmiyor" dedi. Bu modül sayfaları
birbirinden ayırır.

KURAL — UYDURMA ÖZELLİK YOK. Buradaki her olgu sitenin kendi yayımladığı
metinden gelir:

* `/ankara-3d-baski/` malzeme tablosu:
  "İnce detay: yüz hatları, küçük parçalar, büst → SLA reçine",
  "Dekor, hediyelik, maket; boyanacak yüzey → PLA",
  "Darbeye ve sıcağa dayanım → PETG", "Bükülüp eski hâline dönmesi gereken
  parça → TPU" ve "Malzemeyi işin gereğine göre seçiyoruz".
* `/kisiye-ozel-3d-figur/`: "Karakter ve oyun figürü … İnce detay gerektiği için
  genelde reçineyle basıyoruz", "Evcil hayvan figürü … tüy rengine kadar
  boyanmış figür", "Chihuahua ve Fransız bulldog gibi çalışmalarımız galeride
  duruyor", "ARTOPOP aile figürleri", "Diorama ve set … kamp ateşi dioraması ya
  da mini figür setleri gibi" ve sayfanın SSS cevapları.
* `/3d-modelleme/`: "Ölçüden — belirli bir yere oturması gereken parçalarda
  ölçüyü alıp modeli ona göre kuruyoruz."
* Ürünün kendi katalog kartı: adı, etiketi, açıklaması, fiyatı.

Ölçü, ağırlık, katman kalınlığı, malzeme garantisi gibi BİLİNMEYEN hiçbir şey
yazılmadı. Malzeme, spesifikasyon olarak değil atölyenin kendi ifadesiyle
("bu tür işlerde genellikle şunu kullanıyoruz") ve kaynak sayfaya bağlanarak
veriliyor.
"""

# Ürünün hangi tür iş olduğu. Katalogdaki ad, etiket ve açıklamadan okunur;
# eşleştirme elle yapıldı çünkü tür metnin kendisinde her zaman yazılı değil
# (ör. "Sprinku Figürü" koleksiyon figürü, "Kişiye Özel Araba Standı" isimli
# hediyelik). Tanınmayan slug derlemeyi durdurur.
URUN_TURU = {
    "samuray-bustu-figuru": "karakter",
    "mirabel-figuru-encanto": "karakter",
    "sprinku-figuru": "karakter",
    "masa-ile-koca-ayi-figuru": "karakter",
    "kratos-chibi-figuru": "karakter",
    "kisiye-ozel-anime-karakter-figuru": "karakter",
    "minecraft-warden-figuru": "karakter",
    "detayli-motosiklet-maketi": "maket",
    "honda-civic-araba-maketi": "maket",
    "galatasaray-hagi-forma-cercevesi": "dekor",
    "agac-dalli-ayna-cercevesi": "dekor",
    "kisiye-ozel-chihuahua-figuru": "evcil",
    "kisiye-ozel-fransiz-bulldog-figuru": "evcil",
    "kisiye-ozel-artopop-aile-figuru": "aile",
    "kisiye-ozel-mini-figur-seti": "set",
    "kisiye-ozel-kamp-atesi-diorama-figuru": "set",
    "kisiye-ozel-uluyan-kurt-figuru": "isimli",
    "kisiye-ozel-araba-standi": "isimli",
    "terzi-temali-pasta-susu-seti": "pasta",
    "mini-anahtarlik-figur": "anahtarlik",
    "detayli-anahtarlik-figur": "anahtarlik",
}

# Aynı türdeki ürünler aynı üretim anlatımını paylaşıyor; sayfaları ayıran şey
# bu cümle. Her biri ürünün KENDİ katalog açıklamasındaki olgudan türetildi
# (büst, iki karakterli, chibi, eklemli, isim plaketli, çok parçalı…).
URUN_AYIRT = {
    "samuray-bustu-figuru":
        "Bu çalışma bir büst: gövde değil baş ve omuz kısmı üretiliyor. "
        "Katalogdaki altın detaylar elle boyanıyor.",
    "mirabel-figuru-encanto":
        "Canlı renkli bir çalışma. Renk geçişleri elle boyandığı için aynı "
        "figürün iki baskısı birebir aynı olmuyor.",
    "sprinku-figuru":
        "Koleksiyon rafında durmak üzere üretilen bir figür; renkli detayları "
        "elle boyanıyor.",
    "masa-ile-koca-ayi-figuru":
        "Tek gövde değil iki karakter birlikte çıkıyor. İki figürün boyaması "
        "ayrı ayrı yapıldığı için bu tür çalışmalar tek figürlülerden uzun sürüyor.",
    "kratos-chibi-figuru":
        "Chibi tarz, yani gövdenin küçültülüp başın büyütüldüğü oran. Yüz "
        "büyüdüğü için boyamada en çok işçiliği yüz alıyor.",
    "kisiye-ozel-anime-karakter-figuru":
        "İsim plaketi figürle birlikte üretiliyor; plakete yazılacak metni "
        "sipariş sırasında netleştiriyoruz.",
    "minecraft-warden-figuru":
        "Eklemli bir çalışma: parçalar hareket edecek şekilde ayrı ayrı basılıp "
        "birleştiriliyor, yani tek parça bir figürden daha fazla adım var.",
    "detayli-motosiklet-maketi":
        "Maketin ince parçaları ayrı basılıp birleştirildiği için bu tür "
        "çalışmalarda montaj da işçiliğin bir parçası.",
    "honda-civic-araba-maketi":
        "Gövde tek parça çıkıyor, gri boyamanın üzerine detaylar elle işleniyor.",
    "galatasaray-hagi-forma-cercevesi":
        "Duvara asılacak bir parça. Asılacağı yere göre ölçü önemliyse ölçüyü "
        "baştan alıp modeli ona göre kuruyoruz.",
    "agac-dalli-ayna-cercevesi":
        "Çerçevenin içine gelecek ayna ölçüsüne göre modelleniyor. Elinizde "
        "ayna varsa ölçüsünü baştan alıyoruz.",
    "kisiye-ozel-chihuahua-figuru":
        "Chihuahua çalışmalarımız galeride duruyor; fotoğraftaki tüy rengine "
        "göre boyuyoruz.",
    "kisiye-ozel-fransiz-bulldog-figuru":
        "Fransız bulldog çalışmalarımız galeride duruyor; fotoğraftaki tüy "
        "rengine göre boyuyoruz.",
    "kisiye-ozel-artopop-aile-figuru":
        "Aile fotoğrafından çok kişili bir set çıkıyor. Kişi sayısı, hem "
        "modelleme hem boyama işçiliğini artıran ana etken.",
    "kisiye-ozel-mini-figur-seti":
        "Şövalye temalı, çok parçalı bir set. Parça sayısı arttıkça baskı ve "
        "boyama süresi de artıyor.",
    "kisiye-ozel-kamp-atesi-diorama-figuru":
        "Diorama tek figür değil bir sahne: zemin, figürler ve sahne parçaları "
        "birlikte kurgulanıyor.",
    "kisiye-ozel-uluyan-kurt-figuru":
        "Üzerine isim harfi işleniyor; hangi harf ya da isim geleceğini sipariş "
        "sırasında netleştiriyoruz.",
    "kisiye-ozel-araba-standi":
        "Masaüstü bir stand ve üzerine isim yazılıyor. Belirli bir araca "
        "oturması gerekiyorsa ölçüyü baştan alıyoruz.",
    "terzi-temali-pasta-susu-seti":
        "Dikiş makinesi ve makas figürlerinden oluşan temalı bir set; pastanın "
        "üstünde durmak üzere, süs amaçlı üretiliyor.",
    "mini-anahtarlik-figur":
        "Katalogdaki iki anahtarlık boyundan küçük olanı. Daha büyük ve daha "
        'detaylı boyalı olanı <a href="/urun/detayli-anahtarlik-figur/">detaylı '
        "anahtarlık figür</a> sayfasında.",
    "detayli-anahtarlik-figur":
        "Katalogdaki iki anahtarlık boyundan büyük olanı; boyaması da daha "
        'detaylı. Küçük boy <a href="/urun/mini-anahtarlik-figur/">mini '
        "anahtarlık figür</a> sayfasında.",
}

# Tür başına: (giriş tamamlaması, malzeme paragrafı, model paragrafı).
# Malzeme ifadelerinin tamamı /ankara-3d-baski/ sayfasındaki tablodan geliyor;
# spesifikasyon değil, atölyenin kendi tercihi olarak ve kaynağa bağlanarak.
TUR_METNI = {
    "karakter": (
        "koleksiyon için üretilen karakter figürlerinden biri",
        "İnce detay isteyen figür ve büstleri genellikle <strong>SLA reçine</strong> "
        "ile basıyoruz: katman izi neredeyse görünmüyor, yüz hatları ve küçük "
        "parçalar net çıkıyor. Hangi işte hangi malzemeyi seçtiğimizi "
        '<a href="/ankara-3d-baski/">Ankara 3D baskı</a> sayfasında tablo hâlinde yazdık.',
        "Hazır modeli olan çalışmalarda doğrudan baskıya geçiyoruz. Aklınızdaki "
        'başka bir karakterin modeli yoksa <a href="/3d-modelleme/">modellemeyi</a> '
        "biz yapıyoruz."),
    "maket": (
        "maket tarafına giren bir çalışma",
        "Maket ve dekor parçalarında genellikle <strong>PLA</strong> kullanıyoruz; "
        "boyayı iyi tutuyor ve renk seçeneği geniş. Dayanım ya da esneklik isteyen "
        'işlerde başka malzemelere geçiyoruz — <a href="/ankara-3d-baski/">malzeme '
        "tablosu</a> o sayfada.",
        "Elinizde hazır model varsa doğrudan basıyoruz; yoksa fotoğraftan ya da "
        'ölçüden <a href="/3d-modelleme/">modeli biz çıkarıyoruz</a>.'),
    "dekor": (
        "ev dekoru tarafında duran bir çalışma",
        "Dekor ve hediyelik parçalarda genellikle <strong>PLA</strong> kullanıyoruz; "
        "boyanacak yüzeyde boyayı iyi tutuyor. "
        '<a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Belirli bir yere oturması gereken parçalarda ölçüyü alıp modeli ona göre "
        'kuruyoruz — <a href="/3d-modelleme/">ölçüden modelleme</a> böyle işliyor.'),
    "evcil": (
        "fotoğraftan üretilen evcil hayvan figürlerinden biri",
        "Yüz hatları ve ince detay taşıyan figürleri genellikle "
        "<strong>SLA reçine</strong> ile basıyoruz. "
        '<a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Fotoğraftan çalışıyoruz: yüzün ya da vücudun net göründüğü bir fotoğraf "
        "yeterli, birden fazla açı varsa benzerlik daha yüksek çıkıyor. Sürecin "
        'tamamı <a href="/kisiye-ozel-3d-figur/">kişiye özel figür</a> sayfasında.'),
    "aile": (
        "aile fotoğrafından üretilen çok kişili setlerden biri",
        "Yüz hatları taşıdığı için genellikle <strong>SLA reçine</strong> ile "
        'basıyoruz. <a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Aile fotoğrafından çalışıyoruz; yüzlerin net göründüğü bir fotoğraf "
        "yeterli. Tasarım önizlemesini birlikte onayladıktan sonra üretime "
        'geçiyoruz — <a href="/kisiye-ozel-3d-figur/">sürecin tamamı</a>.'),
    "set": (
        "çok parçalı çalışmalardan biri",
        "Sahnedeki parçalar aynı şeyi istemiyor, o yüzden malzemeyi parça parça "
        "seçiyoruz: ince detay taşıyan parçalarda reçine, boyanacak gövde ve zemin "
        'yüzeylerinde PLA öne çıkıyor. <a href="/ankara-3d-baski/">Malzeme '
        "tablosu</a> o sayfada.",
        "Sahnenin kurgusunu baştan konuşuyoruz; önizlemeyi onayladıktan sonra üretim "
        'başlıyor. <a href="/kisiye-ozel-3d-figur/">Süreci</a> o sayfada anlattık.'),
    "isimli": (
        "üzerine isim ya da harf işlenen hediyelik çalışmalardan biri",
        "Hediyelik ve dekor parçalarda genellikle <strong>PLA</strong> kullanıyoruz. "
        '<a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Yazılacak isim ya da harfi sipariş sırasında alıyoruz; önizlemeyi "
        "onayladıktan sonra üretime geçiyoruz."),
    "pasta": (
        "temalı süs setlerinden biri",
        "Bu tür parçalarda genellikle <strong>PLA</strong> kullanıyoruz. "
        '<a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Temayı ve setin içindeki parçaları baştan konuşuyoruz; farklı bir tema "
        "isterseniz onu da üretebiliyoruz."),
    "anahtarlik": (
        "anahtarlık boyunda küçük figürlerden biri",
        "Küçük parçalarda detayın kaybolmaması için genellikle "
        "<strong>SLA reçine</strong> tercih ediyoruz. "
        '<a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Kişiye özel bir figür isterseniz fotoğraftan çalışıyoruz; hazır bir model "
        "varsa doğrudan basıyoruz."),
}

# SSS cevaplarının tamamı sitenin kendi SSS metinlerinden (sayfa-uret.py
# içindeki SAYFALAR sözlüğü) alındı; yeni bir iddia eklenmedi.
SSS_FOTOGRAF = (
    "Fotoğraftan figür yapmak için nasıl bir fotoğraf gerekiyor?",
    "Yüzün ya da vücudun net göründüğü bir fotoğraf yeterli. Birden fazla açı "
    "varsa benzerlik daha yüksek çıkıyor.")
SSS_BOYA = (
    "Figürler boyalı mı geliyor?",
    "Evet, figürleri elle boyayıp gönderiyoruz. Kendiniz boyamak isterseniz "
    "boyanmamış hâliyle de hazırlayabiliyoruz.")
SSS_FIYAT = (
    "Fiyat neye göre değişiyor?",
    "Boyuta, detay yoğunluğuna ve boya işçiliğine göre değişiyor. Farklı bir ölçü "
    "ya da detay isterseniz fiyatı birlikte netleştiriyoruz.")
SSS_SURE = (
    "Ne kadar sürede hazır olur?",
    "Ürünün karmaşıklığına göre değişmekle birlikte siparişler genellikle 3-7 iş "
    "günü içinde kargoya teslim ediliyor. Boyama ve elle rötuş gerektiren "
    "figürlerde bu süre üst sınıra yaklaşıyor.")
SSS_ELDEN = (
    "Ankara'da elden teslim alabilir miyim?",
    "Evet. Ankara içindeyseniz ürünü elden teslim edebiliyoruz, ayrıntıyı "
    "WhatsApp'tan konuşuyoruz.")
SSS_MODEL = (
    "Elimde 3D model yok, yine de bastırabilir miyim?",
    "Bastırabilirsiniz. Fikri, fotoğrafı ya da ölçüyü alıp baskıya hazır modeli "
    "biz tasarlıyoruz.")

TUR_SSS = {
    "karakter": [SSS_BOYA, SSS_FIYAT, SSS_SURE],
    "maket": [SSS_MODEL, SSS_FIYAT, SSS_SURE],
    "dekor": [SSS_MODEL, SSS_ELDEN, SSS_SURE],
    "evcil": [SSS_FOTOGRAF, SSS_BOYA, SSS_SURE],
    "aile": [SSS_FOTOGRAF, SSS_FIYAT, SSS_SURE],
    "set": [SSS_FOTOGRAF, SSS_FIYAT, SSS_SURE],
    "isimli": [SSS_FOTOGRAF, SSS_ELDEN, SSS_SURE],
    "pasta": [SSS_MODEL, SSS_ELDEN, SSS_SURE],
    "anahtarlik": [SSS_FIYAT, SSS_ELDEN, SSS_SURE],
}


def urun_icerik(u: dict) -> str:
    """Ürüne özgü üretim anlatımı + SSS bölümlerinin HTML'i.

    Tanınmayan slug derlemeyi DURDURUR: yeni bir ürün eklenirse sessizce
    diğerleriyle aynı metni taşımasın, çünkü düzeltilen arıza tam buydu.
    """
    tur = URUN_TURU.get(u["slug"])
    if tur is None:
        raise SystemExit(
            f"Yeni ürün '{u['slug']}': scripts/urun_icerik.py içindeki URUN_TURU "
            "ve URUN_AYIRT'a eklenmeli. Eklenmezse sayfa diğer ürünlerle aynı "
            "metni taşır ve dizine girmez.")
    giris, malzeme, model = TUR_METNI[tur]
    ayirt = URUN_AYIRT.get(u["slug"], "")
    sss = "\n".join(
        f'        <details class="faq-item"><summary>{q}</summary><p>{c}</p></details>'
        for q, c in TUR_SSS[tur])
    return f"""
  <section>
    <div class="container">
      <div class="section-head reveal"><h2>Bu çalışma nasıl üretiliyor?</h2></div>
      <div class="sayfa-metin reveal">
        <p>{u["ad"]}, atölyede {giris}. {ayirt}</p>
        <p><strong>Malzeme.</strong> {malzeme}</p>
        <p><strong>Model.</strong> {model}</p>
        <p><strong>Fiyat.</strong> Katalogdaki {u["fiyat_metni"]} bu çalışmanın kendi
           ölçüsü ve detayı için. Boy, detay yoğunluğu ve boya işçiliği değiştiğinde
           fiyat da değişiyor; farklı bir ölçü isterseniz WhatsApp'tan birlikte
           netleştiriyoruz.</p>
      </div>
    </div>
  </section>

  <section class="section--alt">
    <div class="container">
      <div class="section-head reveal"><span class="eyebrow">Merak Edilenler</span><h2>Sıkça sorulan sorular</h2></div>
      <div class="faq reveal">
{sss}
      </div>
    </div>
  </section>
"""
