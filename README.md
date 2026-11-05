# Viktors Simonenko — Bilingual Landing Page

A static, two-language professional landing page for a Systems Architect & Integrator.

## Languages and routes

- English: `/` (`index.html`)
- Russian: `/ru/` (`ru/index.html`)
- The visible `EN / RU` switch links directly between the two static pages.
- Each page declares its language with `lang`, localized title and metadata, and reciprocal `hreflang` links.

## Architecture

- Semantic HTML5
- Modular CSS (`tokens`, `base`, `layout`, `components`, `responsive`)
- Small vanilla JavaScript module for mobile navigation and the footer year
- No build system, package manager, framework, backend, analytics or third-party runtime dependency
- System font stack; no remote font service

## Local preview

From this directory:

```bash
python -m http.server 8081 --bind 127.0.0.1
```

Open:

- `http://127.0.0.1:8081/` — English
- `http://127.0.0.1:8081/ru/` — Russian

## Content and evidence policy

The two language pages describe the same offers, initiatives and evidence boundaries. The personal engineering practice remains distinct from Golden Greens Crop, ERICA OS and the Sovereign Engineering Platform. The R&D cards describe ongoing initiatives; they do not claim a commissioned production greenhouse, certified system, production-ready ERICA OS, or completed enterprise deployment.

The €400 Device-to-Service Integration Diagnostic is described as a bounded, read-only entry engagement: one defined integration path, up to six hours, delivered within three working days after agreed inputs. Production changes, hardware commissioning and guaranteed fixes are excluded. Confirm the public price, tax wording, service scope and delivery window before publication.

## Before publication

1. Confirm the public €400 diagnostic price, tax wording, service scope and delivery window.
2. Verify the Golden Greens public URL and all contact/profile destinations.
3. Review project maturity statements against the latest source evidence.
4. Add the canonical Golden Greens SVG only where it supports the company/project identity. Do not use it as the personal brand mark.
5. Test both language routes, mobile navigation, keyboard focus, links, and narrow/wide viewport sizes.
6. Review repository diff before merging or publishing.

## Directory structure

```text
.
├── index.html           # English
├── ru/
│   └── index.html       # Russian
├── README.md
├── css/
│   ├── tokens.css
│   ├── base.css
│   ├── layout.css
│   ├── components.css
│   └── responsive.css
├── js/
│   └── main.js
└── assets/
    ├── brand/
    └── images/
```
