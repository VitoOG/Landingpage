#!/usr/bin/env python3
"""Offline SEO integrity checks for every configured page and sitemap."""
import argparse,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
S="http://www.sitemaps.org/schemas/sitemap/0.9";X="http://www.w3.org/1999/xhtml"
class P(HTMLParser):
 def __init__(self):super().__init__();self.head=False;self.title=0;self.titledepth=0;self.t=[];self.meta=[];self.links=[];self.json=[];self.j=False;self.buf=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=="head":self.head=True;return
  if not self.head:return
  if t=="title":self.title+=1;self.titledepth+=1
  if t=="meta":self.meta.append(d)
  if t=="link":self.links.append(d)
  if t=="script" and d.get("type")=="application/ld+json":self.j=True;self.buf=[]
 def handle_endtag(self,t):
  if t=="title" and self.titledepth:self.titledepth-=1
  if t=="script" and self.j:self.json.append("".join(self.buf));self.j=False
  if t=="head":self.head=False
 def handle_data(self,d):
  if self.j:self.buf.append(d)
  elif self.head and self.titledepth:self.t.append(d)
def main():
 a=argparse.ArgumentParser();a.add_argument("--site-root",default=".");a.add_argument("--config",default="seo/site-config.json");args=a.parse_args()
 root=Path(args.site_root);c=json.load(open(args.config,encoding="utf-8"));pages=c["site"]["pages"];base=c["site"]["base_url"];errors=[];groups={}
 for p in pages:groups.setdefault(p["translation_group"],[]).append(p)
 expected={}
 for g,ps in groups.items():
  d={p["language"]:p["canonical_url"] for p in ps};en=next((p for p in ps if p["language"]=="en"),None)
  if not en:errors.append("missing English in "+g)
  else:d["x-default"]=en["canonical_url"]
  expected[g]=d
 canon=set()
 for p in pages:
  f=root/p["path"]
  if not f.is_file():errors.append("missing page "+p["path"]);continue
  h=f.read_text(encoding="utf-8");q=P();q.feed(h);canon.add(p["canonical_url"])
  if h.count("<!-- BEGIN MANAGED SEO:")!=1:errors.append("managed block count "+p["path"])
  if q.title!=1 or "".join(q.t).strip()!=p["title"]:errors.append("title mismatch "+p["path"])
  for name in ("description","robots"):
   if sum((m.get("name") or "").lower()==name for m in q.meta)!=1:errors.append(name+" meta count "+p["path"])
  ca=[l.get("href") for l in q.links if "canonical" in (l.get("rel") or "").split()]
  if ca!=[p["canonical_url"]]:errors.append("canonical mismatch "+p["path"])
  alt={l.get("hreflang"):l.get("href") for l in q.links if "alternate" in (l.get("rel") or "").split() and l.get("hreflang")}
  if alt!=expected[p["translation_group"]]:errors.append("hreflang mismatch "+p["path"])
  try:
   g=json.loads(q.json[0])["@graph"];types={n["@type"]:n for n in g}
   for t in ("WebSite","Person","Organization",p["schema_type"]):
    if t not in types:errors.append("schema missing "+t+" "+p["path"])
   if "ProfilePage" in types:errors.append("unexpected ProfilePage "+p["path"])
  except Exception as e:errors.append("invalid JSON-LD "+p["path"]+": "+str(e))
 robots=(root/"robots.txt")
 if not robots.is_file() or "Sitemap: "+base+"sitemap.xml" not in robots.read_text():errors.append("robots.txt missing or sitemap mismatch")
 try:
  sm=ET.parse(root/"sitemap.xml").getroot();urls=sm.findall("{"+S+"}url");locs=[u.findtext("{"+S+"}loc") for u in urls]
  if set(locs)!=canon or len(locs)!=len(canon):errors.append("sitemap URL set mismatch")
  for u in urls:
   loc=u.findtext("{"+S+"}loc");p=next((p for p in pages if p["canonical_url"]==loc),None)
   if p:
    alt={n.attrib.get("hreflang"):n.attrib.get("href") for n in u.findall("{"+X+"}link")}
    if alt!=expected[p["translation_group"]]:errors.append("sitemap hreflang mismatch "+str(loc))
 except Exception as e:errors.append("invalid sitemap: "+str(e))
 if errors:
  print("\n".join("FAIL: "+e for e in errors));return 1
 print(f"PASS: {len(pages)} pages; canonical, grouped hreflang, JSON-LD, robots.txt and sitemap verified.")
 return 0
if __name__=="__main__":raise SystemExit(main())
