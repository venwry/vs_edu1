"""Resolve legacy source names in immutable provenance records after the directory move."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATHS=json.loads((ROOT/'data/manifest.json').read_text())['paths']
def resolve_path(path):
    return PATHS.get(path,path)
