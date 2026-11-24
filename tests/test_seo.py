import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SeoTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  c=json.load(open(ROOT/"seo/site-config.json",encoding="utf-8"));self.cfg=self.root/"site-config.json";json.dump(c,open(self.cfg,"w",encoding="utf-8"),ensure_ascii=False)
  for p in c["site"]["pages"]:
   f=self.root/p["path"];f.parent.mkdir(parents=True,exist_ok=True);f.write_text(f'<html lang="{p["language"]}"><head><title>Old</title></head><body>Content</body></html>')
  subprocess.run([sys.executable,str(ROOT/"scripts/apply_seo.py"),"--site-root",str(self.root),"--config",str(self.cfg),"--no-backup"],check=True)
 def tearDown(self):self.tmp.cleanup()
 def test_six_pages_and_sitemap(self):
  r=subprocess.run([sys.executable,str(ROOT/"scripts/verify_seo.py"),"--site-root",str(self.root),"--config",str(self.cfg)],capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stdout+r.stderr)
  self.assertEqual(Path(self.root/"sitemap.xml").read_text().count("<url>"),6)
 def test_idempotent(self):
  before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file() and p!=self.cfg}
  subprocess.run([sys.executable,str(ROOT/"scripts/apply_seo.py"),"--site-root",str(self.root),"--config",str(self.cfg),"--no-backup"],check=True)
  after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file() and p!=self.cfg}
  self.assertEqual(before,after)
if __name__=="__main__":unittest.main()
