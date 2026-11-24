#!/usr/bin/env python3
"""Gera a versão do BION-07 para o GameDistribution.

Uso:  python3 tools/build-gamedistribution.py SEU_GAME_ID
      (o Game ID aparece no painel do GameDistribution depois de criar o jogo)
Saída: dist/gamedistribution.zip  (index.html na raiz; é este .zip que você envia)
"""
import os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
game_id = sys.argv[1] if len(sys.argv) > 1 else 'COLE_AQUI_O_GAME_ID'
if not re.fullmatch(r'[A-Za-z0-9_-]+', game_id):
    raise SystemExit('Game ID inválido')

SDK = """<script>
window["GD_OPTIONS"] = {
  "gameId": "%s",
  "onEvent": function (event) { if (window.__gdEvent) window.__gdEvent(event); }
};
(function (d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = 'https://html5.api.gamedistribution.com/main.min.js';
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'gamedistribution-jssdk'));
</script>""" % game_id

html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
for old, new in [("const BION_PLATFORM = 'web';", "const BION_PLATFORM = 'gamedistribution';"), ('<!--PLATFORM_SDK-->', SDK)]:
    if old not in html:
        raise SystemExit('Marcador não encontrado: ' + old)
    html = html.replace(old, new, 1)
html, n = re.subn(r'<!--PWA-->.*?<!--/PWA-->\n?', '', html, flags=re.S)
if n != 1:
    raise SystemExit('Bloco PWA não encontrado')

out_dir = os.path.join(ROOT, 'dist', 'gamedistribution')
os.makedirs(out_dir, exist_ok=True)
out_html = os.path.join(out_dir, 'index.html')
open(out_html, 'w', encoding='utf-8').write(html)
zip_path = os.path.join(ROOT, 'dist', 'gamedistribution.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out_html, 'index.html')
print('OK:', os.path.relpath(zip_path, ROOT), '| gameId =', game_id)
