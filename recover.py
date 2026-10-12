import base64, hashlib, json, requests
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

root = Path(__file__).parent
site = root/'docs'
meta = root/'meta'


def save_capture(client, record):
    response = client.get_memento(record)
    if response.status_code != 200: raise ValueError(f'{response.status_code}: {response.url}')
    path = site/urlsplit(record.original).path.lstrip('/')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)
    return dict(path=path.relative_to(site).as_posix(), source=response.memento_url, timestamp=response.timestamp.isoformat())


def save_log(name, data):
    meta.mkdir(exist_ok=True)
    (meta/name).write_text(json.dumps(data, indent=2, default=str)+'\n')


def save_external(url, path, integrity=None):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    if integrity:
        algorithm, expected = integrity.split('-', 1)
        actual = base64.b64encode(hashlib.new(algorithm, response.content).digest()).decode()
        if actual != expected: raise ValueError(f'Integrity mismatch: {url}')
    dest = site/path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)
    return dict(path=path, source=url, retrieved=datetime.now(timezone.utc).isoformat())


def localize(path, replacements):
    dest = site/path
    text = dest.read_text()
    for old, new in replacements.items(): text = text.replace(old, new)
    dest.write_text(text)


def add_archive_notice():
    notice = r'''<aside class="archive-notice" aria-label="Archive notice">
  <strong>Archived copy.</strong> Stanford's original Universal Models / FORUM website (2021). This is not the current Stanford site.
  <a href="https://web.archive.org/web/20210728001856/https://universalmodels.stanford.edu/workshop.html">View the original archive</a>.
</aside>'''
    for page in site.glob('*.html'):
        if 'class="archive-notice"' in page.read_text(): continue
        localize(page.name, {'</head>': '<link rel="stylesheet" href="static/archive.css">\n</head>', '<body>': '<body>\n'+notice})
