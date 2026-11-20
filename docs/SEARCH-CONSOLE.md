# Google Search Console

Use the URL-prefix property: `https://vitoog.github.io/Landingpage/`.

## robots.txt scope

The repository-root file is served at `https://vitoog.github.io/Landingpage/robots.txt`. It does not control the host-level `https://vitoog.github.io/robots.txt`. Host-level policy requires access to the user-site publishing root (for example, the `VitoOG.github.io` repository), which this change does not modify.

Submit `https://vitoog.github.io/Landingpage/sitemap.xml` separately in the URL-prefix property's Sitemaps report.

## Verification

1. Create/select the URL-prefix property.
2. Choose HTML tag verification and copy Google's exact token into `site.google_site_verification`.
3. Run the generator, offline validator and tests.
4. Deploy the reviewed branch; confirm token in live homepage source.
5. Inspect all four canonical URLs; confirm successful fetch, indexing allowed and self-canonical.
6. Submit sitemap and monitor Page indexing / Performance.

A sitemap or indexing request does not guarantee crawl timing, inclusion or ranking. Do not insert guessed verification tokens.
