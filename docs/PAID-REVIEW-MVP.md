# Paid entry offer — System Integration Review

**Status:** Website pilot offer drafted on a feature branch. Email intake only. No online checkout, automated payment confirmation, CRM or order backend is connected.

## Offer definition

- **Name:** System Integration Review
- **Pilot fee:** EUR 150. This is an initial commercial hypothesis, not a validated market rate.
- **Scope:** one existing or planned technical system and one agreed integration question.
- **Inputs:** up to three customer-provided technical artefacts, such as a system diagram, interface specification, topology or bill of materials.
- **Session:** one remote working session, up to 90 minutes.
- **Outputs:** a concise written findings note; a lightweight system-context and interface/data-flow sketch; prioritized integration risks; recommended next steps.
- **Delivery date:** agreed when the request is accepted.
- **Exclusions:** system changes, production access, commissioning, intrusive security testing, electrical or functional-safety assessment, certification, conformity assessment, legal/tax advice, and agronomic validation.

The offer is intentionally bounded. It is an entry diagnostic, not a full architecture project, implementation package or certification service.

## Current customer flow

1. Visitor clicks **Request invoice / Запросить счёт**.
2. The browser opens a pre-addressed email with a short intake template.
3. The provider reviews fit, scope and availability manually.
4. If accepted, the provider confirms the scope and issues an invoice with the applicable tax treatment and payment details.
5. Work is scheduled after payment is received.
6. Findings are delivered on the date agreed with the customer.

A general project inquiry remains available separately and is not converted into a paid gate.

## Current implementation boundary

This repository is a static GitHub Pages site. The pilot CTA uses `mailto:` only. It does **not**:
- collect or persist submissions in a server-side system;
- create invoices or calculate VAT;
- create Stripe Checkout Sessions or collect card details;
- receive or verify Stripe webhooks;
- update the local ERICA OS / SEP task or event store;
- send transactional email through Web3Forms.

Do not describe the present implementation as an online payment flow. Buy Me a Coffee remains voluntary support and must not be presented as payment for this engineering service.

## Production payment integration — prerequisites

Before adding a live card checkout:

1. Confirm merchant onboarding, settlement bank details and the company's account setup in Stripe.
2. Confirm invoice, VAT and any applicable Latvian fiscal/EKA treatment with the company's accountant or VID. The public price must have an unambiguous tax presentation before card payment is enabled.
3. Define cancellation, refund, rescheduling, service-delivery and privacy terms.
4. Define a stable offer identifier and authoritative server-side amount. The browser must not be allowed to supply the amount.
5. Implement server-side Checkout Session creation with an allowlist of sellable offers.
6. Verify Stripe webhook signatures, handle events idempotently, and persist payment state independently of the browser redirect.
7. Route only the minimum required event data into a restricted order/intake endpoint. Do not expose an unauthenticated local Go Core or the broader ERICA OS runtime to the public internet.
8. Test successful payment, failed payment, expired session, duplicate webhook, refund and unavailable local endpoint before activation.

## Integration roles

- **Cloudflare:** DNS and controlled public edge. A Tunnel may provide a private path to a specifically designed endpoint; it does not replace application authentication.
- **Stripe:** card payment and signed payment events after merchant/fiscal prerequisites are satisfied.
- **Web3Forms:** optional transport for ordinary non-payment inquiries. It is not the payment source of truth.
- **Local request/order store:** authoritative application state once a backend exists. Payment success must be derived from a verified provider event, not a browser success URL.
- **ERICA OS / SEP capability broker:** do not treat this as a commercial lead/order CRM. Its action/capability semantics are a different boundary.

## Acceptance criteria for the next implementation phase

- Fixed-price offer ID maps to a server-controlled amount and currency.
- No Stripe secret or webhook signing secret is present in static assets, repository history or client-side JavaScript.
- A paid order is accepted only after a valid webhook event.
- Duplicate webhook delivery does not duplicate an order.
- The system records request ID, provider session/event IDs, payment state and timestamps without storing card data.
- The visitor receives a clear pending / paid / failed result.
- General inquiries remain free and separate.
- The flow has a documented rollback switch that disables checkout without breaking the service catalogue.
