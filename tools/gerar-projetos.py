# Gera a área de projetos do site, no formato da referência (luizmotion.com.br):
#   projetos/index.html          as pastas
#   projetos/<pasta>/index.html  os projetos de uma pasta
#   projetos/<slug>/index.html   a apresentação de cada projeto (título, vídeo ou
#                                capa, destaques, ficha, texto e "próximo projeto")
#
#   python tools/gerar-projetos.py
#
# Os textos e os dados ficam todos aqui
# embaixo; navegação, popup de contato e rodapé são copiados do index.html,
# então qualquer mudança neles chega às páginas na próxima geração.

import html
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
e = html.escape

# ------------------------------------------------------------------
# MOTION — textos "O projeto" vêm do carlosmograph.myportfolio.com
# ------------------------------------------------------------------
MOTION = [
    dict(slug="lotenet", nome="Lotenet", cliente="Lotenet", categoria="Institucional", ano="2026",
         duracao="1:00", formato="16:9 horizontal", capa="motion/lotenet-capa.webp",
         video=("1195043718", "b5a3938e82"),
         texto="Motion design desenvolvido para a Lotenet, o projeto foi pensado para criar ritmo e impacto visual, "
               "destacando números, pessoas e momentos importantes através de animações fluidas, cortes rápidos e "
               "composições cinematográficas. O resultado é uma peça institucional moderna, estratégica e envolvente, "
               "criada para fortalecer o posicionamento da marca e gerar identificação com o público."),
    dict(slug="casas-bahia", nome="Casas Bahia", cliente="Casas Bahia (projeto de estudo)", categoria="Motion ads", ano="2025",
         duracao="0:15", formato="16:9 horizontal", capa="motion/casasbahia-capa.webp",
         video=("1090293626", "afb7e16c84"),
         grupos=[("Styleframes", "Os quadros-chave antes da animação.", [f"frame-{i:02d}.webp" for i in range(1, 9)])],
         texto="Este projeto foi desenvolvido como um exercício de criação para simular uma campanha promocional da "
               "Casas Bahia, com foco em Black Friday. A proposta foi explorar elementos visuais da identidade da marca, "
               "utilizando tipografia impactante, cores vibrantes e animações dinâmicas para transmitir urgência e "
               "atratividade, características típicas de campanhas promocionais de grande impacto."),
    dict(slug="quero-delivery", nome="Quero Delivery", cliente="Quero Delivery (projeto de estudo)", categoria="Motion ads", ano="2024",
         duracao="0:20", formato="16:9 horizontal", capa="motion/quero-capa.webp",
         video=("1038007604", "3d5d3b8683"),
         grupos=[("Styleframes", "Os quadros-chave antes da animação.", [f"frame-{i:02d}.webp" for i in range(1, 10)]),
                 ("Moodboard e bastidores", "Referências e o projeto aberto no After Effects.", [f"frame-{i:02d}.webp" for i in range(10, 14)])],
         texto="Este projeto foi criado como um exercício para simular uma peça publicitária da Quero Delivery, com o "
               "objetivo de apresentar os principais benefícios do aplicativo de forma clara, atrativa e dinâmica. A "
               "proposta visual explora ilustrações simples, cores vibrantes e uma narrativa direta, reforçando a agilidade "
               "e praticidade do serviço de delivery. O vídeo foi pensado para funcionar tanto em redes sociais quanto em "
               "campanhas digitais, com foco em comunicação rápida e eficaz."),
    dict(slug="dj-thiago", nome="DJ Thiago", cliente="DJ Thiago", categoria="Logo reveal", ano="2025",
         duracao="0:13", formato="16:9 horizontal", capa="motion/djthiago-capa.webp",
         video=("1100180853", None),
         grupos=[("Styleframes", "A marca aplicada no universo do DJ.", [f"frame-{i:02d}.webp" for i in range(1, 4)])],
         texto="Este projeto foi criado para apresentar a nova identidade visual do cliente de forma dinâmica e "
               "envolvente. A animação destaca a logomarca de maneira impactante, reforçando sua presença e conexão com o "
               "público por meio de um vídeo curto. A logo foi utilizada em contexto real, integrando-se diretamente ao "
               "universo do DJ e valorizando seu trabalho de forma autêntica."),
    dict(slug="clinica-verassi", nome="Clínica Verassi", cliente="Clínica Verassi", categoria="Logo reveal", ano="2026",
         duracao="0:08", formato="16:9 horizontal", capa="motion/verassi-capa.webp",
         video=("1195055816", "10f7402f55"),
         grupos=[("Destaques da animação", "Os momentos mais animados, em loop.", ["frame-01.webp", "frame-02.webp"])],
         texto="Logo reveal desenvolvido para a Verassi com uma estética sofisticada e contemporânea, utilizando "
               "movimentos fluidos, iluminação refinada e composições minimalistas para transmitir exclusividade, "
               "elegância e presença de marca de forma impactante e memorável."),
    dict(slug="daniela-souza", nome="Daniela Souza", cliente="Daniela Souza Arquitetura", categoria="Logo reveal", ano="2026",
         duracao="0:10", formato="16:9 horizontal", capa="motion/daniela-capa.webp",
         video=("1195052255", "15bc744838"),
         grupos=[("Destaques da animação", "Os momentos mais animados, em loop.", [f"frame-{i:02d}.webp" for i in range(1, 4)])],
         texto="Logo reveal minimalista desenvolvido para fortalecer a identidade visual da marca com elegância, ritmo e "
               "impacto. A animação utiliza movimentos fluidos e uma estética moderna para criar uma apresentação "
               "sofisticada e memorável."),
    dict(slug="louvre", nome="Louvre", cliente="Louvre", categoria="Logo reveal", ano="2026",
         duracao="0:10", formato="4:5 vertical", capa="motion/louvre-capa.webp", proporcao="4/5",
         video=("1195050547", "6af21349a5"),
         extras=[("1195050777", "0d079fdcb8", "16/9"), ("1195050524", "5959b4b494", "4/5"), ("1195050480", "9d9faf6b81", "4/5")],
         texto="Animação com transições fluidas para criar uma experiência moderna e envolvente. O projeto explora ritmo, "
               "contraste e identidade visual de forma estratégica, resultando em uma peça motion elegante e energética, "
               "criada para fortalecer a presença da marca e prender a atenção do público do início ao fim."),
    dict(slug="eleva", nome="Eleva", cliente="Eleva", categoria="Motion reveal", ano="2026",
         duracao="0:07", formato="4:5 vertical", capa="motion/eleva-capa.webp", proporcao="4/5",
         video=("1195047577", "2c927126c2"),
         extras=[("1195048100", "a852eeea64", "16/9"), ("1195047601", "366f7f6250", "4/5"), ("1195048218", "8094c8697b", "1/1"),
                 ("1195047594", "0ce0aca6e1", "4/5")],
         texto="Logo reveal desenvolvido para a Eleva, com foco em sofisticação, impacto visual e construção de marca. A "
               "animação utiliza movimentos fluidos, iluminação cinematográfica e transições minimalistas para valorizar a "
               "identidade visual da empresa de forma elegante e moderna."),
    dict(slug="orconalt", nome="Orconalt", cliente="Orconalt Gestão Empresarial", categoria="Logo reveal", ano="2026",
         duracao="0:10", formato="16:9 em 1440p", capa="projetos/orconalt/capa.webp",
         # vídeos curtos e sem som: tocam sozinhos, em loop
         mp4=("projetos/orconalt/orconalt-chumbo.mp4", "projetos/orconalt/capa.webp"), mp4_auto=True,
         mp4_serie=("Mais versões", "A assinatura nos dois fundos da marca, e o símbolo sozinho.", [
             ("projetos/orconalt/orconalt-offwhite.mp4", "projetos/orconalt/capa-offwhite.webp", "Versão off-white"),
             ("projetos/orconalt/simbolo-escuro.mp4", "projetos/orconalt/capa-simbolo-escuro.webp", "Símbolo, fundo chumbo"),
             ("projetos/orconalt/simbolo-claro.mp4", "projetos/orconalt/capa-simbolo-claro.webp", "Símbolo, fundo off-white")]),
         grupos=[("Construção do símbolo", "Das linhas do desenho à marca completa.", [f"frame-{i:02d}.webp" for i in range(1, 5)])],
         texto="Logo reveal para a Orconalt, de gestão empresarial. O símbolo nasce das linhas do próprio desenho, ganha "
               "peso e abre espaço para o nome da marca. A animação foi entregue nos dois fundos da identidade, chumbo e "
               "off-white, e também só com o símbolo, para vinhetas e aplicações curtas."),
    dict(slug="orbion-saas", nome="Orbion Place SaaS", cliente="Orbion Place", categoria="Motion SaaS", ano="2026",
         duracao="0:26", formato="16:9 horizontal e 9:16 vertical", capa="projetos/orbion-saas/capa.webp",
         # vídeos hospedados no próprio site (MP4 comprimido), não no Vimeo
         mp4=("projetos/orbion-saas/orbion-horizontal.mp4", "projetos/orbion-saas/capa.webp"),
         mp4_extras=[("Versão vertical", "A mesma animação em 9:16, para Reels e Stories.",
                      "projetos/orbion-saas/orbion-vertical.mp4", "projetos/orbion-saas/capa-vertical.webp", "9/16")],
         grupos=[("Styleframes", "Uma ideia por cena.", [f"frame-{i:02d}.webp" for i in range(1, 9)]),
                 ("Moodboard", "As referências que guiaram a direção visual.", ["moodboard.webp"], "largo")],
         texto="A Orbion Place é um sistema que mostra para quem vende em marketplace quanto realmente sobra de lucro "
               "em cada produto. O desafio era mostrar um dashboard cheio de informação sem cansar quem assiste. A "
               "solução foi mostrar uma coisa por vez: cada cena explica uma ideia só, como quando você conta algo "
               "difícil para uma criança e vai por partes."),
    dict(slug="orbion-place", nome="Orbion Place", cliente="Orbion Place", categoria="Looping", ano="2026",
         duracao="Loop", formato="16:9 horizontal", capa="motion/orbion-capa.webp",
         abertura="projetos/orbion-place/frame-01.webp",
         grupos=[("Destaques da animação", "Os loops, um a um.", [f"frame-{i:02d}.webp" for i in range(2, 6)])],
         texto="Animação visual desenvolvida com foco em formas, contraste e movimento minimalista, explorando uma direção "
               "de arte moderna e vibrante para criar uma composição dinâmica, elegante e memorável."),
]

# ------------------------------------------------------------------
# SOCIAL MEDIA — posts vêm do Behance; os textos são descrições do que
# aparece nos posts e precisam da revisão do Carlos.
# ------------------------------------------------------------------
SOCIAL = [
    dict(slug="biomundo", nome="BioMundo", setor="Saúde natural", ano="2026", pecas=15,
         behance="254764033/Social-Media-19-BioMundo", capa="social/biomundo.webp",
         texto="Feed para a BioMundo, de produtos naturais, com posts que explicam suplementos e alimentação natural "
               "de forma simples, sempre com pessoas reais e o verde da marca em destaque."),
    dict(slug="peralta", nome="Restaurante Péralta", setor="Gastronomia", ano="2025", pecas=21,
         behance="222909033/Social-Media-06-Restaurante-Pralta", capa="social/peralta.webp",
         texto="Posts para o Restaurante Péralta com os pratos no centro: fotos que abrem o apetite, tipografia forte "
               "e chamadas para o cardápio."),
    dict(slug="localize", nome="Localize", setor="Segurança eletrônica", ano="2025", pecas=13,
         behance="231379525/Social-Media-14-Localize-Monitoramentos", capa="social/localize.webp",
         texto="Comunicação para a Localize Monitoramentos: controle de acesso, rastreamento veicular, alarmes e câmeras "
               "explicados em posts claros, no azul e no verde da marca."),
    dict(slug="big-valenca", nome="Big Valença", setor="Varejo", ano="2025", pecas=27,
         behance="231378371/Social-Media-12-Big-Valenca", capa="social/big-valenca.webp",
         texto="Posts para o supermercado Big, em Valença, que transformam ofertas e utilidades do dia a dia em "
               "conversa, com o preço em destaque."),
    dict(slug="taina-oliveira", nome="Tainá Oliveira", setor="Psico-oncologia", ano="2025", pecas=16,
         behance="225443711/Social-Media-07-Taina-Oliveira-Psico-Oncologista", capa="social/taina-oliveira.webp",
         texto="Feed da psico-oncologista Tainá Oliveira, com uma linha visual roxa e acolhedora para falar de cuidados "
               "paliativos e saúde emocional com delicadeza."),
    dict(slug="br-pneus", nome="Br Pneus", setor="Automotivo", ano="2025", pecas=22,
         behance="231377867/Social-Media-11-Br-Pneus-Oficina", capa="social/br-pneus.webp",
         texto="Posts para a Br Pneus, oficina de pneus e serviços automotivos, com fotos da equipe e chamadas diretas "
               "para o cliente."),
    dict(slug="clinica-nape", nome="Clínica Nape", setor="Saúde infantil", ano="2025", pecas=33,
         behance="231379211/Social-Media-13-Clinica-Nape", capa="social/clinica-nape.webp",
         texto="Comunicação da Clínica Nape voltada a pais e mães: temas de saúde infantil com fotos acolhedoras e a "
               "criança no centro de cada peça."),
    dict(slug="dra-luana-cafe", nome="Dra. Luana Café", setor="Saúde", ano="2025", pecas=53,
         behance="231376255/Social-Media-09-Dra-Luana-Caf", capa="social/dra-luana-cafe.webp",
         texto="Posts da Dra. Luana Café pensados para famílias com bebês: informação de saúde em linguagem próxima, "
               "com tons suaves."),
]

VIMEO = "https://player.vimeo.com/video/{}?{}title=0&byline=0&portrait=0&dnt=1"

# ------------------------------------------------------------------
# PASTAS da página /projetos — cada projeto entra numa pasta pelo slug.
# "imagem" é a capa que aparece no alto da pasta (com a prévia animada no hover);
# "frase" é o subtítulo dentro da pasta e "apoio", a descrição embaixo dele.
# ------------------------------------------------------------------
PASTAS = [
    dict(slug="motion-ads", nome="Motion ads", apoio="Anúncios para tráfego pago", frase="Anúncios que vendem",
         imagem="motion/casasbahia-capa.webp", anim="motion/casasbahia.webp",
         projetos=["casas-bahia", "quero-delivery"]),
    dict(slug="logo-reveal", nome="Logo reveal", apoio="Marcas em movimento", frase="Marcas que se movem",
         imagem="motion/djthiago-capa.webp", anim="motion/djthiago.webp",
         projetos=["orconalt", "dj-thiago", "clinica-verassi", "daniela-souza", "louvre", "eleva", "orbion-place"]),
    dict(slug="institucional", nome="Institucional", apoio="Vídeos de marca", frase="Marca em movimento",
         imagem="motion/lotenet-capa.webp", anim="motion/lotenet.webp",
         projetos=["orbion-saas", "lotenet"]),
    dict(slug="social-media", nome="Social media", apoio="Posts, carrosséis e feeds", frase="Feed com cara de marca",
         imagem="social/peralta.webp", anim=None,
         projetos=[p["slug"] for p in SOCIAL]),
]
PROJETOS = {p["slug"]: dict(p, tipo="motion") for p in MOTION}
PROJETOS.update({p["slug"]: dict(p, tipo="social") for p in SOCIAL})
PASTA_DE = {s: pasta for pasta in PASTAS for s in pasta["projetos"]}

# ------------------------------------------------------------------
# Peças compartilhadas, copiadas da home
# ------------------------------------------------------------------
home = (RAIZ / "index.html").read_text(encoding="utf-8")


def trecho(inicio, fim, incluir_fim=True):
    a = home.index(inicio)
    b = home.index(fim, a) + (len(fim) if incluir_fim else 0)
    return home[a:b]


def para_subpasta(bloco, raiz):
    """Ajusta os links da home para uma página que está `raiz` acima dela."""
    bloco = re.sub(r'href="#([a-z]+)"', lambda m: f'href="{raiz}index.html#{m.group(1)}"', bloco)
    return bloco.replace('"./', f'"{raiz}')


SPRITE = trecho('<svg width="0" height="0"', "</svg>")
NAV = trecho('<header class="master-navigation">', "</header>")
CONTATO = trecho("<!-- ============ POPUP DE CONTATO", "<!-- linhas verticais do fundo -->", incluir_fim=False)
GRADE = trecho('<div class="master-bg-grid"', "</div></div>")
BLUR = trecho('<div class="wrap-progressive-blur"', "</div>\n  </div>")
RODAPE = trecho("<!-- ============ RODAPÉ", "</footer>")
ICONE = trecho('<link rel="icon"', '">')
CABECA_FONTES = trecho('<link rel="preconnect" href="https://fonts.googleapis.com">', 'rel="stylesheet">')
SCRIPTS = trecho('<script src="https://cdn.jsdelivr.net/npm/gsap', '<script src="./site.js" defer></script>')


def casca(titulo, descricao, raiz, conteudo):
    """A página inteira: cabeça, navegação, contato, conteúdo, rodapé e scripts."""
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)} — Carlos Mograph</title>
<meta name="description" content="{e(descricao[:150])}">
<meta name="theme-color" content="#151517">
{para_subpasta(ICONE, raiz)}
<script>
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("js-anim");
  try {{ if (localStorage.getItem("crmo-modo") === "claro") document.documentElement.classList.add("modo-claro"); }} catch (e) {{}}
</script>
{CABECA_FONTES}
<link rel="stylesheet" href="{raiz}crmo.css">
<link rel="stylesheet" href="{raiz}site.css">
</head>
<body>

{SPRITE}

<div class="page-wrap">

  {para_subpasta(NAV, raiz)}

  {CONTATO}
  {GRADE}

  <main id="topo" class="projeto">
{conteudo}
  </main>

  {BLUR}

  {para_subpasta(RODAPE, raiz)}

</div>

{para_subpasta(SCRIPTS, raiz)}
</body>
</html>
'''


def topo(voltar_href, voltar, titulo, meta):
    return f'''    <section class="projeto-topo">
      <div class="main-container">
        <a class="projeto-voltar" href="{voltar_href}">&larr; {e(voltar)}</a>
        <div heading-animation><h1 class="projeto-nome">{e(titulo)}</h1></div>
        <p class="projeto-meta">{e(meta)}</p>
      </div>
    </section>'''


def ficha(itens):
    linhas = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in itens)
    return f'<dl class="ficha">{linhas}</dl>'


def iframe(vid, h, prop, titulo):
    return (f'<div class="video-frame" style="--proporcao:{prop}"><iframe src="{VIMEO.format(vid, f"h={h}&amp;" if h else "")}" '
            f'title="{e(titulo)}" loading="lazy" allow="autoplay; fullscreen; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>')


def video_local(arquivo, capa, prop, titulo, raiz, auto=False):
    """auto: vídeo curto e sem som, que toca sozinho em loop (logo reveal)."""
    modo = "autoplay muted loop " if auto else ""
    return (f'<div class="video-frame" style="--proporcao:{prop}"><video src="{raiz}assets/{arquivo}" poster="{raiz}assets/{capa}" '
            f'{modo}controls playsinline preload="metadata" title="{e(titulo)}"></video></div>')


def secao_titulo(titulo, apoio):
    return (f'<div class="projeto-secao-topo"><h2 class="projeto-rotulo">{e(titulo)}</h2>'
            f'<p class="projeto-apoio">{e(apoio)}</p></div>')


# ------------------------------------------------------------------
# Página de cada projeto
# ------------------------------------------------------------------
def pagina_projeto(p, proximo):
    raiz = "../../"
    pasta = PASTA_DE[p["slug"]]
    if p["tipo"] == "motion":
        meta = [p["cliente"].split(" (")[0], p["categoria"], p["ano"]]
        prop = p.get("proporcao", "16/9")
        if "video" in p:
            midia = iframe(*p["video"], prop, p["nome"])
        elif "mp4" in p:
            midia = video_local(*p["mp4"], prop, p["nome"], raiz, p.get("mp4_auto", False))
        else:
            midia = (f'<div class="video-frame" style="--proporcao:{prop}"><img src="{raiz}assets/{p["abertura"]}" '
                     f'alt="{e(p["nome"])}" loading="eager"></div>')
        blocos = []
        if p.get("extras"):
            vids = "".join(iframe(v, h, pr, f'{p["nome"]} — peça {i + 2}') for i, (v, h, pr) in enumerate(p["extras"]))
            blocos.append(f'<section class="projeto-bloco">{secao_titulo("Mais peças da série", "Cada versão da marca, no formato em que roda.")}'
                          f'<div class="projeto-videos">{vids}</div></section>')
        if p.get("mp4_serie"):
            titulo, apoio, itens = p["mp4_serie"]
            vids = "".join(f'<figure class="projeto-serie-item">{video_local(arq, cp, prop, rot, raiz, True)}'
                           f'<figcaption>{e(rot)}</figcaption></figure>' for arq, cp, rot in itens)
            blocos.append(f'<section class="projeto-bloco">{secao_titulo(titulo, apoio)}<div class="projeto-serie">{vids}</div></section>')
        for titulo, apoio, arquivo, capa, pr in p.get("mp4_extras", []):
            blocos.append(f'<section class="projeto-bloco">{secao_titulo(titulo, apoio)}'
                          f'<div class="projeto-video-unico">{video_local(arquivo, capa, pr, f"{p['nome']} — {titulo}", raiz)}</div></section>')
        # cada grupo: (título, apoio, arquivos) ou (título, apoio, arquivos, "largo") para uma imagem só, em largura total
        for titulo, apoio, arquivos, *largo in p.get("grupos", []):
            imgs = "".join(f'<img src="{raiz}assets/projetos/{p["slug"]}/{a}" alt="" loading="lazy">' for a in arquivos)
            classe = "projeto-frames largo" if largo else "projeto-frames"
            blocos.append(f'<section class="projeto-bloco">{secao_titulo(titulo, apoio)}<div class="{classe}">{imgs}</div></section>')
        dados = ficha([("Cliente", p["cliente"]), ("Categoria", p["categoria"]), ("Ano", p["ano"]),
                       ("Duração", p["duracao"]), ("Formato", p["formato"]),
                       ("Ferramentas", "After Effects · Premiere Pro")])
    else:
        meta = [p["setor"], "Social media", p["ano"]]
        midia = f'<div class="projeto-capa"><img src="{raiz}assets/{p["capa"]}" alt="Posts para {e(p["nome"])}" loading="eager"></div>'
        posts = "".join(f'<img src="{raiz}assets/projetos/{p["slug"]}/post-{i:02d}.webp" alt="" loading="lazy">' for i in range(1, 13))
        link = f'https://www.behance.net/gallery/{p["behance"]}'
        blocos = [f'<section class="projeto-bloco">{secao_titulo("Os posts", "Uma seleção do feed.")}'
                  f'<div class="projeto-posts">{posts}</div>'
                  f'<a class="cta-main secundario projeto-behance" button href="{link}" target="_blank" rel="noopener">'
                  f'<span class="button-text-mask"><span button-text class="button-text">Ver os {p["pecas"]} posts no Behance</span></span>'
                  f'<span button-bg class="button-bg"></span></a></section>']
        dados = ficha([("Cliente", p["nome"]), ("Setor", p["setor"]), ("Categoria", "Social media"), ("Ano", p["ano"]),
                       ("Peças", f'{p["pecas"]} posts'), ("Ferramentas", "Photoshop")])

    conteudo = f'''{topo(f'../{pasta["slug"]}/', f'Voltar para {pasta["nome"].lower()}', p["nome"], " · ".join(meta))}

    <section class="projeto-midia">
      <div class="main-container" data-blur>{midia}</div>
    </section>

    <div class="main-container">
      {"".join(blocos)}

      <section class="projeto-bloco projeto-sobre" data-fade>
        <div><h2 class="projeto-rotulo">Sobre o projeto</h2>{dados}</div>
        <div class="projeto-texto"><h3>O projeto</h3><p>{e(p["texto"])}</p></div>
      </section>
    </div>

    <section class="projeto-proximo">
      <div class="main-container">
        <a href="../{proximo["slug"]}/" class="proximo-link">
          <span class="projeto-rotulo">Próximo projeto</span>
          <span class="proximo-linha">
            <strong>{e(proximo["nome"])}</strong>
            <img src="{raiz}assets/{proximo["capa"]}" alt="" loading="lazy">
            <span class="proximo-seta" aria-hidden="true"><svg viewBox="0 0 24 24"><use href="#i-seta-d"/></svg></span>
          </span>
        </a>
      </div>
      <div class="line-section"><div class="line-inner"><i></i><i></i></div></div>
    </section>'''
    return casca(p["nome"], p["texto"], raiz, conteudo)


# ------------------------------------------------------------------
# Página /projetos: as pastas
# ------------------------------------------------------------------
def cartao_pasta(pasta, raiz):
    n = len(pasta["projetos"])
    anim = f' data-anim="{raiz}assets/{pasta["anim"]}"' if pasta["anim"] else ""
    return f'''        <a class="pasta" href="{pasta["slug"]}/">
          <span class="pasta-moldura">
            <span class="pasta-imagem"><img src="{raiz}assets/{pasta["imagem"]}"{anim} alt="" loading="lazy"></span>
            <span class="pasta-corpo">
              <span class="pasta-titulo"><strong>{e(pasta["nome"])}</strong><em>{e(pasta["frase"])}</em><span>{e(pasta["apoio"])}</span></span>
              <span class="pasta-base">
                <span class="pasta-num"><b>{n:02d}</b> {"projeto" if n == 1 else "projetos"}</span>
              </span>
            </span>
          </span>
        </a>'''


def pagina_pastas():
    raiz = "../"
    cartoes = "\n".join(cartao_pasta(p, raiz) for p in PASTAS)
    conteudo = f'''{topo(f"{raiz}index.html", "Voltar para o site", "Projetos", "Escolha uma pasta e explore os projetos")}

    <section class="pastas-secao">
      <div class="main-container">
        <div class="pastas" data-blur>
{cartoes}
        </div>
      </div>
      <div class="line-section"><div class="line-inner"><i></i><i></i></div></div>
    </section>'''
    return casca("Projetos", "Projetos de motion design e social media de Carlos Mograph, separados por pasta.", raiz, conteudo)


# ------------------------------------------------------------------
# Página de cada pasta: a lista dos projetos dela
# ------------------------------------------------------------------
def pagina_pasta(pasta):
    raiz = "../../"
    cartoes = []
    for s in pasta["projetos"]:
        p = PROJETOS[s]
        sub = p["categoria"] if p["tipo"] == "motion" else p["setor"]
        anim = ""
        if p["tipo"] == "motion":
            anim = f' data-anim="{raiz}assets/{p["capa"].replace("-capa", "")}"'
        cartoes.append(f'''          <a class="pasta-projeto" href="../{s}/">
            <span class="pasta-projeto-img"><img src="{raiz}assets/{p["capa"]}"{anim} alt="" loading="lazy"></span>
            <span class="pasta-projeto-texto"><strong>{e(p["nome"])}</strong><span>{e(sub)} · {e(p["ano"])}</span></span>
          </a>''')
    n = len(pasta["projetos"])
    conteudo = f'''{topo("../", "Todas as pastas", pasta["nome"], f'{n} {"projeto" if n == 1 else "projetos"} · {pasta["apoio"]}')}

    <section class="pastas-secao">
      <div class="main-container">
        <div class="pasta-lista" data-blur>
{chr(10).join(cartoes)}
        </div>
      </div>
      <div class="line-section"><div class="line-inner"><i></i><i></i></div></div>
    </section>'''
    return casca(pasta["nome"], f'{pasta["nome"]}: {pasta["apoio"]}.', raiz, conteudo)


def escrever(caminho, texto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")
    print(f"  + {caminho.relative_to(RAIZ).as_posix()}")


escrever(RAIZ / "projetos" / "index.html", pagina_pastas())
for pasta in PASTAS:
    escrever(RAIZ / "projetos" / pasta["slug"] / "index.html", pagina_pasta(pasta))
    lista = pasta["projetos"]
    for i, s in enumerate(lista):
        escrever(RAIZ / "projetos" / s / "index.html", pagina_projeto(PROJETOS[s], PROJETOS[lista[(i + 1) % len(lista)]]))
print(f"\n{len(PROJETOS)} projetos em {len(PASTAS)} pastas")
