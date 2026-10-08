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
* Ürünün kendi kaydı (content/urunler.json): adı, türü, açıklaması, ayırt edici
  cümlesi ve fiyat aralığı. Fiyatlar ve süreç 08.10.2026'da @3dartolyemiz
  Instagram mesajlarından ölçüldü (sahibin müşteriye verdiği fiyatlar).

Ölçü, ağırlık, katman kalınlığı, malzeme garantisi gibi BİLİNMEYEN hiçbir şey
yazılmadı. Malzeme, spesifikasyon olarak değil atölyenin kendi ifadesiyle
("bu tür işlerde genellikle şunu kullanıyoruz") ve kaynak sayfaya bağlanarak
veriliyor.
"""

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
    "boyama": (
        "kendiniz boyamanız için hazırlanan kutulu setlerden biri",
        "Boyanacak figürlerde genellikle <strong>PLA</strong> kullanıyoruz; yüzeyi boyayı "
        'iyi tutuyor. <a href="/ankara-3d-baski/">Malzeme tablosu</a> o sayfada.',
        "Figür boyasız gönderiliyor; boyalar minik tüplerde, fırçasıyla birlikte kutunun "
        'içinde. Aynı deneyimi grupça yaşamak için <a href="/dogum-gunu-boyama-atolyesi/">'
        "boyama atölyemiz</a> var."),
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
    "Boyuta, detay yoğunluğuna ve boya işçiliğine göre değişiyor; sayfadaki fiyat "
    "yaklaşıktır. Farklı bir ölçü ya da detay isterseniz fiyatı birlikte "
    "netleştiriyoruz.")
SSS_SURE = (
    "Ne kadar sürede hazır olur?",
    "Genellikle 3-7 gün içinde hazırlanıp kargoya veriliyor. Elle boyanan "
    "işlerde süre üst sınıra yaklaşıyor; yoğun dönemlerde 10-14 güne çıkabiliyor. "
    "Kargo 2-3 gün sürüyor.")
SSS_ODEME = (
    "Ödeme nasıl yapılıyor?",
    "Modelleme bitince videosunu gönderiyoruz; onaylarsanız kapora alıp baskıya "
    "geçiyoruz. Ürün bitince yine video atıyoruz, kalan tutarı aldıktan sonra "
    "gönderiyoruz. Taksit imkânımız yok.")
SSS_BOYASIZ = (
    "Kutunun içinde neler var?",
    "Boyanmamış figür, minik tüplerde boyalar ve fırça. Boyasız figür ve boyalar "
    "kutuda birlikte geliyor; isterseniz figürü boyalı da gönderiyoruz.")
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
    "maket": [SSS_MODEL, SSS_ODEME, SSS_SURE],
    "dekor": [SSS_MODEL, SSS_ELDEN, SSS_SURE],
    "evcil": [SSS_FOTOGRAF, SSS_ODEME, SSS_SURE],
    "aile": [SSS_FOTOGRAF, SSS_ODEME, SSS_SURE],
    "set": [SSS_FOTOGRAF, SSS_FIYAT, SSS_SURE],
    "isimli": [SSS_FOTOGRAF, SSS_ELDEN, SSS_SURE],
    "pasta": [SSS_MODEL, SSS_ELDEN, SSS_SURE],
    "anahtarlik": [SSS_FIYAT, SSS_ELDEN, SSS_SURE],
    "boyama": [SSS_BOYASIZ, SSS_ELDEN, SSS_SURE],
}


def urun_icerik(u: dict) -> str:
    """Ürüne özgü üretim anlatımı + SSS bölümlerinin HTML'i.

    Türü ya da ayırt edici cümlesi olmayan ürün derlemeyi DURDURUR: sessizce
    diğerleriyle aynı metni taşımasın, çünkü düzeltilen arıza tam buydu.
    """
    if u.get("tur") not in TUR_METNI or not u.get("ayirt"):
        raise SystemExit(
            f"Ürün '{u['slug']}': content/urunler.json'da geçerli 'tur' ve dolu "
            "'ayirt' olmalı. Yoksa sayfa diğer ürünlerle aynı metni taşır ve dizine girmez.")
    tur = u["tur"]
    giris, malzeme, model = TUR_METNI[tur]
    ayirt = u["ayirt"]
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
        <p><strong>Fiyat.</strong> Bu çalışma için fiyat {u["fiyat_kucuk"]} arasında.
           Boy, detay yoğunluğu ve boya işçiliği aralığın neresinde olacağını
           belirliyor; görseli WhatsApp'tan gönderdiğinizde kesin tutarı netleştiriyoruz.</p>
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
