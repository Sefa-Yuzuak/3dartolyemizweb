# Görsel inceleme — 14 Ekim 2026

Sahibin talebi: fotoğraf arşivini gözden geçirip sitede uygun yerlerde kullanmak; WhatsApp logo önizlemesi ve Instagram/WhatsApp bağlantıları önemlidir.

## İnceleme ve seçim

- Sitedeki 149 ürün ana görseli, ek çalışma ve atölye görselleri dahil 193 görsel önizleme üzerinden incelendi.
- 08.10.2026 tarihli Instagram dışa aktarımının yalnız `media/posts/` ve `media/stories/` fotoğrafları kullanıldı. 2.378 dosyanın birebir SHA-256 tekrarları elenince 1.367 gönderi ve 613 story fotoğrafı kaldı.
- Bu 1.980 farklı fotoğrafın tamamı küçük önizleme sayfalarında tarandı. Seçim adayları daha büyük boyutta ayrıca incelendi; bütün arşivin tam çözünürlükte tek tek incelendiği iddia edilmiyor.
- 17 fotoğraf seçildi. Orijinal arşivler değiştirilmedi. WebP büyük/küçük sürümler üretildi; kaynak yolu ve kaynak SHA-256 değerleri `content/gorsel-secimleri.json` içinde kayıtlı.
- Müşteri mesajı ekran görüntüleri, tekrarlanan kareler, güncelliğini yitirmiş etkinlik afişleri ve kaynağı net olmayan katalog renderları yeni üretim kanıtı olarak seçilmedi. Yeni çocuk portresi eklenmedi.

## Uygulama

- Ana açılış: kişiye özel çift figürü, mevcut motosiklet maketi ve yazıcı tablasındaki eklemli ejderha.
- Sekiz hizmet sayfası: hizmetle ilgili üçer kare ve ne görüldüğünü söyleyen kısa alt yazılar. Tamir sayfasındaki kareler atölye ekipmanını gösterir; belirli bir tamirin önce/sonra kanıtı değildir.
- Altı ürün sayfası: köpek, kedi, Garfield, Fred Çakmaktaş, Yukarı Bak evi ve ArtoPop kutusunda ek açı/içerik fotoğrafları.
- Garfield ana görseli arkadan görünümden önden görünüme değişti.
- Ürün ve ana galeri kartları 3:4 oranında, `contain` ile fotoğrafın tamamını gösterir. Galeri hover büyütmesiyle oluşan kırpma kaldırıldı.
- Telefonda ek fotoğraflar yatay kaydırılır; büyük görseller bağlantıyla açılır. Ana galeri mevcut klavye destekli lightbox kullanır.
- Genel WhatsApp/Open Graph logo görseli korunur. Ürün sayfaları kendi ürün görsellerini kullanmayı sürdürür.

## Risk ve geri dönüş

Yeni kareler mobilde indirme yükü oluşturabilir; küçük WebP, srcset ve lazy loading kullanıldı. Tam kadraj gösterimi bazı dikey fotoğrafların kenarında boşluk bırakır; ürünün kesilmemesi tercih edildi. Kaynak dosyalar ve eski görseller korunur. Yayın commit'i `git revert` ile geri alınarak tekrar yayımlanabilir; değişiklik öncesi HEAD `c6ed4ad`.

## Doğrulama

Sayfa üretimi ve denetimler: 186 HTML, yüksek 0, orta 0; önceki 80 düşük başlık uzunluğu uyarısı devam ediyor. İletişim denetimi: 185 sayfa, 149 ürün, 1.114 WhatsApp ve 543 Instagram bağlantısı, hata 0. Son tarayıcı ve canlı yayın sonucu faz kaydına eklenir.
