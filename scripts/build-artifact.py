#!/usr/bin/env python3
"""
Gera a versão da landing page para publicar como página hospedada no
claude.ai, a partir do mesmo index.html do repositório.

A plataforma injeta o próprio <!doctype html>, <head> e <body>, então a
página publicada não pode trazer esses elementos. Este script tira o
invólucro, embute o CSS compilado (a plataforma não serve arquivos .css
relativos como o servidor comum) e devolve o miolo pronto.

Uso:
    python3 scripts/build-artifact.py [destino]

O destino padrão é dist/artifact/. Rode `npm run build` antes, senão o
CSS embutido fica desatualizado.
"""

import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO_PADRAO = RAIZ / "dist" / "artifact"

FONTES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2'
    "?family=Inter:wght@400;500;600"
    "&family=Outfit:wght@500;600;700;800"
    '&display=swap" rel="stylesheet">'
)


def titulo(html: str) -> str:
    achado = re.search(r"<title>(.*?)</title>", html, re.S)
    return achado.group(1).strip() if achado else "Adultando"


def corpo(html: str) -> tuple[str, str]:
    achado = re.search(r'<body[^>]*class="([^"]*)"[^>]*>(.*)</body>', html, re.S)
    if not achado:
        raise SystemExit("index.html: não achei <body class=\"...\"> para extrair.")
    return achado.group(1), achado.group(2)


def main() -> None:
    destino = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DESTINO_PADRAO

    html = (RAIZ / "index.html").read_text(encoding="utf-8")
    css_path = RAIZ / "assets" / "css" / "app.css"
    if not css_path.exists():
        raise SystemExit("assets/css/app.css não existe. Rode `npm run build` antes.")
    css = css_path.read_text(encoding="utf-8")

    classes, miolo = corpo(html)

    pagina = (
        f"<title>{titulo(html)}</title>\n"
        f"{FONTES}\n"
        f"<style>\n{css}\n</style>\n"
        f'<div class="{classes}">\n{miolo}\n</div>\n'
    )

    if "<html" in pagina or "<head>" in pagina:
        raise SystemExit("O invólucro HTML não saiu do arquivo gerado.")

    destino.mkdir(parents=True, exist_ok=True)
    (destino / "page.html").write_text(pagina, encoding="utf-8")

    # As imagens são publicadas ao lado da página, nos mesmos caminhos que
    # o HTML referencia.
    imagens = destino / "assets" / "img"
    imagens.mkdir(parents=True, exist_ok=True)
    copiadas = 0
    for arquivo in sorted((RAIZ / "assets" / "img").iterdir()):
        if arquivo.is_file():
            shutil.copy2(arquivo, imagens / arquivo.name)
            copiadas += 1

    print(f"gerado: {destino / 'page.html'} ({len(pagina):,} bytes)")
    print(f"imagens copiadas: {copiadas}")


if __name__ == "__main__":
    main()
