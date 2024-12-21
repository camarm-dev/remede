import os
import sqlite3
import json
from hashlib import md5

from jsonschema import validate


def check_validity(db_path: str, schema_path: str = None):
    with open(schema_path) as f:
        schema = json.loads(f.read())
    db = sqlite3.connect(db_path, check_same_thread=False)
    db_cursor = db.cursor()
    all_documents = db_cursor.execute("SELECT document FROM dictionary").fetchall()
    db_cursor.close()

    errors = 0
    total = len(all_documents)
    current = 0

    for row in all_documents:
        current += 1
        doc = json.loads(row[0])
        if not doc:
            continue
        try:
            validate(doc, schema)
        except Exception as e:
            print(e)
            return False
        print(f"\033[A\033[KChecking JSON schemas validity... {current}/{total} | {errors} erreurs")
    return True


def save(results: dict, slug: str):
    with open('validity.json', 'w') as f:
        data = json.loads(f.read())
        data[slug] = results
        f.write(json.dumps(data))


if __name__ == '__main__':
    databases = list(filter(lambda x: x.endswith('.db'), os.listdir('data')))
    schemas = list(filter(lambda x: x.endswith('schema.json'), os.listdir('docs')))
    print("Available databases:")
    for file in databases:
        print(f"[{databases.index(file)}] {file}")
    database_choice = databases[int(input("Select database : "))]
    print("Available schemas:")
    for file in schemas:
        print(f"[{schemas.index(file)}] {file}")
    schema_choice = schemas[int(input("Select schema : "))]
    print(f"Checking {database_choice} with {schema_choice}\n\n")

    result = check_validity(f"data/{database_choice}", f"docs/{schema_choice}")

    print("Check is finished, saving results...")
    data = {
        "hash": md5(open(f'data/{database_choice}', 'rb').read()).hexdigest()[0:7],
        "valid": result,
        "schema": schema_choice
    }
    slug = database_choice[:-3]
    save(data, slug)
