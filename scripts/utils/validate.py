import json
from jsonschema import validate

with open('data/remede.schema.json') as f:
    SCHEMA = json.loads(f.read())


def validate_doc(document: dict, schema: str = None):
    if not schema:
        schema = SCHEMA
    else:
        with open(schema) as f:
            schema = json.loads(f.read())
    try:
        validate(document, schema)
        return True, ""
    except Exception as e:
        return False, e
