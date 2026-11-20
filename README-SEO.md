# Landingpage SEO & Entity Identity Integration

Covers the four existing static routes: EN/RU homepages and EN/RU service catalogues.

- `seo/site-config.json`: authoritative page, language and entity configuration.
- `robots.txt` and `sitemap.xml`: crawler discovery artifacts for the project site.
- Homepage JSON-LD uses `WebPage`; service catalogues use `CollectionPage`.
- EN/RU alternate links are paired within matching page groups.
- `ProfilePage` is intentionally not used for mixed homepages or catalogues.

## GitHub Pages robots scope

This is a GitHub Pages project site. Repository-root `robots.txt` is served at `/Landingpage/robots.txt`, not host-level `https://vitoog.github.io/robots.txt`. It does not control crawler policy for the entire host. The sitemap can be submitted separately through the URL-prefix Search Console property `https://vitoog.github.io/Landingpage/`.

## Verification

Run from repository root:

```bash
python3 scripts/apply_seo.py --site-root . --config seo/site-config.json
python3 scripts/verify_seo.py --site-root . --config seo/site-config.json
python3 -m unittest discover -s tests -v
bash scripts/check_live.sh https://vitoog.github.io/Landingpage
git diff --check
```

The generator backs up modified files and is idempotent. Sitemap and indexing requests are discovery hints, not ranking or indexing guarantees.
