import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "index.html": {
        "language": "en",
        "labels": ["Profile", "Scope", "Services", "Full catalogue", "Selected work", "Method", "Contact"],
        "hrefs": ["#profile", "#scope", "#services", "services/", "#work", "#method", "#contact"],
        "language_hrefs": {"en": "./", "ru": "ru/", "es": "es/", "fr": "fr/"},
    },
    "ru/index.html": {
        "language": "ru",
        "labels": ["Профиль", "Области работы", "Услуги", "Каталог услуг", "Проекты", "Метод", "Контакт"],
        "hrefs": ["#profile", "#scope", "#services", "services/", "#work", "#method", "#contact"],
        "language_hrefs": {"en": "../", "ru": "./", "es": "../es/", "fr": "../fr/"},
    },
    "es/index.html": {
        "language": "es",
        "labels": ["Perfil", "Áreas de trabajo", "Servicios", "Catálogo completo", "Proyectos seleccionados", "Método", "Contacto"],
        "hrefs": ["#profile", "#scope", "#services", "services/", "#work", "#method", "#contact"],
        "language_hrefs": {"en": "../", "ru": "../ru/", "es": "./", "fr": "../fr/"},
    },
    "fr/index.html": {
        "language": "fr",
        "labels": ["Profil", "Domaines d’intervention", "Services", "Catalogue complet", "Projets sélectionnés", "Méthode", "Contact"],
        "hrefs": ["#profile", "#scope", "#services", "services/", "#work", "#method", "#contact"],
        "language_hrefs": {"en": "../", "ru": "../ru/", "es": "../es/", "fr": "./"},
    },
    "services/index.html": {
        "language": "en",
        "labels": ["Profile", "Scope", "Services", "Full catalogue", "Selected work", "Method", "Contact"],
        "hrefs": ["../#profile", "../#scope", "../#services", "./", "../#work", "../#method", "../#contact"],
        "language_hrefs": {"en": "./", "ru": "../ru/services/", "es": "../es/services/", "fr": "../fr/services/"},
    },
    "ru/services/index.html": {
        "language": "ru",
        "labels": ["Профиль", "Области работы", "Услуги", "Каталог услуг", "Проекты", "Метод", "Контакт"],
        "hrefs": ["../../ru/#profile", "../../ru/#scope", "../../ru/#services", "./", "../../ru/#work", "../../ru/#method", "../../ru/#contact"],
        "language_hrefs": {"en": "../../services/", "ru": "./", "es": "../../es/services/", "fr": "../../fr/services/"},
    },
    "es/services/index.html": {
        "language": "es",
        "labels": ["Perfil", "Áreas de trabajo", "Servicios", "Catálogo completo", "Proyectos seleccionados", "Método", "Contacto"],
        "hrefs": ["../../es/#profile", "../../es/#scope", "../../es/#services", "./", "../../es/#work", "../../es/#method", "../../es/#contact"],
        "language_hrefs": {"en": "../../services/", "ru": "../../ru/services/", "es": "./", "fr": "../../fr/services/"},
    },
    "fr/services/index.html": {
        "language": "fr",
        "labels": ["Profil", "Domaines d’intervention", "Services", "Catalogue complet", "Projets sélectionnés", "Méthode", "Contact"],
        "hrefs": ["../../fr/#profile", "../../fr/#scope", "../../fr/#services", "./", "../../fr/#work", "../../fr/#method", "../../fr/#contact"],
        "language_hrefs": {"en": "../../services/", "ru": "../../ru/services/", "es": "../../es/services/", "fr": "./"},
    },
}


class HeaderParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_nav = False
        self.current_link = None
        self.links = []
        self.in_subtitle = False
        self.subtitle_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if tag == "nav" and attrs.get("id") == "primary-navigation":
            self.in_nav = True
        if tag == "span" and "wordmark-subtitle" in classes:
            self.in_subtitle = True
        if tag == "a" and self.in_nav:
            self.current_link = {"attrs": attrs, "parts": []}

    def handle_endtag(self, tag):
        if tag == "a" and self.current_link is not None:
            self.links.append(self.current_link)
            self.current_link = None
        elif tag == "span" and self.in_subtitle:
            self.in_subtitle = False
        elif tag == "nav" and self.in_nav:
            self.in_nav = False

    def handle_data(self, data):
        if self.current_link is not None:
            self.current_link["parts"].append(data)
        if self.in_subtitle:
            self.subtitle_parts.append(data)


class NavigationContractTests(unittest.TestCase):
    def test_all_routes_share_brand_and_localized_navigation(self):
        for route, expected in PAGES.items():
            with self.subTest(route=route):
                parser = HeaderParser()
                parser.feed((ROOT / route).read_text(encoding="utf-8"))

                subtitle = " ".join(" ".join(parser.subtitle_parts).split())
                self.assertEqual(subtitle, "ENGINEERING & R&D")

                menu = [item for item in parser.links if not item["attrs"].get("lang")]
                labels = [
                    " ".join(" ".join(item["parts"]).replace("↗", "").split())
                    for item in menu
                ]
                self.assertEqual(labels, expected["labels"])
                self.assertEqual([item["attrs"].get("href") for item in menu], expected["hrefs"])

                catalogue_current = menu[3]["attrs"].get("aria-current")
                self.assertEqual(
                    catalogue_current,
                    "page" if route.endswith("services/index.html") else None,
                )

    def test_language_switch_targets_and_current_locale(self):
        for route, expected in PAGES.items():
            with self.subTest(route=route):
                parser = HeaderParser()
                parser.feed((ROOT / route).read_text(encoding="utf-8"))
                language_links = {
                    item["attrs"].get("lang"): item
                    for item in parser.links
                    if item["attrs"].get("lang")
                }
                self.assertEqual(set(language_links), {"en", "ru", "es", "fr"})
                self.assertEqual(
                    {lang: item["attrs"].get("href") for lang, item in language_links.items()},
                    expected["language_hrefs"],
                )
                for lang, item in language_links.items():
                    self.assertEqual(
                        item["attrs"].get("aria-current") == "page",
                        lang == expected["language"],
                    )


if __name__ == "__main__":
    unittest.main()
