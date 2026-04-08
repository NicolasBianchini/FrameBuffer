import json
from pathlib import Path
import subprocess
import sys

import numpy as np

LARGURA = 24
ALTURA = 16
TAMANHO_PIXEL = 28
ATRASO_ENTRE_PIXELS_MS = 35
COR_PIXEL_APAGADO = "#111827"
COR_GRADE = "#374151"
ARQUIVO_VISUAL = Path("framebuffer.html")

CORES_DOS_PIXELS = {
    0: COR_PIXEL_APAGADO,
    1: "#e5e7eb",  # corpo do foguete
    2: "#38bdf8",  # janela
    3: "#ef4444",  # detalhes vermelhos
    4: "#f97316",  # fogo laranja
    5: "#facc15",  # fogo amarelo e estrelas
}

DESENHO = [
    "........................",
    ".....................5..",
    "...........11...........",
    "..........1111..........",
    "..........1221..........",
    ".........112211.........",
    ".........111111.....5...",
    "........11133111........",
    ".......1111331111.......",
    "......111113311111......",
    ".....11111133111111.....",
    "......331111111133......",
    ".......33..11..33.......",
    "..........4444..........",
    ".........445544.........",
    "...........55...........",
]


def criar_framebuffer(largura, altura):
    """Cria uma matriz preenchida com zeros."""
    return np.zeros((altura, largura), dtype=int)


def desenhar_mapa_de_pixels(framebuffer, desenho):
    """Copia um desenho em texto para dentro do framebuffer."""
    for y, linha in enumerate(desenho):
        for x, caractere in enumerate(linha):
            if caractere != ".":
                framebuffer[y][x] = int(caractere)


def mostrar_framebuffer(framebuffer):
    """Mostra o framebuffer no terminal."""
    for linha in framebuffer:
        print(" ".join(str(pixel) for pixel in linha))


def gerar_html_do_framebuffer(framebuffer):
    """Gera uma pagina HTML que desenha o framebuffer no navegador."""
    altura, largura = framebuffer.shape
    pixels = []
    pixels_acesos = []

    for y in range(altura):
        for x in range(largura):
            pixel = framebuffer[y][x]
            indice = y * largura + x
            cor = CORES_DOS_PIXELS[pixel]

            pixels.append(f'<div class="pixel" data-indice="{indice}"></div>')

            if pixel != 0:
                pixels_acesos.append({"indice": indice, "cor": cor})

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Framebuffer visual</title>
    <style>
        body {{
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            background: #020617;
            color: white;
            font-family: Arial, sans-serif;
        }}

        main {{
            text-align: center;
        }}

        p {{
            color: #cbd5e1;
        }}

        .tela {{
            display: grid;
            grid-template-columns: repeat({largura}, {TAMANHO_PIXEL}px);
            grid-template-rows: repeat({altura}, {TAMANHO_PIXEL}px);
            border: 2px solid {COR_GRADE};
            margin: 24px 0;
        }}

        .pixel {{
            width: {TAMANHO_PIXEL}px;
            height: {TAMANHO_PIXEL}px;
            box-sizing: border-box;
            border: 1px solid {COR_GRADE};
            background: {COR_PIXEL_APAGADO};
            transition: background 180ms ease, transform 180ms ease;
        }}

        .pixel.aceso {{
            transform: scale(0.9);
        }}

        button {{
            border: 0;
            border-radius: 8px;
            padding: 12px 16px;
            background: #38bdf8;
            color: #052e16;
            cursor: pointer;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <main>
        <h1>Framebuffer visual</h1>
        <p>Um foguete em pixel art, renderizado progressivamente a partir de uma matriz.</p>
        <div class="tela">
            {"".join(pixels)}
        </div>
        <button onclick="animarFramebuffer()">Reiniciar animacao</button>
    </main>

    <script>
        const pixelsAcesos = {json.dumps(pixels_acesos)};
        const atrasoEntrePixels = {ATRASO_ENTRE_PIXELS_MS};

        function apagarTodosOsPixels() {{
            document.querySelectorAll(".pixel").forEach((pixel) => {{
                pixel.classList.remove("aceso");
                pixel.style.background = "{COR_PIXEL_APAGADO}";
            }});
        }}

        function animarFramebuffer() {{
            apagarTodosOsPixels();

            pixelsAcesos.forEach((pixelAceso, passo) => {{
                setTimeout(() => {{
                    const pixel = document.querySelector(`[data-indice="${{pixelAceso.indice}}"]`);
                    pixel.style.background = pixelAceso.cor;
                    pixel.classList.add("aceso");
                }}, passo * atrasoEntrePixels);
            }});
        }}

        animarFramebuffer();
    </script>
</body>
</html>
"""


def abrir_framebuffer_no_navegador(framebuffer):
    """Salva o HTML e abre a visualizacao no navegador."""
    ARQUIVO_VISUAL.write_text(gerar_html_do_framebuffer(framebuffer), encoding="utf-8")
    caminho = ARQUIVO_VISUAL.resolve()

    if sys.platform == "darwin":
        resultado = subprocess.run(
            ["open", str(caminho)],
            check=False,
            stderr=subprocess.DEVNULL,
        )

        if resultado.returncode != 0:
            print(f"Abra este arquivo no navegador: {caminho}")
    else:
        print(f"Abra este arquivo no navegador: {caminho}")

framebuffer = criar_framebuffer(LARGURA, ALTURA)
desenhar_mapa_de_pixels(framebuffer, DESENHO)

print("Framebuffer:")
mostrar_framebuffer(framebuffer)
abrir_framebuffer_no_navegador(framebuffer)
