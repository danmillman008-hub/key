"""Recover MAZ schedule geometry, not flat OCR order. Every cell retains bbox and fill.
Only pages with row-date rectangles AND time-column rectangles qualify.
"""
import pathlib,re,json,unicodedata,collections
import pymupdf as f
OUT=pathlib.Path('data');OUT.mkdir(exist_ok=True)
TRANS=str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩','01234567890123456789')
def norm(t):return unicodedata.normalize('NFKC',t).translate(TRANS).replace('ي','ی').replace('ك','ک').replace('ƽ','ر').replace('Ƽ','ر').replace('Ƹ','ی').replace('ƭ','ی').replace('ƾ','ز').strip()
def category(t,fill):
 if 'مدرسه' in t:return 'school'
 if 'تحلیل' in t and 'آ' in t:return 'exam_analysis'
 if 'آ' in t and 'ماز' in t:return 'exam'
 if 'مروری' in t:return 'review'
 if 'تست' in t:return 'test'
 if 'مطالعه' in t:return 'learn'
 if 'کلاس' in t:return 'class'
 if 'استراحت' in t or 'ناهار' in t:return 'rest'
 if not t:
  if fill and max(fill)-min(fill)>.12:return 'colored_empty_reservation'
  return 'empty_flex_or_unclassified'
 return 'other'
alltables=[]
for file in sorted(pathlib.Path('google_drive').rglob('*.pdf')):
 if '@Bank' in file.name:continue
 doc=f.open(file)
 for pi,p in enumerate(doc):
  if p.rect.width<p.rect.height:continue
  drawings=p.get_drawings(); rects=[]
  for d in drawings:
   r=d['rect']
   if d['fill'] is not None and 35<r.width<150 and 20<r.height<115:
    t=norm(p.get_text(clip=r));rects.append((r,t,list(d['fill'])))
  dates=[v for v in rects if v[0].x0>p.rect.width*.8 and any(x in v[1] for x in ['آبان','مهر','مرداد','شهریور','آذر','دی']) and v[0].y0>70]
  if len(dates)<5:continue
  rightmost=max(v[0].x0 for v in dates)
  dates=[v for v in dates if abs(v[0].x0-rightmost)<5]
  dates.sort(key=lambda v:(v[0].y0+v[0].y1)/2)
  grouped=[]
  for v in dates:
   cy=(v[0].y0+v[0].y1)/2
   if grouped and abs(cy-(grouped[-1][0][0].y0+grouped[-1][0][0].y1)/2)<15:grouped[-1].append(v)
   else:grouped.append([v])
  dates=[max(g,key=lambda v:len(v[1])) for g in grouped]
  firsty=dates[0][0].y0
  headers=[v for v in rects if re.search(r'\d+:\d+',v[1]) and v[0].y1<=firsty+10 and v[0].x1<dates[0][0].x0+5]
  # Keep the lowest header band; remove unrelated header texts.
  if len(headers)<4:continue
  hy=max(v[0].y0 for v in headers);headers=[v for v in headers if abs(v[0].y0-hy)<8]
  headers.sort(key=lambda v:-v[0].x0)
  cells=[]
  for ri,(dr,day,_) in enumerate(dates):
   cy=(dr.y0+dr.y1)/2
   for ci,(hr,time,_) in enumerate(headers):
    cx=(hr.x0+hr.x1)/2
    hits=[v for v in rects if abs((v[0].x0+v[0].x1)/2-cx)<10 and abs((v[0].y0+v[0].y1)/2-cy)<10]
    if hits:
     r,t,color=min(hits,key=lambda v:abs(v[0].width-hr.width)+abs((v[0].y0+v[0].y1)/2-cy))
     status='vector_cell'
    else:
     r=f.Rect(hr.x0,dr.y0,hr.x1,dr.y1);t=norm(p.get_text(clip=r));color=None;status='inferred_grid_bbox'
    kind=category(t,color)
    cells.append(dict(row=ri,column=ci,day_label=day,time_label=time,bbox=[round(x,3) for x in r],fill=color,text=t,kind=kind,geometry_status=status))
  counts=dict(collections.Counter(x['kind'] for x in cells))
  if not any(counts.get(k,0) for k in ['learn','test','review']):tabletype='blank_self_fill'
  else:tabletype='filled_or_mixed'
  alltables.append(dict(id=f'{file.stem}-p{pi+1}',file=str(file),pdf_page=pi+1,table_type=tabletype,rows=len(dates),columns=len(headers),counts=counts,cells=cells,visual_review='not_yet',note='Extraction candidates; empty colored class reservations are not free study time.'))
  print(file.name,pi+1,len(dates),len(headers),counts,flush=True)
(OUT/'maz_tables.json').write_text(json.dumps(alltables,ensure_ascii=False,indent=2))
print('TABLES',len(alltables),'CELLS',sum(len(t['cells']) for t in alltables))
