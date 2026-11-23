# Viktors Simonenko — Bilingual Landing Page

Static bilingual professional website and engineering service catalogue.

## Routes
- English home: `/`
- Russian home: `/ru/`
- English catalogue: `/services/`
- Russian catalogue: `/ru/services/`
- English request cart: `/cart/`
- Russian request cart: `/ru/cart/`

## Service request flow
The catalogue contains 33 offers in bilingual JSON data files. Visitors add unique service IDs to a browser-local request cart. Cart state is stored in versioned localStorage and persists across pages and refreshes. The order form sends the selected service list and contact details to Web3Forms.

This is an enquiry/request workflow, not checkout, payment processing, a binding order confirmation or automatic invoicing. Price ranges are itemized; no combined payable total is calculated because offers use different billing models (fixed fee, milestones, recurring monthly retainers).

The Web3Forms Access Key is a public client-side form identifier. Provider success is shown only when the API responds with `success: true`; fields and cart remain on failures. Automated tests mock the provider and never send email.

## Local preview
```bash
python3 -m http.server 8081 --bind 127.0.0.1
```
Open `http://127.0.0.1:8081/`, `/ru/`, `/services/`, `/ru/services/`, `/cart/` or `/ru/cart/`.

## Validation
```bash
python -m unittest discover -s tests -v
node --check js/order-core.js
node --check js/order-cart.js
node --check js/order-form.js
node --check js/catalog.js
node --test tests/order-core.test.cjs
```

## Production notes
- The current provider integration uses the Golden Greens Crop public Web3Forms key.
- If Web3Forms Pro domain restriction is enabled, configure the hostname `vitoog.github.io`; do not include protocol or path.
- The current form includes the legacy `botcheck` honeypot as a supplementary field. Current Web3Forms documentation marks honeypot protection as deprecated and recommends CAPTCHA protection.
- Review and publish a privacy notice before collecting customer personal data.
- A successful provider response confirms receipt by Web3Forms, not delivery to a recipient inbox, a signed agreement or payment.
