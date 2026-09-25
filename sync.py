from pathlib import Path
import re
import time
from urllib.request import Request, urlopen
from xml.etree import ElementTree

SOURCE = 'https://misterww-noticias.misterwwpr.chatgpt.site'
DESTINATION = 'https://misteruww.github.io'
TARGET = Path('_site')
ASSET_PATTERN = re.compile(r'/images/[a-zA-Z0-9._-]+\.(?:jpg|jpeg|png|webp|gif|svg)', re.IGNORECASE)


def fetch_bytes(path):
    fresh_url = SOURCE + path + ('&' if '?' in path else '?') + f'mirror={time.time_ns()}'
    request = Request(fresh_url, headers={'User-Agent': 'MisterWW-News-Mirror/1.0', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f'{path}: HTTP {response.status}')
        return response.read()


def fetch(path):
    return fetch_bytes(path).decode('utf-8')


sitemap = fetch('/sitemap.xml')
root = ElementTree.fromstring(sitemap)
namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
paths = []
for url in root:
    location = url.find(f'{namespace}loc')
    if location is None or not location.text or not location.text.startswith(SOURCE + '/'):
        raise RuntimeError('The source sitemap contains an unexpected URL')
    paths.append(location.text[len(SOURCE):])
if '/' not in paths or len(paths) < 2:
    raise RuntimeError('The source sitemap contains no article pages')

assets = set()
for route in paths:
    relative = route.lstrip('/')
    if not relative or route.endswith('/'):
        relative += 'index.html'
    content = fetch(route).replace(SOURCE, DESTINATION)
    target = TARGET / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
    assets.update(ASSET_PATTERN.findall(content))

for asset_path in sorted(assets):
    target = TARGET / asset_path.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(fetch_bytes(asset_path))

(TARGET / 'sitemap.xml').write_text(sitemap.replace(SOURCE, DESTINATION), encoding='utf-8')
(TARGET / 'robots.txt').write_text(fetch('/robots.txt').replace(SOURCE, DESTINATION), encoding='utf-8')
(TARGET / '.nojekyll').touch()
print(f'Mirrored {len(paths)} pages and {len(assets)} image assets')
