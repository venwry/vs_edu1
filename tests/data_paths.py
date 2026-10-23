"""Shared source reader and immutable-provenance path aliases."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from data_store import read_document, document_text, document_bytes, registry

def resolve_path(path):return registry()['legacy_paths'].get(path,path)
