# Viktors Simonenko — Bilingual Engineering Website

A static bilingual professional website for Viktors Simonenko, Systems Architect & Integration Engineer, and the engineering services offered through SIA “Golden Greens Crop”.

## Public routes

| Route | Language | Source |
|---|---|---|
| `/` | English homepage | `index.html` |
| `/ru/` | Russian homepage | `ru/index.html` |
| `/services/` | English service catalogue | `services/index.html` |
| `/ru/services/` | Russian service catalogue | `ru/services/index.html` |

Each route is a separately maintained static HTML page. Language switches connect equivalent EN/RU routes.

## Identity and content boundaries

The website distinguishes the independent engineering practice of **Viktors Simonenko** from **SIA “Golden Greens Crop”**, **ERICA OS**, and the **Sovereign Engineering Platform**. The company is the contracting entity for commercial engagements; the other projects and initiatives are described according to their actual development and evidence status.

Project descriptions do not claim a commissioned production greenhouse, certified system, production-ready ERICA OS, or completed enterprise deployment. Catalogue prices are indicative; final scope, responsibilities, acceptance criteria and price are agreed before engagement.

The supplied SVG in `assets/brand/` is the canonical Golden Greens Crop mark. It is used as a secondary company emblem; it does not replace the personal name as the primary identity.

## Architecture

- **HTML:** four semantic, language-specific static pages.
- **CSS:** shared design tokens, base styles, layout, components, responsive rules, and separate catalogue styling.
- **JavaScript:** vanilla JavaScript for mobile navigation, footer year, catalogue loading, filtering, search and the offer-details dialog.
- **Data:** `data/catalog.en.json` and `data/catalog.ru.json`, each containing 33 offers with matching IDs and fields.
- **SEO:** `seo/site-config.json` is the authoritative source for route metadata and person / organization identity. Python scripts generate and validate managed metadata, `robots.txt` and `sitemap.xml`.
- **Assets:** the supplied SVG brand mark and a reserved location for publication-safe project images.

There is no framework, package manager, Node build, generated frontend bundle or application backend. The homepages load Google Fonts through an external stylesheet and retain CSS fallback fonts. Catalogue enquiry links use `mailto:`; the current `main` branch does not collect visitor details through a server-side form.

## Service catalogue

- Data: `data/catalog.en.json`, `data/catalog.ru.json`.
- Renderer and interaction: `js/catalog.js`.
- Styling: `css/catalog.css`.
- English catalogue: `/services/`.
- Russian catalogue: `/ru/services/`.

The catalogue provides localized service descriptions, indicative prices, billing models, intended buyers, problems addressed, deliverables and scope boundaries. Internal sales-planning fields are not part of the public data.

## SEO and discovery

`seo/site-config.json` defines the four public routes, canonical URLs, language groups, titles, descriptions and entity information. The managed HTML blocks contain canonical metadata, reciprocal `hreflang`, localized Open Graph metadata and JSON-LD. The schema distinguishes the Person, Organization, WebSite and page entities.

- `scripts/apply_seo.py` generates managed metadata and the sitemap from the configuration. It is designed to be deterministic and idempotent; by default it makes a `.pre-seo-*.bak` backup before changing an existing file.
- `scripts/verify_seo.py` checks route metadata, language alternates, JSON-LD, robots directives and sitemap consistency.
- `scripts/check_live.sh` performs a live-site smoke check.
- `robots.txt` and `sitemap.xml` are project-site discovery artifacts.
- `google1d7fc4778589f1c1.html` is the Google Search Console HTML verification artifact. Do not remove or replace it without checking the active Search Console property.

This is a GitHub Pages **project site**. The repository-root robots file is served at `https://vitoog.github.io/Landingpage/robots.txt`; it does not control the host-level `https://vitoog.github.io/robots.txt`. The sitemap URL is `https://vitoog.github.io/Landingpage/sitemap.xml`. Search Console setup and monitoring instructions are in `docs/SEARCH-CONSOLE.md`.

## Local development

Run from the repository root:

```bash
python3 -m http.server 8081 --bind 127.0.0.1
```

Open `http://127.0.0.1:8081/`, `/ru/`, `/services/` or `/ru/services/`.

To regenerate SEO output intentionally:

```bash
python3 scripts/apply_seo.py --site-root . --config seo/site-config.json
```

Review the generated diff and any `*.pre-seo-*.bak` files before committing. To validate without modifying the site, run:

```bash
python3 scripts/verify_seo.py --site-root . --config seo/site-config.json
python3 -m unittest discover -s tests -v
git diff --check
```

For a live deployment smoke check:

```bash
bash scripts/check_live.sh https://vitoog.github.io/Landingpage
```

The `SEO integrity` GitHub Actions workflow runs the SEO validator and regression tests on pushes to `main` and pull requests targeting `main`. GitHub Pages publishing is managed separately by the repository's Pages configuration.

## Repository structure

```text
.
├── .github/workflows/seo-validation.yml
├── assets/
│   ├── brand/golden-greens-crop-mark.svg
│   └── images/                 # reserved for approved project images
├── css/
│   ├── tokens.css
│   ├── base.css
│   ├── layout.css
│   ├── components.css
│   ├── responsive.css
│   └── catalog.css
├── data/
│   ├── catalog.en.json
│   └── catalog.ru.json
├── docs/
│   ├── DISCOVERY-PLAN.md
│   └── SEARCH-CONSOLE.md
├── js/
│   ├── main.js
│   └── catalog.js
├── ru/
│   ├── index.html
│   └── services/index.html
├── scripts/
│   ├── apply_seo.py
│   ├── verify_seo.py
│   └── check_live.sh
├── seo/site-config.json
├── services/index.html
├── tests/
├── google1d7fc4778589f1c1.html
├── index.html
├── robots.txt
└── sitemap.xml
```
