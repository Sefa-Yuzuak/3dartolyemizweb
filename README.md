# 3D Atölyemiz — artolyemiz.com

Statik tanıtım/portfolyo sitesi. Vanilla HTML/CSS/JS — framework, build step veya npm yok.

## Kurulum (lokal önizleme)

Build adımı yok. Herhangi bir statik sunucu ile açman yeterli, örneğin:

```
npx serve .
```

veya VS Code "Live Server" eklentisi ile `index.html` dosyasını aç.

## Görseller ve galeri verisi

Instagram görselleri artık entegre edilmiş durumda: `assets/img/is-01.webp` ... `is-41.webp`
(41 görsel) + `assets/img/og.webp`. Kaynak veri ve üretim adımları:

- Ham medyalar `assets/img/_raw/` içindeydi (git'e girmez, `.gitignore`'da hariç tutulur).
  `scripts/optimize-images.ps1` bu klasördeki her görseli (JPG/PNG/HEIC/WebP) ImageMagick ile
  max 1200px genişlik, kalite ~80, EXIF temizlenmiş ve sRGB olarak `is-01.webp`, `is-02.webp`
  ... şeklinde `assets/img/` köküne yazar; gerçek en/boy oranlarını `scripts/image-manifest.csv`
  dosyasına kaydeder. 2 adet `.mp4` video otomatik atlandı (galeri sadece görsel içerir).
- `content/aciklamar.txt.json` (Instagram veri export'u) → `scripts/extract-captions.ps1` ile
  gönderi açıklamaları okunup mojibake (çift UTF-8 kodlama) hatası düzeltilir, çıktısı
  `scripts/captions-report.txt`'e yazılır.
- Bu iki kaynaktan üretilen nihai ürün adı/açıklama/kategori eşleşmesi elle
  `assets/js/gallery.js` içindeki `GALLERY` dizisine yazıldı (41 kayıt, her biri `src, w, h,
  title, alt, tag` alanlarına sahip). 11 kayıt doğrudan gerçek Instagram gönderi metninden,
  30 kayıt ise gönderiyle eşleşen açıklama bulunamadığı için görselin doğrudan incelenmesiyle
  yazıldı — bu 30 kayıt için ürün/müşteri isimleri site tarafından bilinmediğinden başlıklar
  kategoriye dayalı genel ama gerçeğe uygun ifadelerdir (bkz. sohbet özeti / commit mesajı).
  Yeni görsel eklemek istersen `GALLERY` dizisine aynı formatta bir satır eklemen yeterli.
- Bir görsel yüklenemezse sayfa kırılmaz: `onerror` ile marka renklerinde, kategori adı
  yazılı bir SVG placeholder'a düşer (`assets/js/gallery.js` içindeki `placeholder()`).

Yeniden görsel eklemek/değiştirmek istersen: dosyayı `assets/img/_raw/` içine koy,
`powershell -ExecutionPolicy Bypass -File scripts/optimize-images.ps1` çalıştır, çıkan
`is-XX.webp` için `gallery.js`'e satır ekle.

## Dosya yapısı

```
/index.html          Tek sayfalık site
/404.html            Özel 404 sayfası
/robots.txt
/sitemap.xml
/site.webmanifest
/favicon.ico
/assets/img/logo.jpg, favicon-*.png, apple-touch-icon.png, icon-192.png, icon-512.png
/assets/css/style.css
/assets/js/main.js       header, mobil menü, scroll reveal, WhatsApp FAB
/assets/js/gallery.js    galeri verisi + lightbox
/assets/img/             ürün/etkinlik görselleri (is-01..41.webp, og.webp)
/content/aciklamar.txt.json   Instagram veri export'u (kaynak veri, siteye dahil değil)
/scripts/                bir kerelik dev scriptleri (görsel dönüştürme, caption çıkarma)
/Dockerfile
/nginx.conf
```

## Coolify üzerinde deploy / redeploy

1. Coolify'da yeni bir "Application" oluştur, kaynak olarak bu Git reposunu bağla,
   build tipi olarak **Dockerfile** seç (repo kökündeki `Dockerfile` otomatik algılanır).
2. Port olarak `80` kullan (Dockerfile içinde `EXPOSE 80` tanımlı).
3. İlk deploy'da Coolify image'ı build edip container'ı ayağa kaldıracaktır.
4. Görselleri ekledikten veya içerikte değişiklik yaptıktan sonra:
   - Değişiklikleri bu repoya `git push` ile gönder.
   - Coolify panelinden ilgili uygulamanın üzerine gidip **Redeploy** butonuna bas
     (veya otomatik deploy webhook'u bağlıysa push sonrası otomatik tetiklenir).
5. Domain (`artolyemiz.com`) Coolify tarafında bu uygulamaya bağlanmalı; SSL sertifikası
   Coolify'ın kendi Let's Encrypt entegrasyonundan otomatik sağlanır.

## Notlar / varsayımlar

- Hero bölümündeki "500+ mutlu müşteri" rakamı örnek/başlangıç değeridir —
  `index.html` içinde `<!-- Not: -->` yorumuyla işaretlenmiştir, gerçek sayıya göre güncelle.
- `og.webp` (1200×630), hero kolajı (`is-01/02/03`) ve etkinlik bölümü (`is-08`) artık
  gerçek Instagram görselleri kullanıyor.
- Lighthouse Performance/Accessibility/SEO hedefleri için: harici tek bağımlılık
  Google Fonts'tur (preconnect + `display=swap` ile optimize edilmiştir).
