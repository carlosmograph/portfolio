# Gera uma cópia do portfólio em arquivo único: CSS, JS e imagens embutidos.
# Serve para pré-visualizar em lugares que só aceitam um HTML.
# O arquivo de trabalho continua sendo o index.html.
#
#   python build-preview.py
#
# Saída: preview.html, ao lado do index.html.

import base64
import mimetypes
import pathlib
import re

AQUI = pathlib.Path(__file__).parent
ENTRADA = AQUI / "index.html"
SAIDA = AQUI / "preview.html"

html = ENTRADA.read_text(encoding="utf-8")


def ler(nome):
    caminho = AQUI / nome
    if not caminho.exists():
        print(f"  ! não encontrei {nome}")
        return None
    print(f"  + {nome} ({caminho.stat().st_size // 1024} KB)")
    return caminho


# 1. <link rel="stylesheet" href="./crmo.css">  ->  <style>…</style>
def embutir_css(match):
    caminho = ler(match.group(1))
    if not caminho:
        return match.group(0)
    return "<style>\n" + caminho.read_text(encoding="utf-8") + "\n</style>"


html = re.sub(r'<link rel="stylesheet" href="\./([^"]+\.css)">', embutir_css, html)

# 2. <script src="./crmo.js" defer></script>  ->  <script>…</script>
def embutir_js(match):
    caminho = ler(match.group(1))
    if not caminho:
        return match.group(0)
    return "<script>\n" + caminho.read_text(encoding="utf-8") + "\n</script>"


html = re.sub(r'<script src="\./([^"]+\.js)"[^>]*></script>', embutir_js, html)

# 3. imagens -> data URI
def embutir_img(match):
    caminho = ler(match.group(1))
    if not caminho:
        return match.group(0)
    tipo = mimetypes.guess_type(caminho.name)[0] or "application/octet-stream"
    dados = base64.b64encode(caminho.read_bytes()).decode("ascii")
    return f'"data:{tipo};base64,{dados}"'


html = re.sub(r'"\./(assets/[^"]+)"', embutir_img, html)

SAIDA.write_text(html, encoding="utf-8")
print(f"\npreview.html gerado — {len(html.encode('utf-8')) // 1024} KB")
