from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
import re, shutil

SOURCE = 'https://gamecorepr.misterwwpr.chatgpt.site'
TARGET = Path('_site')
if TARGET.exists():
    shutil.rmtree(TARGET)
TARGET.mkdir()
def get(path):
    with urlopen(Request(SOURCE + path, headers={'User-Agent': 'GameCorePR-Publisher/1.0'}), timeout=60) as response:
        data = response.read()
    if b'drippycodeshop' in data.lower() and path.endswith('.html'):
        raise RuntimeError('Unexpected content; refusing to publish')
    dest = TARGET / path.lstrip('/')
    if path.endswith('/'):
        dest = dest / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return data
sitemap = get('/sitemap.xml')
root = ET.fromstring(sitemap)
paths = [urlparse(node.text).path for node in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assets = {'/style.css', '/app.js', '/favicon.svg', '/robots.txt'}
def page(path):
    data = get(path)
    text = data.decode()
    assets.update(re.findall(r'(?:src|href)="(/images/[^"]+)"', text))
    return path
with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(page, paths))
with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(get, sorted(assets)))
(TARGET / 'CNAME').write_text('gamecorepr.com\n')
(TARGET / '.nojekyll').touch()
print(f'Published {len(paths)} GameCorePR pages from its independent project. No scheduled news updates.')
