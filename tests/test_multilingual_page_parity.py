import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME_PAGES = ("index.html", "ru/index.html", "es/index.html", "fr/index.html")
EXPECTED_SECTIONS = [
    "top", "profile", "scope", "services", "method", "work", "principles", "contact"
]


class MultilingualPageParityTests(unittest.TestCase):
    def test_all_homepages_use_the_same_section_order(self):
        for route in HOME_PAGES:
            html = (ROOT / route).read_text(encoding="utf-8")
            section_ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', html)
            with self.subTest(route=route):
                self.assertEqual(section_ids, EXPECTED_SECTIONS)

    def test_all_homepages_have_matching_content_card_counts(self):
        for route in HOME_PAGES:
            html = (ROOT / route).read_text(encoding="utf-8")
            with self.subTest(route=route):
                self.assertEqual(html.count('class="scope-item"'), 6)
                self.assertEqual(html.count('class="service-card'), 3)
                self.assertEqual(html.count('<li><span class="step-number">'), 5)
                self.assertEqual(html.count('class="work-card"'), 4)
                self.assertEqual(html.count('<div><h3>'), 6)
                self.assertIn('id="profile"', html)
                self.assertIn('id="principles"', html)

    def test_spatial_configurator_uses_the_same_canonical_url(self):
        expected = "https://vitoog.github.io/golden-greens-spatial-system/"
        for route in HOME_PAGES:
            html = (ROOT / route).read_text(encoding="utf-8")
            with self.subTest(route=route):
                self.assertIn(expected, html)
                self.assertNotIn(expected + "es/", html)
                self.assertNotIn(expected + "fr/", html)


if __name__ == "__main__":
    unittest.main()
