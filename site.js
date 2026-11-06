/* ============================================================
   Portfólio Carlos Mograph — comportamentos
   Reproduz as interações do template Aluro (Webflow IX2/IX3) com GSAP,
   ScrollTrigger, SplitText e Lenis. Tudo é melhoria progressiva: sem as
   bibliotecas, ou com movimento reduzido, a página continua inteira.
   ============================================================ */
(function () {
  "use strict";
  var raiz = document.documentElement;
  var reduz = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fino = window.matchMedia("(pointer: fine)").matches;
  var temGsap = !!(window.gsap && window.ScrollTrigger && window.SplitText);
  var animar = temGsap && raiz.classList.contains("js-anim");
  var WHATSAPP = "5575981251114";

  /* O CSS esconde o que vai entrar até esta classe chegar. */
  function liberar() { raiz.classList.add("anim-pronta"); }
  if (!animar) liberar();
  setTimeout(liberar, 3000); /* rede de segurança */

  /* --- rolagem suave (Lenis, mesmos números do template) --- */
  var lenis = null;
  if (window.Lenis && !reduz) {
    lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 0.6, gestureOrientation: "vertical", smoothTouch: false });
    if (temGsap) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      var quadro = function (t) { lenis.raf(t); requestAnimationFrame(quadro); };
      requestAnimationFrame(quadro);
    }
  }
  function rolarPara(alvo) {
    if (lenis) lenis.scrollTo(alvo, { duration: 1.2 });
    else alvo.scrollIntoView({ behavior: reduz ? "auto" : "smooth" });
  }

  /* --- menu do celular --- */
  var menu = document.getElementById("menu");
  var botaoMenu = document.querySelector("[data-menu]");
  function fecharMenu() {
    menu.classList.remove("aberto");
    botaoMenu.setAttribute("aria-expanded", "false");
  }
  botaoMenu.addEventListener("click", function () {
    var abre = !menu.classList.contains("aberto");
    menu.classList.toggle("aberto", abre);
    botaoMenu.setAttribute("aria-expanded", String(abre));
  });

  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      var alvo = id.length > 1 && document.querySelector(id);
      if (!alvo) return;
      e.preventDefault();
      fecharMenu();
      rolarPara(alvo);
    });
  });

  /* --- modo claro / escuro --- */
  var corTema = document.querySelector('meta[name="theme-color"]');
  function pintarTema() { corTema.content = raiz.classList.contains("modo-claro") ? "#FDF7E9" : "#151517"; }
  pintarTema();
  document.querySelector("[data-modo]").addEventListener("click", function () {
    var claro = raiz.classList.toggle("modo-claro");
    try { localStorage.setItem("crmo-modo", claro ? "claro" : "escuro"); } catch (e) {}
    pintarTema();
  });

  /* --- popup de contato: o envio vira uma mensagem pronta no WhatsApp --- */
  var popup = document.querySelector(".popup-contact");
  var form = document.getElementById("form-contato");
  var focoAntes = null;
  function abrirModal(modal) {
    focoAntes = document.activeElement;
    fecharMenu();
    modal.hidden = false;
    void modal.offsetWidth; /* aplica o display antes da transição de opacidade */
    modal.classList.add("aberto");
    if (lenis) lenis.stop();
  }
  function fecharModal(modal, depois) {
    modal.classList.remove("aberto");
    if (lenis) lenis.start();
    setTimeout(function () { modal.hidden = true; if (depois) depois(); }, 350);
    if (focoAntes) focoAntes.focus({ preventScroll: true });
  }
  function abrirContato(tipo) {
    if (tipo) form.tipo.value = tipo;
    abrirModal(popup);
    setTimeout(function () { form.nome.focus({ preventScroll: true }); }, 60);
  }
  function fecharContato() { fecharModal(popup); }
  document.querySelectorAll("[data-abrir-contato]").forEach(function (b) {
    b.addEventListener("click", function () { abrirContato(b.dataset.tipo); });
  });
  document.querySelectorAll("[data-fechar-contato]").forEach(function (b) {
    b.addEventListener("click", fecharContato);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !popup.hidden) fecharContato();
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var linhas = ["Oi Carlos! Vim pelo seu site.", "", "Nome: " + d.get("nome")];
    if (d.get("marca")) linhas.push("Empresa/perfil: " + d.get("marca"));
    linhas.push("Projeto: " + d.get("tipo"), "Prazo: " + d.get("prazo"));
    if (d.get("mensagem")) linhas.push("", d.get("mensagem"));
    window.open("https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(linhas.join("\n")), "_blank", "noopener");
    form.reset();
    fecharContato();
  });

  /* --- abas dos planos --- */
  document.querySelectorAll("[data-abas]").forEach(function (abas) {
    var botoes = abas.querySelectorAll('[role="tab"]');
    botoes.forEach(function (b) {
      b.addEventListener("click", function () {
        botoes.forEach(function (o) {
          var ativo = o === b;
          o.classList.toggle("ativo", ativo);
          o.setAttribute("aria-selected", String(ativo));
          document.getElementById(o.getAttribute("aria-controls")).hidden = !ativo;
        });
        /* um slider que estava escondido precisa medir de novo */
        window.dispatchEvent(new Event("resize"));
        if (animar) {
          gsap.fromTo("#" + b.getAttribute("aria-controls"), { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, ease: "power1.out" });
          ScrollTrigger.refresh();
        }
      });
    });
  });

  /* --- dúvidas: um aberto por vez --- */
  var faqs = document.querySelectorAll(".expandable-single");
  faqs.forEach(function (item) {
    var botao = item.querySelector(".expandable-top");
    botao.addEventListener("click", function () {
      var abre = !item.classList.contains("aberto");
      faqs.forEach(function (o) {
        o.classList.remove("aberto");
        o.querySelector(".expandable-top").setAttribute("aria-expanded", "false");
      });
      item.classList.toggle("aberto", abre);
      botao.setAttribute("aria-expanded", String(abre));
      if (temGsap) setTimeout(function () { ScrollTrigger.refresh(); }, 650);
    });
  });

  /* --- marquees: velocidade constante em px/s, seja qual for a largura --- */
  document.querySelectorAll(".marquee-track").forEach(function (trilha) {
    var vel = trilha.closest(".hero-marquee") ? 110 : trilha.closest(".logos-marquee") ? 40 : 60;
    function medir() {
      trilha.style.setProperty("--dur", (trilha.firstElementChild.offsetWidth / vel).toFixed(1) + "s");
    }
    medir();
    if (document.fonts) document.fonts.ready.then(medir);
    trilha.querySelectorAll("img").forEach(function (img) {
      if (!img.complete) img.addEventListener("load", medir);
    });
    window.addEventListener("load", medir);
  });

  /* --- vídeos do Vimeo em modo fundo (mudo, em loop, sem controles) ---
     Cada um entra por cima da sua capa só quando o player avisa que já está
     tocando. Se o Vimeo falhar ou bloquear, o aviso não chega e a capa fica. */
  window.addEventListener("message", function (ev) {
    if (ev.origin !== "https://player.vimeo.com") return;
    var d;
    try { d = typeof ev.data === "string" ? JSON.parse(ev.data) : ev.data; } catch (e) { return; }
    var q = d && d.player_id && document.getElementById(d.player_id);
    if (!q) return;
    if (d.event === "ready") {
      var janela = q.querySelector("iframe").contentWindow;
      var envia = function (m, v) { janela.postMessage(JSON.stringify({ method: m, value: v }), "https://player.vimeo.com"); };
      envia("addEventListener", "playProgress");
      /* o demoreel começa no segundo pedido (data-inicio) */
      if (q.dataset.inicio) { envia("setCurrentTime", Number(q.dataset.inicio)); envia("play"); }
    } else if (d.event === "playProgress") {
      /* com ponto de início, só mostra depois do salto: antes disso o
         player pode exibir a capa ou o primeiro quadro */
      var inicio = Number(q.dataset.inicio || 0);
      if (!inicio || (d.data && d.data.seconds >= inicio)) q.classList.add("tocando");
      if (inicio && d.data) {
        q._visto = Date.now();
        /* fecha o loop antes do fim: volta ao ponto de início, sem passar pela abertura */
        if (d.data.duration && d.data.seconds >= d.data.duration - 0.4) comandar(q, "setCurrentTime", inicio);
      }
    }
  });
  function videoDeFundo(caixa, id, hash, extra) {
    caixa.id = caixa.id || "vimeo-" + id;
    var f = document.createElement("iframe");
    f.title = "";
    f.setAttribute("aria-hidden", "true");
    f.setAttribute("tabindex", "-1");
    f.allow = "autoplay; fullscreen";
    f.referrerPolicy = "strict-origin-when-cross-origin";
    f.src = "https://player.vimeo.com/video/" + id + "?" + (hash ? "h=" + hash + "&" : "") +
      "background=1&dnt=1&player_id=" + caixa.id + (extra || "");
    caixa.appendChild(f);
  }

  /* hero: o demoreel começa a carregar junto com a página e toca sozinho */
  var reel = document.querySelector(".hero-reel[data-reel-vimeo]");
  if (reel) {
    videoDeFundo(reel, reel.dataset.reelVimeo, null, "&quality=1080p#t=" + (reel.dataset.inicio || 0) + "s");
  }

  /* vídeo de fundo fora da tela fica pausado: não gasta dados nem processador */
  function comandar(caixa, metodo, valor) {
    var f = caixa.querySelector("iframe");
    if (f) f.contentWindow.postMessage(JSON.stringify({ method: metodo, value: valor }), "https://player.vimeo.com");
  }
  var pausador = window.IntersectionObserver && new IntersectionObserver(function (es) {
    es.forEach(function (en) { comandar(en.target, en.isIntersecting ? "play" : "pause"); });
  });
  if (reel && pausador) pausador.observe(reel);
  /* vigia do demoreel: se parar de avançar com a home visível, retoma */
  if (reel) {
    var reelNaTela = true;
    if (window.IntersectionObserver) new IntersectionObserver(function (es) {
      reelNaTela = es[0].isIntersecting;
      reel._visto = Date.now();
    }).observe(reel);
    setInterval(function () {
      if (!reelNaTela || document.hidden || !reel._visto || Date.now() - reel._visto < 3000) return;
      reel._visto = Date.now();
      comandar(reel, "setCurrentTime", Number(reel.dataset.inicio || 0));
      comandar(reel, "play");
    }, 1000);
    document.addEventListener("visibilitychange", function () {
      reel._visto = Date.now();
      if (!document.hidden && reelNaTela) comandar(reel, "play");
    });
  }

  /* pastas e projetos: no hover a capa vira a prévia animada do trabalho */
  if (fino && !reduz) {
    document.querySelectorAll(".pasta img[data-anim], .pasta-projeto img[data-anim]").forEach(function (img) {
      var capa = img.getAttribute("src"), cartao = img.closest(".pasta, .pasta-projeto");
      cartao.addEventListener("pointerenter", function () { img.src = img.dataset.anim; });
      cartao.addEventListener("pointerleave", function () { img.src = capa; });
    });
  }

  /* --- mosaico: o vídeo do Vimeo (modo fundo: mudo, em loop, sem controles)
     só é criado quando o quadro chega perto da tela; até lá fica a capa. --- */
  /* vídeos do próprio site no mosaico: só baixam perto da tela e pausam fora dela */
  var locais = document.querySelectorAll(".mosaico-midia video[data-src]");
  if (locais.length && window.IntersectionObserver) {
    var obsLocal = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) {
          if (!v.getAttribute("src")) v.src = v.dataset.src;
          if (!reduz) v.play().catch(function () {});
        } else {
          v.pause();
        }
      });
    }, { rootMargin: "200px 0px" });
    locais.forEach(function (v) { obsLocal.observe(v); });
  }

  var quadros = document.querySelectorAll(".mosaico-midia[data-vimeo]");
  if (quadros.length && !reduz && window.IntersectionObserver) {
    var vimeo = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        vimeo.unobserve(en.target);
        videoDeFundo(en.target, en.target.dataset.vimeo, en.target.dataset.hash);
        if (pausador) pausador.observe(en.target);
      });
    }, { rootMargin: "200px 0px" });
    quadros.forEach(function (q) { vimeo.observe(q); });
  }

  /* --- sliders ---
     Todos os slides dividem a mesma célula; cada um vai para
     (distância até o atual) × (largura + vão). Quem dá a volta pelo
     outro lado troca de ponta sem transição, fora da área visível. */
  document.querySelectorAll("[data-slider]").forEach(function (caixa) {
    var mascara = caixa.querySelector("[data-mascara]");
    var slides = [].slice.call(mascara.children);
    var n = slides.length, atual = 0, timer = null, sobre = false, visivel = false;
    var atraso = (parseInt(caixa.dataset.delay, 10) || 3000) + 750;
    var pontos = [];

    var trilhaPontos = caixa.querySelector("[data-pontos]");
    if (trilhaPontos) slides.forEach(function (_, i) {
      var p = document.createElement("button");
      p.type = "button";
      p.setAttribute("aria-label", "Ir para o trabalho " + (i + 1));
      p.addEventListener("click", function () { ir(i); reiniciar(); });
      trilhaPontos.appendChild(p);
      pontos.push(p);
    });

    function posicionar(anima) {
      var passo = slides[0].offsetWidth + (parseFloat(getComputedStyle(mascara).columnGap) || 0);
      slides.forEach(function (s, i) {
        var d = i - atual;
        if (d > n / 2) d -= n;
        if (d < -n / 2) d += n;
        var salto = s._d !== undefined && Math.abs(d - s._d) > 1;
        s.style.transition = !anima || salto ? "none" : "";
        s.style.transform = "translateX(" + d * passo + "px)";
        s.classList.toggle("ativo", d === 0);
        /* a prévia animada só roda (e só baixa) no slide da frente */
        var img = s.querySelector("img[data-anim]");
        if (img) {
          if (!img.dataset.capa) img.dataset.capa = img.getAttribute("src");
          var quer = d === 0 && !reduz ? img.dataset.anim : img.dataset.capa;
          if (img.getAttribute("src") !== quer) img.src = quer;
        }
        s.setAttribute("aria-hidden", String(d !== 0));
        if (s.tagName === "A") s.tabIndex = d === 0 ? 0 : -1;
        s._d = d;
      });
      pontos.forEach(function (p, i) { p.setAttribute("aria-current", String(i === atual)); });
    }
    function ir(i) { atual = (i + n) % n; posicionar(true); }
    function reiniciar() {
      clearInterval(timer);
      if (reduz || sobre || !visivel || document.hidden) return;
      timer = setInterval(function () { ir(atual + 1); }, atraso);
    }

    caixa.querySelector("[data-proximo]").addEventListener("click", function () { ir(atual + 1); reiniciar(); });
    caixa.querySelector("[data-anterior]").addEventListener("click", function () { ir(atual - 1); reiniciar(); });
    caixa.addEventListener("pointerenter", function () { sobre = true; reiniciar(); });
    caixa.addEventListener("pointerleave", function () { sobre = false; reiniciar(); });
    document.addEventListener("visibilitychange", reiniciar);
    new IntersectionObserver(function (es) { visivel = es[0].isIntersecting; reiniciar(); }).observe(caixa);

    /* arrastar no toque e no mouse */
    var x0 = null, arrastou = false;
    mascara.querySelectorAll("img").forEach(function (img) { img.draggable = false; });
    mascara.addEventListener("pointerdown", function (e) { x0 = e.clientX; arrastou = false; });
    mascara.addEventListener("pointerup", function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0;
      x0 = null;
      if (Math.abs(dx) > 8) arrastou = true;
      if (Math.abs(dx) > 40) { ir(atual + (dx < 0 ? 1 : -1)); reiniciar(); }
    });
    /* clique num vizinho traz ele para o centro em vez de abrir o link */
    mascara.addEventListener("click", function (e) {
      var s = e.target.closest("[data-mascara] > *");
      if (arrastou) { e.preventDefault(); arrastou = false; return; }
      if (s && !s.classList.contains("ativo")) { e.preventDefault(); ir(slides.indexOf(s)); reiniciar(); }
    });

    window.addEventListener("resize", function () { posicionar(false); });
    posicionar(false);
  });

  /* --- ímã: botões seguem o ponteiro (só mouse, só com GSAP) --- */
  if (temGsap && fino && !reduz) {
    document.querySelectorAll("[data-magnet]").forEach(function (el) {
      var lim = el.dataset.magnet.split(",").map(Number);
      var xTo = gsap.quickTo(el, "x", { duration: 0.8, ease: "power3" });
      var yTo = gsap.quickTo(el, "y", { duration: 0.8, ease: "power3" });
      var mascara = el.querySelector(".button-text-mask");
      var txTo = mascara && gsap.quickTo(mascara, "x", { duration: 0.6, ease: "power3" });
      var tyTo = mascara && gsap.quickTo(mascara, "y", { duration: 0.6, ease: "power3" });
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        xTo(px * 2 * lim[0]);
        yTo(py * 2 * lim[1]);
        if (mascara) { txTo(px * 40); tyTo(py * 20); }
      });
      el.addEventListener("pointerleave", function () {
        xTo(0); yTo(0);
        if (mascara) { txTo(0); tyTo(0); }
      });
    });
  }

  if (!animar) return;
  gsap.registerPlugin(ScrollTrigger, SplitText);
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(montarAnimacoes);

  function montarAnimacoes() {
    /* letras sobem e a cópia entra por baixo (botões, nav, rodapé) */
    function rolarLetras(gatilho, texto, y, opcoes) {
      var letras = new SplitText(texto, { type: "chars", tag: "span" }).chars;
      var tl = gsap.timeline({ paused: true }).to(letras, Object.assign({ y: y }, opcoes), 0);
      gatilho.addEventListener("mouseenter", function () { tl.play(); });
      gatilho.addEventListener("mouseleave", function () { tl.reverse(); });
      return tl;
    }
    document.querySelectorAll("[button]").forEach(function (b) {
      var tl = rolarLetras(b, b.querySelector("[button-text]"), "-1.5em", { duration: 0.635, stagger: { amount: 0.1 }, ease: "expo.out" });
      tl.to(b.querySelector("[button-bg]"), { scale: 0.95, duration: 0.5, ease: "power2.out" }, 0);
    });
    document.querySelectorAll(".nav-link:not(.nav-icone)").forEach(function (a) {
      rolarLetras(a, a.querySelector("[text]"), "-1.25em", { duration: 0.4, stagger: 0.02, ease: "power2.inOut" });
    });
    document.querySelectorAll(".footer-link").forEach(function (a) {
      rolarLetras(a, a, "-1.25em", { duration: 0.4, stagger: 0.02, ease: "power2.inOut" });
    });

    /* títulos: palavras sobem de dentro de uma máscara ao entrar na tela */
    document.querySelectorAll("[heading-animation]").forEach(function (caixa) {
      [].forEach.call(caixa.children, function (filho) {
        var partes = new SplitText(filho, { type: "words", mask: "words", tag: "span" });
        gsap.from(partes.words, {
          yPercent: 105, opacity: 0, duration: 0.6, stagger: 0.1, ease: "power2.out",
          scrollTrigger: { trigger: caixa, start: "top 92%", once: true }
        });
      });
    });

    /* entrada do hero (só na home) */
    if (document.querySelector(".hero-nome")) {
    var nome = new SplitText(".hero-nome", { type: "chars", mask: "chars", tag: "span" });
    var sub = new SplitText(".hero-sub", { type: "words", mask: "words", tag: "span" });
    gsap.timeline()
      .from(".hero-label", { yPercent: 100, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.1)
      .from(nome.chars, { yPercent: 105, duration: 0.9, stagger: 0.035, ease: "expo.out" }, 0.2)
      .from(sub.words, { yPercent: 100, duration: 0.75, stagger: 0.03, ease: "power3.out" }, 0.6)
      .from(".hero-prova, .hero-acoes > *", { y: 16, opacity: 0, duration: 0.7, stagger: 0.1, ease: "power3.out" }, 0.8);

    /* o fundo do hero sobe devagar enquanto a página rola */
    gsap.to(".hero-reel", { yPercent: 18, ease: "none",
      scrollTrigger: { trigger: ".hero-section", start: "top top", end: "bottom top", scrub: true } });
    }


    /* desfoque que assenta (Blur In / General) */
    gsap.utils.toArray("[data-blur]").forEach(function (el) {
      gsap.fromTo(el, { filter: "blur(12px)", opacity: 0 }, {
        filter: "blur(0px)", opacity: 1, duration: 1, delay: 0.4, ease: "circ.out", clearProps: "filter",
        scrollTrigger: { trigger: el, start: "top 88%", once: true }
      });
    });
    gsap.utils.toArray("[data-fade]").forEach(function (el) {
      gsap.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 1, ease: "power4.out",
        scrollTrigger: { trigger: el, start: "top 94%", once: true } });
    });
    if (document.querySelector(".section-divider")) gsap.fromTo(".section-divider", { width: "0%" }, { width: "100%", duration: 1, ease: "sine.out",
      scrollTrigger: { trigger: ".section-divider", start: "top 96%", once: true } });

    liberar();
    ScrollTrigger.refresh();
  }
})();
