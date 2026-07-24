(function(){
  "use strict";

  var GALLERY = [
    { src:"assets/img/is-01.jpg", alt:"Kişiye özel isimli 3D baskı gece lambası", tag:"3D Baskı" },
    { src:"assets/img/is-02.jpg", alt:"Sevgiliye özel 3D baskı fotoğraf çerçevesi", tag:"Hediyelik" },
    { src:"assets/img/is-03.jpg", alt:"Doğum günü boyama etkinliğinden kare, boyanan alçı figürler", tag:"Etkinlik" },
    { src:"assets/img/is-04.jpg", alt:"Masa üstü 3D baskı biblo ve dekor ürünü", tag:"Dekor" },
    { src:"assets/img/is-05.jpg", alt:"Çocuklara özel 3D baskı boyanabilir figür seti", tag:"Etkinlik" },
    { src:"assets/img/is-06.jpg", alt:"Kişiye özel isim yazılı anahtarlık 3D baskı", tag:"Hediyelik" },
    { src:"assets/img/is-07.jpg", alt:"Renkli 3D baskı saksı ve mini bitki dekoru", tag:"Dekor" },
    { src:"assets/img/is-08.jpg", alt:"Doğum günü partisinde boyama atölyesi masası", tag:"Etkinlik" },
    { src:"assets/img/is-09.jpg", alt:"3D baskı kişiye özel oyuncak figür", tag:"3D Baskı" },
    { src:"assets/img/is-10.jpg", alt:"El yapımı detaylarla boyanmış 3D baskı obje", tag:"3D Baskı" },
    { src:"assets/img/is-11.jpg", alt:"Sevgililer gününe özel 3D baskı hediyelik kutu", tag:"Hediyelik" },
    { src:"assets/img/is-12.jpg", alt:"Doğum günü etkinliğinde çocukların boyadığı figürler", tag:"Etkinlik" }
  ];

  var COLORS = ["#FF6B4A", "#2EC4B6", "#FFC94A", "#E24F2F"];

  function placeholder(text, color){
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">' +
      '<rect width="600" height="600" fill="' + color + '"/>' +
      '<rect x="24" y="24" width="552" height="552" rx="24" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="2"/>' +
      '<text x="300" y="290" font-family="sans-serif" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">3D Atölyemiz</text>' +
      '<text x="300" y="335" font-family="sans-serif" font-size="18" fill="rgba(255,255,255,.85)" text-anchor="middle">' + text + '</text>' +
      '</svg>';
    return "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg);
  }

  var grid = document.getElementById("gallery-grid");
  if(!grid) return;

  GALLERY.forEach(function(item, i){
    var fig = document.createElement("div");
    fig.className = "gallery-item reveal";
    fig.innerHTML =
      '<button type="button" data-index="' + i + '" aria-label="' + item.alt + ' - büyüt">' +
        '<img src="' + item.src + '" alt="' + item.alt + '" loading="lazy" decoding="async" width="600" height="600">' +
      '</button>' +
      '<span class="tag">' + item.tag + '</span>';
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
  var current = 0;
  var lastFocused = null;

  function show(index){
    current = (index + GALLERY.length) % GALLERY.length;
    var item = GALLERY[current];
    lbImg.src = grid.querySelectorAll("img")[current].src;
    lbImg.alt = item.alt;
    lbCaption.textContent = item.alt;
  }

  function open(index){
    lastFocused = document.activeElement;
    show(index);
    lightbox.classList.add("is-open");
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
    lightbox.querySelector(".lightbox-close").focus();
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
  lightbox.querySelector(".lightbox-close").addEventListener("click", close);
  lightbox.querySelector(".lightbox-prev").addEventListener("click", function(){ show(current - 1); });
  lightbox.querySelector(".lightbox-next").addEventListener("click", function(){ show(current + 1); });
  lightbox.addEventListener("click", function(e){
    if(e.target === lightbox) close();
  });
})();
