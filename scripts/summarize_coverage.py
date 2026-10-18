"""Record automatic extraction/OCR coverage without claiming semantic validation."""
import collections
import json
import pathlib

index_path = pathlib.Path('research/page_audit.json')
index = json.loads(index_path.read_text())
targets = json.loads(pathlib.Path('.work/full/ocr_tasks.json').read_text())
target_keys = {(x['file'], x['page']) for x in targets}
statuses = collections.Counter()
for source in index:
    folder = pathlib.Path(source['internal_folder'])
    for page in source['page_audit']:
        key = (str(pathlib.Path(source['file']).resolve()), page['page'])
        page['ocr_target'] = key in target_keys
        ocr_file = folder / f"{page['page']:04}-ocr.json"
        if page['ocr_target']:
            if ocr_file.exists():
                record = json.loads(ocr_file.read_text())
                page['ocr_status'] = record['status']
                page['ocr_confidence_engine_only'] = record.get('confidence')
            else:
                page['ocr_status'] = 'pending'
            statuses[page['ocr_status']] += 1
index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
summary = dict(files=len(index), pages=sum(x['pages'] for x in index),
               ocr_target_pages=len(targets), ocr_status=dict(statuses),
               visual_review_manifest='research/visual_review.json',
               warning='Automatic extraction, OCR and thumbnail generation are NOT full semantic or visual review.')
pathlib.Path('research/coverage_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(summary)
