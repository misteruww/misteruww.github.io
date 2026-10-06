from pathlib import Path
import shutil

TARGET = Path('_site')
if TARGET.exists():
    shutil.rmtree(TARGET)
TARGET.mkdir()
HTML = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>GameCorePR - En mantenimiento</title><style>*{box-sizing:border-box}body{margin:0;min-height:100svh;display:grid;place-items:center;padding:24px;background:#101020;color:#f4f3ff;font-family:monospace}main{width:min(100%,560px);padding:48px 24px;text-align:center;border:3px solid #59dce8;box-shadow:8px 8px 0 #7656b7;background:#19182f}.brand{font-size:14px;letter-spacing:3px;color:#59dce8;margin-bottom:28px}h1{font-size:clamp(25px,7vw,38px);color:#fff06a;margin:0 0 22px}p{font-size:16px;line-height:1.7;margin:0;color:#c8c6df}</style></head><body><main><div class="brand">GAMECOREPR.COM</div><h1>En mantenimiento</h1><p>Estamos trabajando en la página.<br>Volvemos pronto.</p></main></body></html>'''
(TARGET / 'index.html').write_text(HTML, encoding='utf-8')
(TARGET / '404.html').write_text(HTML, encoding='utf-8')
(TARGET / 'CNAME').write_text('gamecorepr.com\n', encoding='utf-8')
(TARGET / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
(TARGET / '.nojekyll').touch()
print('GameCorePR maintenance page built; catalog mirroring disabled')
