"""Local schema registry; validation never retrieves remote schemas."""
import json
from pathlib import Path
import jsonschema
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]

def record_validator(schema):
    category = json.loads((ROOT / 'schemas/category.schema.json').read_text())
    registry = Registry().with_resource(category['$id'], Resource.from_contents(category))
    return jsonschema.Draft202012Validator(schema, registry=registry)
