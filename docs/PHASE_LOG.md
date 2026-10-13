# Faz günlüğü

## 13 Ekim 2026 — SEO/GEO, Instagram kanıtları ve iletişim bağlantıları

Yetki: kullanıcı mevcut araştırmaya göre iyileştirme istedi; hizmet girişlerinin
zaten yeterli olduğunu belirtti ve WhatsApp/Instagram bağlantılarını öncelikledi.

Karar: mevcut hizmet metinlerini korumak; gerçek export örneklerini kullanmak;
sayfa bağlamı taşıyan statik WhatsApp bağlantıları ve görünür Instagram erişimi
sağlamak. Özel müşteri yazışmaları yerine kamuya paylaşılmış üretim örnekleri
siteye işlendi. Araştırma ve teknik gerekçeler `SEO_GEO_2026-10-13.md` içindedir.

Etki: ortak şablon, 185 sayfa, 149 ürünün fiyat şeması; 3 story görseli ve 7 ürün notu.
Risk: sabit mobil iletişim alanının kaplama davranışı; tahmini teklif kaldırıldığı
için ürün zengin sonucu uygunluğunun azalması. Canlıya değişiklik gönderilmedi.
Geri dönüş: `3cee049` ve dosya listeleriyle yalnız bu turun yerel değişikliklerini
geri al; yeni dosyalarda proje sınırını doğrula. Arşiv/mesaj kaynakları değişmedi.
Doğrulama: üretim, iletişim regresyonu ve JS sözdizimi kontrolleri başarılı;
genel denetimde yüksek/orta hata yok, 80 eski düşük uyarı var. Bağlı tarayıcı
olmadığı için ekran ve uygulama geçişi doğrulaması tamamlanamadı.

Durum: yerel geliştirme aşaması tamamlandı. Kullanıcının faz sonunda durma
talimatı gereği yayın aşamasına geçilmedi. Sonraki adım: görsel önizleme ve
yayın onayı sonrasında mevcut Coolify akışıyla yayın; ardından canlı doğrulama.

## 13 Ekim 2026 — Onaylanan yayın aşaması

Yetki: kullanıcı önceki yayın sorusunu alıntılayarak "yayın aşamasına geç" dedi.
Karar: mevcut master → GitHub Actions → Coolify akışıyla onaylanan dosyaları yayınla.
Etki: 185 sayfanın iletişim/SEO çıktıları, 3 story görseli ve 7 üretim notu.
Risk: dağıtım sırasında kısa erişim kesintisi ve mobil iletişim alanının yerleşimi.
Bağlı tarayıcı bulunmadığından görsel ekran kontrolü hâlâ doğrulanamadı.
Geri dönüş: bu yayın commit'ini git revert ile geri alıp master'a gönder; mevcut
dağıtım akışı önceki site dosyalarını yeniden yayınlar. Başlangıç: 3cee049.
Doğrulama: yayın öncesi kapsam listeleri birebir eşleşti (195 izlenen, 10 yeni dosya).
186 HTML denetiminde yüksek/orta hata yok; 80 önceki düşük uyarı sürüyor.
185 sayfa, 1114 WhatsApp, 543 Instagram ve 149 ürün denetiminde sıfır hata;
JavaScript sözdizimi kontrolü başarılı. Uzak master başlangıç commit'iyle aynı.
Sonraki adım: commit/push, dağıtım takibi ve canlı dosya/bağlantı doğrulaması.
