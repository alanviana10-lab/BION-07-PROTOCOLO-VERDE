#!/usr/bin/env python3
"""Gera a versão do BION-07 para o itch.io a partir do index.html principal.

Uso:  python3 tools/build-itch.py
Saída: dist/itch.zip  (envie este .zip no itch.io, tipo de projeto HTML)

Diferenças da versão web: sem manifesto/service worker do PWA (no itch o cache
offline poderia prender os jogadores numa versão antiga após uma atualização).
"""
import os, re, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
if "const BION_PLATFORM = 'web';" not in html:
    raise SystemExit('Marcador de plataforma não encontrado')
html = html.replace("const BION_PLATFORM = 'web';", "const BION_PLATFORM = 'itch';", 1)
html = html.replace('<!--PLATFORM_SDK-->', '', 1)
html, n = re.subn(r'<!--PWA-->.*?<!--/PWA-->\n?', '', html, flags=re.S)
if n != 1:
    raise SystemExit('Bloco PWA não encontrado')

out_dir = os.path.join(ROOT, 'dist', 'itch')
os.makedirs(out_dir, exist_ok=True)
out_html = os.path.join(out_dir, 'index.html')
open(out_html, 'w', encoding='utf-8').write(html)
zip_path = os.path.join(ROOT, 'dist', 'itch.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out_html, 'index.html')
print('OK:', os.path.relpath(zip_path, ROOT), f'({os.path.getsize(zip_path) // 1024} KB)')
