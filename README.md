# Universal Models archive

A static restoration of Stanford's 2021 Universal Models website, originally called Foundations of Responsible Universal Models (FORUM). It preserves the site's original wording, design, and workshop announcement. Every page has a notice identifying it as an archived copy, not the current Stanford site.

The starting point was the [July 28, 2021 workshop snapshot](https://web.archive.org/web/20210728001856/https://universalmodels.stanford.edu/workshop.html).

## What was recovered

- `universalmodels/workshop.html`: the July 28, 2021 workshop page.
- `universalmodels/index.html`: the August 3, 2021 homepage.
- Styles, scripts, logos, and workshop artwork: August 24, 2021 captures of the original domain.
- Missing shared styles, icon fonts, and the Stanford panorama: August/September 2021 captures of `crfm.stanford.edu`. Several shared files have identical archive hashes on both domains. No later CRFM page text was substituted.

No original People page capture was found. `people.html` explains that gap instead of inventing a roster. Missing mobile navigation logos use the recovered FORUM logo.

Bootstrap 5.0.1 and jQuery 3.6.0 were downloaded from the original pinned CDN URLs and verified against the integrity hashes in the HTML. Google Fonts files are current downloads of the original Manrope and DM Serif Display families, not verified 2021 binaries. Display assets are served locally. Original external links remain external. Unused video/gallery styles still reference several unarchived images.

## Preview

From this directory:

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory universalmodels
```

Open <http://127.0.0.1:8765/> or <http://127.0.0.1:8765/workshop.html>. No build step is needed.

## Publishing

Publish `universalmodels/` as the GitHub Pages artifact using an Actions workflow. Branch-based Pages publishing only supports the repository root or `/docs`.

`universalmodels/CNAME` specifies `universalmodels.fast.ai`. Its DNS-only Cloudflare CNAME points to `fastai.github.io`. Configure the same custom domain in the repository's Pages settings.

## Recovery helpers and checks

`recover.py` contains the small helpers used interactively with the Python `wayback` package. It is not a complete recovery script. `test_site.py` checks local page links, assets, font/style dependencies, and archive notices.

With `pytest` and `beautifulsoup4` installed, run:

```bash
pytest -q
```

Local recovery logs are stored in `meta/` and are excluded from git. Original Stanford content and third-party assets retain their respective ownership and licenses.
