(function(){
  "use strict";

  const GALLERY = [
    { src:'assets/img/is-01.webp', w:828, h:987, title:'Doğum Günü Boyama Atölyesi', alt:'Çocukların figür boyadığı doğum günü boyama atölyesi - boyama etkinliği - 3D Atölyemiz', tag:'Boyama Etkinliği' },
    { src:'assets/img/is-02.webp', w:1200, h:1200, title:'Kendin Boya Figür Atölyesi Anısı', alt:'Boyanmış Stitch ve ayı figürleriyle boyama atölyesi anısı - boyama etkinliği - 3D Atölyemiz', tag:'Boyama Etkinliği' },
    { src:'assets/img/is-03.webp', w:675, h:1200, title:'Galatasaray Hagi Forma Çerçevesi', alt:'Galatasaray Hagi 10 forma temalı 3D baskı çerçeve - hediyelik - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-04.webp', w:675, h:1200, title:'Ağaç Dallı Ayna Çerçevesi', alt:'Ağaç dalı motifli 3D baskı ayna çerçevesi - ev dekoru - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-05.webp', w:1200, h:1200, title:'Kişiye Özel Uluyan Kurt Figürü', alt:'İsim harfli uluyan kurt figürü, babalar günü hediyesi - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-06.webp', w:900, h:1200, title:'Samuray Büstü Figürü', alt:'Altın detaylı boyalı samuray büst figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-07.webp', w:904, h:1200, title:'Mirabel Figürü (Encanto)', alt:'Encanto filminden elle boyanmış Mirabel figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-08.webp', w:900, h:1200, title:'Etkinlik Alanında Figür Boyama', alt:'Etkinlik alanında aileler ile figür boyama çalışması - boyama etkinliği - 3D Atölyemiz', tag:'Boyama Etkinliği' },
    { src:'assets/img/is-09.webp', w:1080, h:1080, title:'Sprinku Figürü', alt:'Renkli detaylarla üretilmiş Sprinku koleksiyon figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-10.webp', w:900, h:1200, title:'Messi Kendin Boya Seti', alt:'Messi figürlü kendin boya seti, boyanmamış figür ve fırça - boyama seti - 3D Atölyemiz', tag:'Boyama Etkinliği' },
    { src:'assets/img/is-11.webp', w:900, h:1200, title:'Anneler Günü Özel Figürü', alt:'Anneler gününe özel tasarlanmış 3D baskı figür - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-12.webp', w:675, h:1200, title:'Aksiyon Karakter Figürü', alt:'Boyanmamış aksiyon karakteri 3D baskı figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-13.webp', w:904, h:1200, title:'Maşa ile Koca Ayı Figürü', alt:'Maşa ile Koca Ayı karakterlerinin 3D baskı figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-14.webp', w:891, h:1200, title:'Kişiye Özel Karikatür Figür', alt:'Yüz benzerlikli kaslı karikatür mini figür - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-15.webp', w:675, h:1200, title:'Kişiye Özel Kalpli Çift Figürü', alt:'Kalp tutan kişiye özel çift figürü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-16.webp', w:900, h:1200, title:'Kişiye Özel Chihuahua Figürü', alt:'Gerçekçi boyanmış Chihuahua evcil hayvan figürü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-17.webp', w:1024, h:1024, title:'Kişiye Özel Ofis Figürü', alt:'Ofis çalışanlarını temsil eden kişiye özel masaüstü figür - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-18.webp', w:900, h:1200, title:'Ramazan Temalı Ay Lambası', alt:'Ayet yazılı ışıklı ay şeklinde Ramazan dekoru - ev dekoru - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-19.webp', w:675, h:1200, title:'Kişiye Özel Selfie Figürü', alt:'Telefonla selfie çeken kişiye özel mini figür - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-20.webp', w:1179, h:976, title:'Zootropolis Yılan Figürü', alt:'Zootropolis temalı yılan karakteri 3D baskı figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-21.webp', w:1200, h:900, title:'Deniz Hayvanları Figür Seti', alt:'Renkli deniz hayvanı figürlerinden oluşan set - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-22.webp', w:900, h:1200, title:'Kişiye Özel Mini Figür Seti', alt:'Şövalye temalı ve günlük kıyafetli kişiye özel mini figür seti - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-23.webp', w:904, h:1200, title:'Kratos Chibi Figürü', alt:'God of War Kratos karakterinin chibi tarzı 3D baskı figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-24.webp', w:900, h:1200, title:'Kişiye Özel İsimli Fantastik Figür', alt:'İsim ve unvan yazılı kişiye özel fantastik karakter figürü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-25.webp', w:900, h:1200, title:'Detaylı Motosiklet Maketi', alt:'El boyaması detaylı 3D baskı motosiklet maketi - 3D baskı model - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-26.webp', w:900, h:1200, title:'Kişiye Özel Şık Çift Figürü', alt:'Şık kıyafetli kişiye özel çift figürü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-27.webp', w:1200, h:631, title:'Mercedes G63 Araba Maketi', alt:'Yeşil Mercedes G63 tarzı 3D baskı araba maketi - 3D baskı model - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-28.webp', w:900, h:1200, title:'Kişiye Özel Çift Figürü (Detay)', alt:'Kişiye özel çift figürünün yakın çekim detayı - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-29.webp', w:905, h:1200, title:'Zootropolis Temalı Pasta Süsü', alt:'Zootropolis karakterli kişiye özel doğum günü pasta süsü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-30.webp', w:900, h:1200, title:'Kişiye Özel Anime Karakter Figürü', alt:'İsim plaketli kişiye özel anime tarzı karakter figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-31.webp', w:1200, h:900, title:'Kişiye Özel Pop Tarzı Mini Figür', alt:'Pop tarzı boyanmış kişiye özel mini figür - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-32.webp', w:960, h:1200, title:'Kişiye Özel ARTOPOP Aile Figürü', alt:'Fotoğraftan üretilen kişiye özel ARTOPOP aile figürleri - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-33.webp', w:675, h:1200, title:'Küçük Prens Figürü', alt:'Küçük Prens ve tilki karakterlerinin 3D baskı figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-34.webp', w:675, h:1200, title:'Honda Civic Araba Maketi', alt:'Gri renkli Honda Civic 3D baskı araba maketi - 3D baskı model - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-35.webp', w:675, h:1200, title:'Boyanmamış Dinozor Figürü', alt:'Etkinlik standında boyanmayı bekleyen triceratops figürü - boyama etkinliği - 3D Atölyemiz', tag:'Boyama Etkinliği' },
    { src:'assets/img/is-36.webp', w:675, h:1200, title:'Boyalı T-Rex Dinozor Figürü', alt:'Etkinlik standında elle boyanmış T-Rex dinozor figürü - boyama etkinliği - 3D Atölyemiz', tag:'Boyama Etkinliği' },
    { src:'assets/img/is-37.webp', w:1200, h:1200, title:'Minecraft Warden Figürü', alt:'Eklemli Minecraft Warden karakteri 3D baskı figürü - 3D baskı figür - 3D Atölyemiz', tag:'3D Baskı' },
    { src:'assets/img/is-38.webp', w:864, h:1146, title:'Kişiye Özel Kamp Ateşi Diorama Figürü', alt:'Kamp ateşi sahneli kişiye özel fantastik diorama figürü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-39.webp', w:960, h:1200, title:'Kişiye Özel Araba Standı', alt:'İsimli kişiye özel araba modeli standı - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-40.webp', w:900, h:1200, title:'Kişiye Özel Fransız Bulldog Figürü', alt:'Gerçekçi boyanmış Fransız bulldog evcil hayvan figürü - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' },
    { src:'assets/img/is-41.webp', w:1200, h:1200, title:'Kişiye Özel Terzi Temalı Pasta Süsü', alt:'Dikiş makinesi ve makas figürlü kişiye özel pasta süsü seti - kişiye özel hediye - 3D Atölyemiz', tag:'Hediyelik & Dekor' }
  ];

  const COLORS = ["#FF6B4A", "#2EC4B6", "#FFC94A", "#E24F2F"];

  function placeholder(text, color){
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">' +
      '<rect width="600" height="600" fill="' + color + '"/>' +
      '<text x="300" y="290" font-family="sans-serif" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">3D Atölyemiz</text>' +
      '<text x="300" y="335" font-family="sans-serif" font-size="18" fill="#ffffffd9" text-anchor="middle">' + text + '</text>' +
      '</svg>';
    return "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg);
  }

  var grid = document.getElementById("gallery-grid");
  if(!grid) return;

  GALLERY.forEach(function(item, i){
    var fig = document.createElement("div");
    fig.className = "gallery-item reveal";
    fig.innerHTML =
      '<div class="thumb">' +
        '<button type="button" data-index="' + i + '" aria-label="' + item.title + ' - büyüt">' +
          '<img src="' + item.src + '" alt="' + item.alt + '" width="' + item.w + '" height="' + item.h + '" loading="lazy" decoding="async">' +
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
    lbImg.src = grid.querySelectorAll("img")[current].src;
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
