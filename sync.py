from pathlib import Path
import re
from urllib.request import Request, urlopen
from xml.etree import ElementTree

SOURCE = 'https://misterww-noticias.misterwwpr.chatgpt.site'
DESTINATION = 'https://misteruww.github.io'
TARGET = Path('_site')


def fetch_bytes(path):
    request = Request(SOURCE + path, headers={'User-Agent': 'MisterWW-News-Mirror/1.0'})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f'{path}: HTTP {response.status}')
        return response.read()


def fetch(path):
    return fetch_bytes(path).decode('utf-8')


sitemap = fetch('/sitemap.xml')
root = ElementTree.fromstring(sitemap)
paths = [url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text.removeprefix(SOURCE) for url in root]
if '/' not in paths or len(paths) < 2:
    raise RuntimeError('The source sitemap contains no article pages')

for route in paths:
    relative = 'index.html' if route == '/' else route.lstrip('/')
    content = fetch(route).replace(SOURCE, DESTINATION)
    target = TARGET / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

image_paths = set(re.findall(r'/images/[a-z0-9-]+\.(?:jpg|png|webp)', (TARGET / 'index.html').read_text()))
for image_path in image_paths:
    target = TARGET / image_path.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(fetch_bytes(image_path))

(TARGET / 'sitemap.xml').write_text(sitemap.replace(SOURCE, DESTINATION))
(TARGET / 'robots.txt').write_text(fetch('/robots.txt').replace(SOURCE, DESTINATION))
print(f'Mirrored {len(paths)-1} articles and {len(image_paths)} images')
