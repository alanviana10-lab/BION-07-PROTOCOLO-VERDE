#!/usr/bin/env python3
"""Gera a versão do BION-07 para o CrazyGames a partir do index.html principal.

Uso:  python3 tools/build-crazygames.py
Saída: dist/crazygames/index.html  e  dist/crazygames.zip  (é este .zip que você envia no portal)

O que muda em relação à versão web:
- inclui o SDK v3 do CrazyGames (anúncios, gameplayStart/Stop, salvamento na nuvem);
- remove manifesto/service worker do PWA (o portal não usa);
- esconde o botão de tela cheia (o portal já tem o dele).
"""
import os, re, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
OUT_DIR = os.path.join(ROOT, 'dist', 'crazygames')
SDK_TAG = '<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>'

html = open(SRC, encoding='utf-8').read()

def must_replace(text, old, new):
    if old not in text:
        raise SystemExit('Marcador não encontrado: ' + old)
    return text.replace(old, new, 1)

html = must_replace(html, "const BION_PLATFORM = 'web';", "const BION_PLATFORM = 'crazygames';")
html = must_replace(html, '<!--PLATFORM_SDK-->', SDK_TAG)
html, n = re.subn(r'<!--PWA-->.*?<!--/PWA-->\n?', '', html, flags=re.S)
if n != 1:
    raise SystemExit('Bloco PWA não encontrado')

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, 'index.html')
open(out_html, 'w', encoding='utf-8').write(html)

zip_path = os.path.join(ROOT, 'dist', 'crazygames.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out_html, 'index.html')   # index.html na raiz do zip

print('OK:', os.path.relpath(out_html, ROOT), '|', os.path.relpath(zip_path, ROOT), f'({os.path.getsize(zip_path) // 1024} KB)')
