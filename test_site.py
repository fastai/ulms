import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

site = Path(__file__).parent/'universalmodels'


def test_local_pages_and_fonts():
    refs = []
    for page in site.glob('*.html'):
        soup = BeautifulSoup(page.read_bytes(), 'html.parser')
        assert len(soup.find_all('aside', class_='archive-notice')) == 1
        for tag in soup.find_all():
            for attr in ('src', 'href'):
                if attr not in tag.attrs: continue
                url = tag[attr]
                if tag.name == 'a' and urlsplit(url).scheme: continue
                refs.append((page, url))
            for entry in tag.get('srcset', '').split(','):
                if entry.strip(): refs.append((page, entry.split()[0]))
            refs.extend((page, url) for url in re.findall(r'''url\(['"]?([^)'"\s]+)''', tag.get('style', '')))
    for css in site.rglob('*.css'):
        urls = re.findall(r'''url\(['"]?([^)'"\s]+)''', css.read_text())
        refs.extend((css, url) for url in urls if urlsplit(url).path.endswith(('.css', '.ttf', '.woff', '.woff2', '.eot')))
    for source, url in refs:
        parts = urlsplit(url)
        if parts.scheme == 'data' or not parts.path: continue
        assert not parts.scheme and not parts.netloc, (source, url)
        target = site/parts.path.lstrip('/') if parts.path.startswith('/') else source.parent/parts.path
        assert target.resolve().is_relative_to(site.resolve()), (source, url)
        assert Path(unquote(str(target))).is_file(), (source, url)
