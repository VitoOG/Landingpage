import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    "services/index.html": {
        "title": "System Integration Review",
        "cta": "Request invoice",
        "manual_notice": "Online card checkout is not active yet.",
    },
    "ru/services/index.html": {
        "title": "Инженерный обзор интеграции системы",
        "cta": "Запросить счёт",
        "manual_notice": "Онлайн-оплата картой пока не подключена.",
    },
}


class PaidReviewIntakeTests(unittest.TestCase):
    def test_offer_is_present_in_both_supported_catalogue_locales(self):
        for route, expected in ROUTES.items():
            html = (ROOT / route).read_text(encoding="utf-8")
            with self.subTest(route=route):
                self.assertIn('class="paid-review section-shell"', html)
                self.assertIn(expected["title"], html)
                self.assertIn("€150", html)
                self.assertIn(expected["cta"], html)
                self.assertIn(expected["manual_notice"], html)
                self.assertIn("mailto:viksim1221@gmail.com", html)

    def test_paid_offer_does_not_replace_the_free_project_inquiry(self):
        for route in ROUTES:
            html = (ROOT / route).read_text(encoding="utf-8")
            with self.subTest(route=route):
                self.assertIn('class="catalog-contact"', html)
                self.assertIn("catalog-grid", html)

    def test_catalogue_remains_separate_from_the_fixed_fee_pilot(self):
        for route in ROUTES:
            html = (ROOT / route).read_text(encoding="utf-8")
            with self.subTest(route=route):
                self.assertIn("33", html)
                self.assertIn('class="paid-review-offer"', html)


if __name__ == "__main__":
    unittest.main()
