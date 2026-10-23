from data_store import read_document, document_bytes, document_text
"""Local schema registry; validation never retrieves remote schemas."""
import json
from pathlib import Path
import jsonschema
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]

def record_validator(schema):
    category = read_document('schemas/category.schema.json', root=ROOT)
    registry = Registry().with_resource(category['$id'], Resource.from_contents(category))
    return jsonschema.Draft202012Validator(schema, registry=registry)
