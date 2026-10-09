#!/usr/bin/env python3
"""Build the public DnA Techy Master Logo & Icon Library from upstream vectors."""
from __future__ import annotations
import csv, io, json, re, shutil, tempfile, urllib.request, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BLUE="#0B63CE"; DARK="#082B62"; UA="DnATechy-Master-Logo-Icon-Library/1.0"
GENERATED=["Brand_Logos","General_Icons_Solid","General_Icons_Regular","Featured_Color_Logos"]
ALIASES={
 "power-bi":["powerbi","microsoft-power-bi","business-intelligence"],
 "power-automate":["powerautomate","microsoft-power-automate","flow"],
 "power-query":["powerquery","microsoft-power-query","etl"],
 "power-apps":["powerapps","microsoft-power-apps"],
 "google-apps-script":["googleappsscript","apps-script","appsscript"],
 "microsoft-excel":["excel","ms-excel","xlsx"],"python":["python-language"],
 "amazon-web-services":["aws","amazon-aws"],"microsoft-azure":["azure"],"google-cloud":["gcp","google-cloud-platform"]}
PRODUCTS={
 "power-bi":"https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-BI.svg",
 "power-automate":"https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-Automate-Colored.svg",
 "power-query":"https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-Query-Colored.svg",
 "power-apps":"https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-Apps-Colored.svg",
 "dataverse":"https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Dataverse-Colored.svg",
 "power-pages":"https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-Pages.svg",
 "google-apps-script":"https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_Apps_Script.svg",
 "python":"https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg"}

def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
 with urllib.request.urlopen(req,timeout=120) as r:return r.read()
def text(url):return get(url).decode("utf-8")
def latest(repo,branch):
 try:
  meta=json.loads(text(f"https://api.github.com/repos/{repo}/releases/latest")); u=meta.get("zipball_url")
  if u:return get(u)
 except Exception as e:print("release lookup:",repo,e)
 return get(f"https://github.com/{repo}/archive/refs/heads/{branch}.zip")
def unzip(data,d):
 with zipfile.ZipFile(io.BytesIO(data)) as z:z.extractall(d)
 ds=[p for p in d.iterdir() if p.is_dir()];return ds[0] if len(ds)==1 else d
def finddir(root,suffix):
 for p in root.rglob("*"):
  if p.is_dir() and p.as_posix().endswith(suffix):return p
 return None
def slug(s):return re.sub(r"[^a-z0-9]+","-",s.lower().replace("&"," and ")).strip("-") or "icon"
def strip(s):
 s=re.sub(r"^\s*<\?xml[^>]*\?>\s*","",s,flags=re.I);return re.sub(r"<!DOCTYPE.*?>","",s,flags=re.I|re.S).strip()
def vb(s):
 m=re.search(r'viewBox\s*=\s*["\']([^"\']+)',s,re.I)
 if m:return m.group(1)
 w=re.search(r'width\s*=\s*["\']([\d.]+)',s,re.I);h=re.search(r'height\s*=\s*["\']([\d.]+)',s,re.I)
 return f"0 0 {w.group(1)} {h.group(1)}" if w and h else "0 0 512 512"
def inner(s):
 m=re.search(r"<svg\b[^>]*>(.*)</svg>\s*$",strip(s),re.I|re.S);return m.group(1) if m else strip(s)
def recolor(x,c):return f'<style>path,rect,circle,ellipse,polygon,polyline,line{{fill:{c}!important;stroke:{c}!important}}[fill="none"]{{fill:none!important}}</style>'+x
def trans(s,c):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb(s)}">{recolor(inner(s),c)}</svg>'
def framed(s,bg,shape):
 base=f'<circle cx="32" cy="32" r="30" fill="{bg}"/>' if shape=="circle" else f'<rect x="2" y="2" width="60" height="60" rx="12" fill="{bg}"/>'
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{base}<svg x="14" y="14" width="36" height="36" viewBox="{vb(s)}">{recolor(inner(s),"#FFFFFF")}</svg></svg>'
def variants(s):
 s=strip(s);return {"00_Raw_Source":s,"01_Transparent_Black":trans(s,"#000000"),"02_Transparent_White":trans(s,"#FFFFFF"),"03_Circle_Blue":framed(s,BLUE,"circle"),"04_Circle_Dark":framed(s,DARK,"circle"),"05_Rounded_Square_Blue":framed(s,BLUE,"square"),"06_Rounded_Square_Dark":framed(s,DARK,"square")}
def title(s):
 o={"power-bi":"Power BI","power-automate":"Power Automate","power-query":"Power Query","power-apps":"Power Apps","google-apps-script":"Google Apps Script","amazon-web-services":"Amazon Web Services (AWS)","microsoft-azure":"Microsoft Azure","google-cloud":"Google Cloud (GCP)","microsoft-excel":"Microsoft Excel"}
 return o.get(s," ".join(x.upper() if x in {"aws","gcp","sql","api","bi"} else x.capitalize() for x in s.split("-")))
def write_set(base,name,svg,cat,source,index,aliases=()):
 name=slug(name); names=sorted({name,*[slug(x) for x in aliases]}); v=variants(svg); keywords=" ".join(sorted(set(names+name.split("-")+title(name).lower().split())))
 suffix={"00_Raw_Source":"raw-source","01_Transparent_Black":"transparent-black","02_Transparent_White":"transparent-white","03_Circle_Blue":"circle-blue","04_Circle_Dark":"circle-dark","05_Rounded_Square_Blue":"square-blue","06_Rounded_Square_Dark":"square-dark"}
 for a in names:
  for folder,content in v.items():
   p=base/folder/f'{a}__{"logo" if cat=="brand" else "icon"}__{suffix[folder]}.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding="utf-8")
   index.append({"name":title(name),"slug":a,"category":cat,"variant":folder,"path":p.relative_to(ROOT).as_posix(),"source":source,"keywords":keywords})

def build():
 for d in GENERATED:shutil.rmtree(ROOT/d,ignore_errors=True)
 for f in ["Icon_Index.json","Icon_Index.csv","BUILD_SUMMARY.json"]:
  try:(ROOT/f).unlink()
  except FileNotFoundError:pass
 idx=[];seen=set()
 with tempfile.TemporaryDirectory(prefix="dna-icons-") as td:
  t=Path(td);print("Downloading Simple Icons...");sr=unzip(latest("simple-icons/simple-icons","develop"),t/"si");sid=finddir(sr,"/icons")
  if not sid:raise RuntimeError("Simple Icons folder not found")
  fs=sorted(sid.glob("*.svg"))
  for i,f in enumerate(fs,1):
   n=slug(f.stem);write_set(ROOT/"Brand_Logos",n,f.read_text(encoding="utf-8"),"brand","Simple Icons",idx,ALIASES.get(n,[]));seen.update({n,*map(slug,ALIASES.get(n,[]))})
   if i%500==0:print(" brands",i,"/",len(fs))
  print("Downloading Font Awesome Free...");fr=unzip(latest("FortAwesome/Font-Awesome","7.x"),t/"fa");bd=finddir(fr,"/svgs/brands");sd=finddir(fr,"/svgs/solid");rd=finddir(fr,"/svgs/regular")
  if not sd or not rd:raise RuntimeError("Font Awesome SVG folders not found")
  if bd:
   for f in sorted(bd.glob("*.svg")):
    n=slug(f.stem)
    if n not in seen:write_set(ROOT/"Brand_Logos",n,f.read_text(encoding="utf-8"),"brand","Font Awesome Free",idx,ALIASES.get(n,[]));seen.add(n)
  for typ,dest,src in [("solid",ROOT/"General_Icons_Solid",sd),("regular",ROOT/"General_Icons_Regular",rd)]:
   fs=sorted(src.glob("*.svg"));print(typ,len(fs))
   for f in fs:write_set(dest,slug(f.stem),f.read_text(encoding="utf-8"),f"general-{typ}","Font Awesome Free",idx)
  feat=ROOT/"Featured_Color_Logos"/"SVG";png=ROOT/"Featured_Color_Logos"/"PNG_2048";feat.mkdir(parents=True,exist_ok=True);png.mkdir(parents=True,exist_ok=True)
  for n,u in PRODUCTS.items():
   try:
    s=text(u);write_set(ROOT/"Brand_Logos",n,s,"brand",u,idx,ALIASES.get(n,[]));(feat/f"{n}.svg").write_text(strip(s),encoding="utf-8")
   except Exception as e:print("WARNING product",n,e)
  try:
   import cairosvg
   for f in feat.glob("*.svg"):
    try:cairosvg.svg2png(url=str(f),write_to=str(png/f"{f.stem}.png"),output_width=2048,output_height=2048)
    except Exception as e:print("PNG warning",f.name,e)
  except Exception:print("CairoSVG not installed; featured PNGs skipped")
 dedup={r["path"]:r for r in idx};idx=sorted(dedup.values(),key=lambda r:(r["category"],r["name"].lower(),r["variant"],r["path"]))
 (ROOT/"Icon_Index.json").write_text(json.dumps(idx,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
 with (ROOT/"Icon_Index.csv").open("w",newline="",encoding="utf-8-sig") as h:
  w=csv.DictWriter(h,fieldnames=["name","slug","category","variant","path","source","keywords"]);w.writeheader();w.writerows(idx)
 summary={"indexed_files":len(idx),"brand_records":sum(r["category"]=="brand" for r in idx),"solid_records":sum(r["category"]=="general-solid" for r in idx),"regular_records":sum(r["category"]=="general-regular" for r in idx),"generated_by":"tools/build_library.py"}
 (ROOT/"BUILD_SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2))
if __name__=="__main__":build()
