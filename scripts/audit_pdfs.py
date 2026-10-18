"""Extract every page's native text, words, links, annotations and vector/image geometry.
Raw extracts/renders are internal; the compact coverage index is version-controlled.
Usage: .venv/bin/python scripts/audit_pdfs.py
"""
import hashlib,json,pathlib,unicodedata,zipfile
import pymupdf
root=pathlib.Path('google_drive');out=pathlib.Path('.work/full');out.mkdir(parents=True,exist_ok=True)
for z in root.glob('*.zip'):
 with zipfile.ZipFile(z) as archive:
  image_doc=pymupdf.open()
  image_names=[]
  for item in sorted(archive.infolist(),key=lambda i:i.filename):
   if not item.is_dir() and pathlib.Path(item.filename).suffix.lower()=='.pdf':
    # No archive path traversal; flatten filenames to a dedicated directory.
    dest=root/'archive';dest.mkdir(exist_ok=True)
    (dest/pathlib.Path(item.filename).name).write_bytes(archive.read(item))
   elif not item.is_dir() and pathlib.Path(item.filename).suffix.lower() in {'.jpg','.jpeg','.png'}:
    img=pymupdf.open(stream=archive.read(item),filetype=pathlib.Path(item.filename).suffix[1:])
    image_doc.insert_pdf(pymupdf.open(stream=img.convert_to_pdf(),filetype='pdf'))
    image_names.append(item.filename)
  if len(image_doc):
   dest=root/'archive';dest.mkdir(exist_ok=True)
   image_doc.save(dest/(z.stem.lstrip('@')+'-images.pdf'))
   (dest/(z.stem.lstrip('@')+'-images.json')).write_text(json.dumps(image_names,ensure_ascii=False))
index=[];ocr=[]
for file in sorted(root.rglob('*.pdf')):
 sha=hashlib.sha256(file.read_bytes()).hexdigest();folder=out/sha[:12];folder.mkdir(exist_ok=True)
 doc=pymupdf.open(file);pages=[]
 for n,p in enumerate(doc):
  text=unicodedata.normalize('NFKC',p.get_text())
  imgs=[dict(xref=i[0],width=i[2],height=i[3]) for i in p.get_images()]
  vectors=[dict(rect=list(x['rect']),fill=x['fill'],color=x['color'],type=x['type']) for x in p.get_drawings()]
  annot=[dict(type=a.type,rect=list(a.rect),info=a.info) for a in (p.annots() or [])]
  record=dict(page=n+1,rect=list(p.rect),text=text,words=p.get_text('words'),images=imgs,vectors=vectors,links=p.get_links(),annotations=annot)
  (folder/f'{n+1:04}.json').write_text(json.dumps(record,ensure_ascii=False,default=str))
  pix=p.get_pixmap(matrix=pymupdf.Matrix(.35,.35));pix.save(str(folder/f'{n+1:04}-thumb.png'))
  pages.append(dict(page=n+1,native_chars=len(text.strip()),images=len(imgs),vectors=len(vectors),annotations=len(annot),links=len(record['links']),automatic_extracted=True,thumbnail_rendered=True,visual_review=False))
  large_image=any(pymupdf.Rect(i['bbox']).get_area()>.6*p.rect.get_area() for i in p.get_image_info())
  watermark_only='@kotob_konkoria' in text and len(text.strip())<1000
  if len(text.strip())<100 or watermark_only or (large_image and len(text.strip())<1000):
   ocr.append(dict(file=str(file.resolve()),page=n+1,output=str((folder/f'{n+1:04}-ocr.json').resolve())))
 (folder/'native.txt').write_text(''.join(f'\n=== PDF PAGE {i+1} ===\n'+unicodedata.normalize('NFKC',p.get_text()) for i,p in enumerate(doc)))
 index.append(dict(file=str(file),sha256=sha,pages=len(doc),internal_folder=str(folder),page_audit=pages))
 print(file.name,len(doc),flush=True)
pathlib.Path('research/page_audit.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
(out/'ocr_tasks.json').write_text(json.dumps(ocr))
print('TOTAL',len(index),sum(x['pages'] for x in index),'OCR tasks',len(ocr),flush=True)
