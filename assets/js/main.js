(function(){
  "use strict";

  /* Sticky header shadow */
  var header = document.querySelector(".site-header");
  if(header){
    var onScroll = function(){
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, {passive:true});
  }

  /* Mobile menu: open/close, focus trap, Esc */
  var burger = document.querySelector(".hamburger");
  var menu = document.querySelector(".mobile-menu");
  if(burger && menu){
    var lastFocused = null;

    var getFocusable = function(){
      return Array.prototype.slice.call(
        menu.querySelectorAll('a[href], button:not([disabled])')
      );
    };

    var openMenu = function(){
      lastFocused = document.activeElement;
      menu.classList.add("is-open");
      menu.hidden = false;
      burger.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      var f = getFocusable();
      if(f.length) f[0].focus();
      document.addEventListener("keydown", onKeydown);
    };

    var closeMenu = function(){
      menu.classList.remove("is-open");
      burger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      document.removeEventListener("keydown", onKeydown);
      setTimeout(function(){ menu.hidden = true; }, 250);
      if(lastFocused) lastFocused.focus();
    };

    var onKeydown = function(e){
      if(e.key === "Escape"){ closeMenu(); return; }
      if(e.key === "Tab"){
        var f = getFocusable();
        if(!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if(e.shiftKey && document.activeElement === first){
          e.preventDefault(); last.focus();
        } else if(!e.shiftKey && document.activeElement === last){
          e.preventDefault(); first.focus();
        }
      }
    };

    burger.addEventListener("click", function(){
      var expanded = burger.getAttribute("aria-expanded") === "true";
      expanded ? closeMenu() : openMenu();
    });
    menu.querySelectorAll("a").forEach(function(a){
      a.addEventListener("click", closeMenu);
    });
    var closeBtn = menu.querySelector(".mobile-menu-close");
    if(closeBtn) closeBtn.addEventListener("click", closeMenu);
  }

  /* Reveal on scroll */
  var reveals = document.querySelectorAll(".reveal");
  if("IntersectionObserver" in window && reveals.length){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry, i){
        if(entry.isIntersecting){
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, {threshold:0.15, rootMargin:"0px 0px -40px 0px"});
    reveals.forEach(function(el, i){
      el.style.transitionDelay = (i % 6) * 60 + "ms";
      io.observe(el);
    });
  } else {
    reveals.forEach(function(el){ el.classList.add("is-visible"); });
  }

  /* KPI counters: count up from 0 when scrolled into view */
  var statNums = document.querySelectorAll(".stat-num");
  if(statNums.length){
    var animateCount = function(el){
      var target = parseInt(el.getAttribute("data-target"), 10) || 0;
      var suffix = el.getAttribute("data-suffix") || "";
      var duration = 1400;
      var start = null;
      var step = function(ts){
        if(start === null) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(eased * target).toLocaleString("tr-TR") + suffix;
        if(progress < 1) requestAnimationFrame(step);
        else el.textContent = target.toLocaleString("tr-TR") + suffix;
      };
      requestAnimationFrame(step);
    };
    if("IntersectionObserver" in window){
      var statIo = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            animateCount(entry.target);
            statIo.unobserve(entry.target);
          }
        });
      }, {threshold:0.4});
      statNums.forEach(function(el){ statIo.observe(el); });
    } else {
      statNums.forEach(function(el){
        el.textContent = (el.getAttribute("data-target") || "0") + (el.getAttribute("data-suffix") || "");
      });
    }
  }

  /* FAB soft entrance */
  var fab = document.querySelector(".fab");
  if(fab){
    setTimeout(function(){ fab.classList.add("is-visible"); }, 3000);
  }
})();
