import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGES={
"index.html":("en",["Scope","Services","Full catalogue","Cart","Selected work","Method","Contact"],["#scope","#services","services/","cart/","#work","#method","#contact"],{"en":"./","ru":"ru/"}),
"ru/index.html":("ru",["Области работы","Услуги","Каталог услуг","Корзина","Проекты","Метод","Контакт"],["#scope","#services","services/","cart/","#work","#method","#contact"],{"en":"../","ru":"./"}),
"services/index.html":("en",["Scope","Services","Full catalogue","Cart","Selected work","Method","Contact"],["../#scope","../#services","./","../cart/","../#work","../#method","../#contact"],{"en":"./","ru":"../ru/services/"}),
"ru/services/index.html":("ru",["Области работы","Услуги","Каталог услуг","Корзина","Проекты","Метод","Контакт"],["../../ru/#scope","../../ru/#services","./","../../ru/cart/","../../ru/#work","../../ru/#method","../../ru/#contact"],{"en":"../../services/","ru":"./"}),
"cart/index.html":("en",["Scope","Services","Full catalogue","Cart","Selected work","Method","Contact"],["../#scope","../#services","../services/","./","../#work","../#method","../#contact"],{"en":"./","ru":"../ru/cart/"}),
"ru/cart/index.html":("ru",["Области работы","Услуги","Каталог услуг","Корзина","Проекты","Метод","Контакт"],["../../ru/#scope","../../ru/#services","../services/","./","../../ru/#work","../../ru/#method","../../ru/#contact"],{"en":"../../cart/","ru":"./"})}
class P(HTMLParser):
 def __init__(self):
  super().__init__();self.nav=False;self.a=None;self.links=[];self.skip=False
 def handle_starttag(self,t,a):
  a=dict(a);c=(a.get("class") or "").split()
  if t=="nav" and a.get("id")=="primary-navigation":self.nav=True
  if t=="span" and "cart-count" in c:self.skip=True
  if t=="a" and self.nav:self.a={"attrs":a,"text":[]}
 def handle_endtag(self,t):
  if t=="a" and self.a is not None:self.links.append(self.a);self.a=None
  if t=="span":self.skip=False
  if t=="nav":self.nav=False
 def handle_data(self,d):
  if self.a is not None and not self.skip:self.a["text"].append(d)
class NavigationTests(unittest.TestCase):
 def test_localized_navigation(self):
  for path,(lang,labels,hrefs,langs) in PAGES.items():
   with self.subTest(path=path):
    p=P();p.feed((ROOT/path).read_text())
    menu=[x for x in p.links if not x["attrs"].get("lang")]
    self.assertEqual([" ".join(" ".join(x["text"]).replace("↗","").split()) for x in menu],labels)
    self.assertEqual([x["attrs"].get("href") for x in menu],hrefs)
    ll={x["attrs"]["lang"]:x for x in p.links if x["attrs"].get("lang")}
    self.assertEqual({k:v["attrs"]["href"] for k,v in ll.items()},langs)
 def test_catalogue_has_33_and_ordering(self):
  import json
  for path in ["data/catalog.en.json","data/catalog.ru.json"]:
   data=json.loads((ROOT/path).read_text())
   self.assertEqual(len(data["offers"]),33)
   self.assertEqual(len({x["id"] for x in data["offers"]}),33)
  for path in ["services/index.html","ru/services/index.html"]:
   text=(ROOT/path).read_text()
   self.assertIn("catalog-add", (ROOT/"js/catalog.js").read_text())
  for path in ["cart/index.html","ru/cart/index.html"]:
   text=(ROOT/path).read_text()
   self.assertIn("service-order-form",text)
   self.assertIn("d39653f1-c848-4022-81f2-1d0e2c4d57fd",text)
if __name__=="__main__":unittest.main()
