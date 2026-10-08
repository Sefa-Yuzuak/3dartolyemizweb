(function(){
  "use strict";

  const GALLERY = [
    { src:'assets/img/atolye/bambu-lab-yazici-ams.webp', w:900, h:1200, title:'Çok renkli baskı ünitesi (AMS) takılı yazıcı', alt:'Atölyedeki Bambu Lab 3D yazıcı ve üstündeki çok renkli filament ünitesi - 3dartolyemiz', tag:'Atölye' },
    { src:'assets/img/urun/renault-megane-araba-maketi.webp', w:900, h:1200, title:'Renault Megane Araba Maketi', alt:'Beyaz Renault Megane araba maketi', tag:'Maket' },
    { src:'assets/img/urun/porsche-911-maketi.webp', w:900, h:1200, title:'Porsche 911 Maketi', alt:'Porsche 911 Maketi — 3dartolyemiz atölyesinde 3D baskı', tag:'Maket' },
    { src:'assets/img/urun/mercedes-g63-maketi.webp', w:900, h:1200, title:'Mercedes G63 AMG Maketi', alt:'Mercedes G63 AMG Maketi — 3dartolyemiz atölyesinde 3D baskı', tag:'Maket' },
    { src:'assets/img/atolye/ams-filament-rafi.webp', w:900, h:1200, title:'Filament rafı ve çok renkli besleme ünitesi', alt:'Bambu Lab AMS ünitesindeki filament makaraları ve önde 3D baskı ejderha figürü - 3dartolyemiz', tag:'Atölye' },
    { src:'assets/img/urun/cupra-araba-maketi-dioramali.webp', w:900, h:1200, title:'Cupra Araba Maketi (Dioramalı)', alt:'Diorama üzerinde Cupra araba maketi', tag:'Maket' },
    { src:'assets/img/urun/kisiye-ozel-kedi-figuru.webp', w:900, h:1200, title:'Kişiye Özel Kedi Figürü', alt:'Kişiye özel boyanmış kedi figürü', tag:'Figür' },
    { src:'assets/img/urun/pop-tarzi-futbolcu-figuru.webp', w:900, h:1200, title:'Pop Tarzı Futbolcu Figürü', alt:'Elle boyanmış pop tarzı futbolcu figürü ve boyasız hâli', tag:'Figür' },
    { src:'assets/img/atolye/ay-lamba-yazicida.webp', w:900, h:1200, title:'Ay görünümlü lamba, yazıcıdan çıkarken', alt:'3D yazıcının içinde yeni basılmış ay yüzeyi dokulu lamba gövdesi - 3dartolyemiz', tag:'Atölye' },
    { src:'assets/img/urun/venusaur-figuru.webp', w:900, h:1200, title:'Venusaur Figürü', alt:'Venusaur Figürü — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/urun/charmander-figuru.webp', w:900, h:1200, title:'Charmander Figürü', alt:'Charmander Figürü — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/urun/stitch-lamba.webp', w:900, h:1200, title:'Stitch Lamba', alt:'Stitch Lamba — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/atolye/filament-makaralari.webp', w:900, h:1200, title:'Filament makaraları', alt:'Üst üste dizilmiş sarı, gri, yeşil ve mavi filament makaraları - 3dartolyemiz', tag:'Atölye' },
    { src:'assets/img/urun/kedi-taki-kutusu.webp', w:900, h:1200, title:'Kedi Takı Kutusu', alt:'Kedi Takı Kutusu — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/urun/unicorn-taki-standi.webp', w:900, h:1200, title:'Unicorn Takı Standı', alt:'Unicorn Takı Standı — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/urun/gece-gunduz-taki-kutusu.webp', w:900, h:1200, title:'Gece ve Gündüz Takı Kutusu', alt:'Gece ve Gündüz Takı Kutusu — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/atolye/dilimleme-programi.webp', w:900, h:1200, title:'Baskıdan önce: dilimleme', alt:'Dizüstü bilgisayarda dilimleme programında açık figür modeli - 3dartolyemiz', tag:'Atölye' },
    { src:'assets/img/urun/yukari-bak-evi-maketi.webp', w:900, h:1200, title:'Yukarı Bak Evi Maketi', alt:'Yukarı Bak Evi Maketi — 3dartolyemiz atölyesinde 3D baskı', tag:'Maket' },
    { src:'assets/img/urun/walking-dead-figur-seti.webp', w:900, h:1200, title:'The Walking Dead Figür Seti', alt:'The Walking Dead Figür Seti — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/urun/eklemli-ejderha.webp', w:900, h:1200, title:'Eklemli Ejderha', alt:'Eklemli Ejderha — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/atolye/3d-modelleme-egitimi.webp', w:900, h:1200, title:'Modelleme eğitiminden', alt:'Sınıfta projeksiyonla gösterilen 3D modelleme programı ekranı - 3dartolyemiz', tag:'Atölye' },
    { src:'assets/img/urun/hollow-knight-figuru.webp', w:900, h:1200, title:'Hollow Knight Figürü', alt:'Hollow Knight Figürü — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/urun/donkey-kong-figuru.webp', w:900, h:1200, title:'Donkey Kong Figürü', alt:'Donkey Kong Figürü — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/urun/3d-katmanli-duvar-tablosu.webp', w:900, h:1200, title:'3D Katmanlı Duvar Tablosu', alt:'3D Katmanlı Duvar Tablosu — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/urun/bulbasaur-saksi.webp', w:900, h:1200, title:'Bulbasaur Saksı', alt:'Bulbasaur Saksı — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/urun/platform-9-3-4-masa-lambasi.webp', w:900, h:1200, title:'Platform 9¾ Masa Lambası', alt:'Platform 9¾ Masa Lambası — 3dartolyemiz atölyesinde 3D baskı', tag:'Ev & Dekor' },
    { src:'assets/img/urun/labubu-figuru.webp', w:900, h:1200, title:'Labubu Figürü', alt:'Labubu Figürü — 3dartolyemiz atölyesinde 3D baskı', tag:'Figür' },
    { src:'assets/img/urun/araba-logolu-isimli-anahtarlik.webp', w:900, h:1200, title:'Araba Logolu İsimli Anahtarlık', alt:'Kişiye özel isimli araba logolu anahtarlıklar', tag:'Anahtarlık' }
  ];

  const COLORS = ["#FF6B4A", "#2EC4B6", "#FFC94A", "#E24F2F"];

  function placeholder(text, color){
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">' +
      '<rect width="600" height="600" fill="' + color + '"/>' +
      '<text x="300" y="290" font-family="sans-serif" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">3dartolyemiz</text>' +
      '<text x="300" y="335" font-family="sans-serif" font-size="18" fill="#ffffffd9" text-anchor="middle">' + text + '</text>' +
      '</svg>';
    return "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg);
  }

  var grid = document.getElementById("gallery-grid");
  if(!grid) return;

  /* Izgara 15.09.2026'dan beri HTML'de hazir basili (41 gorsel JS'siz de
     okunabilsin diye). Hazirsa yalniz hata yedegini bagla, yeniden uretme. */
  var hazir = grid.querySelectorAll(".gallery-item").length === GALLERY.length;
  if(hazir){
    Array.prototype.forEach.call(grid.querySelectorAll("img"), function(img, i){
      img.addEventListener("error", function(){
        img.onerror = null;
        img.src = placeholder(GALLERY[i].tag, COLORS[i % COLORS.length]);
      });
    });
  }

  if(!hazir) GALLERY.forEach(function(item, i){
    var fig = document.createElement("div");
    fig.className = "gallery-item reveal";
    fig.innerHTML =
      '<div class="thumb">' +
        '<button type="button" data-index="' + i + '" aria-label="' + item.title + ' - büyüt">' +
          '<img src="' + item.src.replace(".webp", "-sm.webp") + '" data-full="' + item.src + '" alt="' + item.alt + '" width="' + item.w + '" height="' + item.h + '" loading="lazy" decoding="async">' +
        '</button>' +
        '<span class="tag">' + item.tag + '</span>' +
      '</div>' +
      '<p class="gallery-item-title">' + item.title + '</p>';
    var img = fig.querySelector("img");
    img.addEventListener("error", function(){
      img.onerror = null;
      img.src = placeholder(item.tag, COLORS[i % COLORS.length]);
    });
    grid.appendChild(fig);
  });

  /* Lightbox */
  var lightbox = document.getElementById("lightbox");
  if(!lightbox) return;
  var lbImg = lightbox.querySelector("img");
  var lbCaption = lightbox.querySelector("figcaption");
  var lbClose = lightbox.querySelector(".lightbox-close");
  var current = 0;
  var lastFocused = null;

  function show(index){
    current = (index + GALLERY.length) % GALLERY.length;
    var item = GALLERY[current];
    var t = grid.querySelectorAll("img")[current];
    lbImg.src = t.getAttribute("data-full") || t.src;
    lbImg.alt = item.alt;
    lbCaption.textContent = item.title;
  }

  function open(index){
    lastFocused = document.activeElement;
    show(index);
    lightbox.classList.add("is-open");
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
    lbClose.focus();
    document.addEventListener("keydown", onKey);
  }

  function close(){
    lightbox.classList.remove("is-open");
    lightbox.hidden = true;
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onKey);
    if(lastFocused) lastFocused.focus();
  }

  function onKey(e){
    if(e.key === "Escape") close();
    if(e.key === "ArrowRight") show(current + 1);
    if(e.key === "ArrowLeft") show(current - 1);
  }

  grid.addEventListener("click", function(e){
    var btn = e.target.closest("button[data-index]");
    if(btn) open(parseInt(btn.getAttribute("data-index"), 10));
  });
  lbClose.addEventListener("click", close);
  lightbox.querySelector(".lightbox-prev").addEventListener("click", function(){ show(current - 1); });
  lightbox.querySelector(".lightbox-next").addEventListener("click", function(){ show(current + 1); });
  lightbox.addEventListener("click", function(e){
    if(e.target === lightbox) close();
  });
})();
