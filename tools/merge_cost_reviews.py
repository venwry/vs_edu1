"""Losslessly consolidate existing review outputs; never recalculate estimates."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def merge(root=ROOT):
    target = root / 'generated/models/manufacturing-costs.json'
    model = json.loads(target.read_text())
    for key in ('ncc-1982', 'comdex-1982'):
        name = 'ncc-1982-review.json' if key == 'ncc-1982' else 'comdex-1982-cost-review.json'
        source = target.parent / name
        if source.exists():
            model.setdefault('reviews', {})[key] = json.loads(source.read_text())
    target.write_text(json.dumps(model, ensure_ascii=False, indent=2) + '\n')
    for name in ('ncc-1982-review.json', 'comdex-1982-cost-review.json'):
        (target.parent / name).unlink(missing_ok=True)
if __name__ == '__main__':
    merge()
