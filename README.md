# 3D Atölyemiz — artolyemiz.com

Statik tanıtım/portfolyo sitesi. Vanilla HTML/CSS/JS — framework, build step veya npm yok.

## Kurulum (lokal önizleme)

Build adımı yok. Herhangi bir statik sunucu ile açman yeterli, örneğin:

```
npx serve .
```

veya VS Code "Live Server" eklentisi ile `index.html` dosyasını aç.

## Görselleri ekleme (ÖNEMLİ)

Instagram'daki gerçek ürün/etkinlik görselleri otomatik indirilemedi, bu yüzden site şu an
marka renkli SVG placeholder görsellerle çalışıyor. Gerçek görselleri eklemek için:

1. `assets/img/` klasörüne aşağıdaki dosya adlarıyla görselleri at:
   - `is-01.jpg` ... `is-12.jpg` → Galeri bölümündeki 12 kare (sırası `assets/js/gallery.js` içindeki `GALLERY` dizisiyle eşleşir, tag/alt metnini oradan güncelleyebilirsin)
   - `hero-1.jpg`, `hero-2.jpg`, `hero-3.jpg` → Ana sayfa (hero) kolaj görselleri
   - `event-1.jpg` → Doğum günü boyama etkinliği bölümü görseli
   - `og.jpg` (1200×630 önerilir) → Sosyal medya paylaşım kartı (Open Graph) görseli
2. **Başka hiçbir şeyi değiştirme.** Dosya adı ve klasör doğruysa görseller otomatik olarak
   placeholder'ların yerine geçer, kod tarafında ek bir işlem gerekmez.
3. Görselleri **maksimum 1200px genişlikte** tut, mümkünse **WebP** formatını tercih et
   (dosya adını yine `.jpg` olarak bırakabilir ya da gallery.js içindeki uzantıları `.webp`
   olarak güncelleyebilirsin — ikisi de çalışır, önemli olan dosya adının eşleşmesi).

Bir görsel eksik/bozuksa sayfa kırılmaz: `onerror` ile otomatik olarak marka renklerinde,
ürün adı yazılı bir SVG placeholder'a düşer.

## Dosya yapısı

```
/index.html          Tek sayfalık site
/404.html            Özel 404 sayfası
/robots.txt
/sitemap.xml
/site.webmanifest
/favicon.svg
/assets/css/style.css
/assets/js/main.js       header, mobil menü, scroll reveal, WhatsApp FAB
/assets/js/gallery.js    galeri verisi + lightbox
/assets/img/             ürün/etkinlik görselleri (bkz. yukarıdaki not)
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
- `og.jpg`, hero ve etkinlik görselleri eklenene kadar SVG placeholder gösterilir.
- Lighthouse Performance/Accessibility/SEO hedefleri için: harici tek bağımlılık
  Google Fonts'tur (preconnect + `display=swap` ile optimize edilmiştir).
