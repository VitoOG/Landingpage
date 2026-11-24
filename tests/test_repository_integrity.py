import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "index.html": "en",
    "ru/index.html": "ru",
    "es/index.html": "es",
    "fr/index.html": "fr",
    "services/index.html": "en",
    "ru/services/index.html": "ru",
    "es/services/index.html": "es",
    "fr/services/index.html": "fr",
}
EXPECTED_FIELDS = {
    "id", "category", "name", "price", "billing",
    "buyer", "problem", "deliverables", "scope", "recurring",
}


class PageReferences(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.language = None
        self.catalog_language = None
        self.catalog_url = None
        self.ids = set()
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "body":
            self.catalog_language = attrs.get("data-lang")
            self.catalog_url = attrs.get("data-catalog-url")
        if attrs.get("id"):
            self.ids.add(attrs["id"])

        if tag in {"a", "link"} and attrs.get("href"):
            self.references.append(attrs["href"])
        if tag in {"script", "img", "source"} and attrs.get("src"):
            self.references.append(attrs["src"])


class RepositoryIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {}
        for route in ROUTES:
            parser = PageReferences()
            parser.feed((ROOT / route).read_text(encoding="utf-8"))
            cls.pages[route] = parser

    def resolve_local_reference(self, route, reference):
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            return None

        relative = unquote(parsed.path)
        if relative.startswith("/"):
            target = ROOT / relative.lstrip("/")
        elif relative:
            target = ROOT / Path(route).parent / relative
        else:
            target = ROOT / route

        target = target.resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            self.fail(f"{route}: local reference escapes repository: {reference}")

        if target.is_dir() or (relative and relative.endswith("/")):
            target = target / "index.html"
        return target, unquote(parsed.fragment)

    def test_all_route_assets_and_internal_links_resolve(self):
        for route, parser in self.pages.items():
            with self.subTest(route=route):
                expected_language = ROUTES[route]
                self.assertEqual(parser.language, expected_language)

                for reference in parser.references:
                    resolved = self.resolve_local_reference(route, reference)
                    if resolved is None:
                        continue
                    target, fragment = resolved
                    self.assertTrue(
                        target.is_file(),
                        f"{route}: missing local target {reference} -> {target}",
                    )

                    target_route = target.relative_to(ROOT).as_posix()
                    if fragment and target_route in self.pages:
                        self.assertIn(
                            fragment,
                            self.pages[target_route].ids,
                            f"{route}: missing fragment #{fragment} in {target_route}",
                        )

                if parser.catalog_url:
                    resolved = self.resolve_local_reference(route, parser.catalog_url)
                    self.assertIsNotNone(resolved)
                    catalog_path, _ = resolved
                    self.assertTrue(catalog_path.is_file(), parser.catalog_url)
                    self.assertEqual(parser.catalog_language, expected_language)

    def test_four_project_cards_and_support_are_present_on_every_profile(self):
        for route in ("index.html", "ru/index.html", "es/index.html", "fr/index.html"):
            html = (ROOT / route).read_text(encoding="utf-8")
            self.assertEqual(html.count('class="work-card"'), 4, route)
            self.assertIn("Golden Greens Spatial Product System", html, route)
            self.assertIn("Sovereign Engineering Platform", html, route)
            self.assertIn("https://buymeacoffee.com/goldengreens", html, route)

    def test_four_language_catalogues_have_matching_33_offer_schema(self):
        catalogues = {}
        for language in ("en", "ru", "es", "fr"):
            path = ROOT / ("data/catalog." + language + ".json")
            with path.open(encoding="utf-8") as file:
                catalogues[language] = json.load(file)["offers"]

        expected_ids = [f"SE-{number:02d}" for number in range(1, 34)]
        english = catalogues["en"]
        for language, offers in catalogues.items():
            self.assertEqual(len(offers), 33, language)
            self.assertEqual([item["id"] for item in offers], expected_ids, language)
            for index, offer in enumerate(offers):
                with self.subTest(language=language, offer=offer.get("id")):
                    self.assertEqual(set(offer), EXPECTED_FIELDS)
                    self.assertEqual(offer["price"], english[index]["price"])
                    for field in EXPECTED_FIELDS:
                        self.assertIsInstance(offer[field], str, field)
                        self.assertTrue(offer[field].strip(), field)

    def test_brand_and_search_console_verification_assets_are_preserved(self):
        logo = ROOT / "assets/brand/golden-greens-crop-mark.svg"
        self.assertTrue(logo.is_file())
        self.assertIn("<svg", logo.read_text(encoding="utf-8").lower())

        verification = ROOT / "google1d7fc4778589f1c1.html"
        self.assertTrue(verification.is_file())
        self.assertEqual(
            verification.read_text(encoding="utf-8").strip(),
            "google-site-verification: google1d7fc4778589f1c1.html",
        )


if __name__ == "__main__":
    unittest.main()
