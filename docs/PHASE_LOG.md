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

### Yayın sonucu

Yayın commit'i: `c442513adb63c80bfd646cd377499f332be79c7b`.
GitHub Actions: https://github.com/Sefa-Yuzuak/3dartolyemizweb/actions/runs/38393143822
İş akışı başarılı. İlk kontrol eski sürümü gösterdiği için iş akışı sonucu tek
başına yayın kanıtı sayılmadı; Coolify'ın dağıtımı tamamlaması beklendi.
Ardından sorgu eki olmadan canlı 185 sayfa ile CSS, JS, üç yeni WebP,
sitemap.xml, robots.txt ve llms.txt (toplam 193 URL) HTTP 200 verdi ve yerel
dosyalarla birebir eşleşti (metin dosyalarında yalnız CRLF/LF normalize edildi).
Böylece yerel denetimden geçen WhatsApp alıcı/sayfa bağlamı ve Instagram profil
hedeflerinin canlı HTML'ye ulaştığı doğrulandı. Dış uygulama açılışı test edilmedi.
docs/PHASE_LOG.md, content/urunler.json, scripts/iletisim.py, .local-research/
ve requirements-build.txt canlıda 404; araştırma/geliştirme dosyaları sunulmuyor.
Tarayıcı bağlı olmadığından mobil/masaüstü görsel kontrol sınırı devam ediyor.
Kesin geri dönüş: `git revert c442513adb63c80bfd646cd377499f332be79c7b` ardından
`git push origin master`; dağıtımdan sonra önceki dosyaların canlı eşleşmesini kontrol et.
Durum: onaylanan yayın aşaması tamamlandı. Yeni bir geliştirme fazı başlatılmadı.

## 14 Ekim 2026 — WhatsApp bağlantı önizlemesinde yazılı logo

Yetki: kullanıcı maket bağlantısının WhatsApp önizlemesindeki atölye fotoğrafını
Artölyemiz yazılı logosuyla değiştirmeyi istedi. Mevcut logo.jpg işareti korunarak
1200×630 PNG paylaşım kartına 3D ARTÖLYEMİZ yazısı eklendi. Yeni dosya adı
artolyemiz-paylasim-logo-v1.png; eski görsel URL'si yeniden kullanılmadı.
Genel resmi kullanan 12 sayfanın OG/Twitter etiketleri ortak şablondan üretildi.
Ürüne özel görsel kullanan sayfalar genel logo boyut/açıklamasını devralmıyor.

Etki: 12 HTML, şablon üreticisi ve yeni marka kartı/üretim betiği. Risk: WhatsApp
önbelleği eski önizlemeyi tutabilir; dağıtımda geçici erişim kesintisi olabilir.
Geri dönüş: bu değişikliği taşıyan yayın commit'ini git revert ile geri alıp
git push origin master; yayın öncesi HEAD 01b85ab864b0cba2dd829967fd29ef5b4ebbbfd6.
Doğrulama: görsel 1200×630, 86.062 bayt; yazı ve logo görsel olarak incelendi.
186 sayfa denetiminde yüksek/orta hata yok, önceki 80 düşük uyarı değişmedi.
185 sayfa/1114 WhatsApp/543 Instagram/149 ürün iletişim denetiminde sıfır hata.
Sonraki adım: mevcut GitHub/Coolify akışıyla yayın ve canlı içerik eşleşmesi.
WhatsApp uygulamasındaki önbelleğin yenilendiği ayrıca doğrulanmış değildir.

Yayın sonucu: 480b4f010e889ea8b3beb17be9342bc2d3ba3412 yayımlandı.
GitHub Actions 38540407191 başarılı. WhatsApp User-Agent başlığıyla sorgu eki
olmadan canlı 12 HTML ve yeni PNG kontrol edildi: 13/13 HTTP 200 ve yerel
içerikle birebir eşleşme (HTML'de CRLF/LF normalize edilerek). PNG image/png
olarak sunuluyor. Kesin geri dönüş: git revert 480b4f0 ve git push origin master.
Site tarafındaki önizleme değişikliği tamamlandı; uygulama içi önbellek veya
önceden gönderilmiş mesajın kartının yenilendiği iddia edilmiyor.


## 2026-10-14 — Fotoğraf arşivi seçimi ve tam kadraj yerleşimi

- Yetki: sahibi tüm site görsellerinin incelenmesini ve uygun fotoğrafların kullanılmasını istedi; önceki yayın yetkisi sürüyor.
- Etki: ana açılış, 8 hizmet sayfası, 6 ürünün ek fotoğrafları, Garfield ana fotoğrafı, ürün/galeri CSS. 17 seçilen fotoğraf, 34 WebP dosyası, toplam 2.131.518 bayt.
- Gerekçe ve kaynaklar: `docs/GORSEL_INCELEME_2026-10-14.md`, `content/gorsel-secimleri.json`. Tüm 1.980 farklı arşiv fotoğrafı önizlemeyle tarandı; seçilen adaylar büyük boyutta kontrol edildi.
- Risk: ek görsel yükü ve tam kadrajda kenar boşlukları. Küçük WebP/srcset/lazy loading kullanıldı; kaynak fotoğraflar ve eski varlıklar korundu.
- Geri dönüş: bu yayın commit'ini `git revert <commit>` ile geri al ve master'a gönder. Önceki HEAD c6ed4ad.
- Doğrulama: üretim başarılı; 186 HTML yüksek/orta 0, önceki düşük 80. 1.114 WhatsApp ve 543 Instagram bağlantısı, hata 0. Chromium 390/1440 genişliklerinde 16 rota × 2 = 32 kontrol; taşma, bozuk resim, JS hatası 0. Ana galeri lightbox iki boyutta açıldı ve görsel olarak incelendi.
- Sonraki adım: yayın iş akışı ve canlı HTML/medya eşleşmesini doğrula.
