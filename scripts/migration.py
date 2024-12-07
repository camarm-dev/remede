import os
import sqlite3
import json
from hashlib import md5

from jsonschema import validate


def migration(database):
    cursor = database.cursor()
    all_documents = cursor.execute("SELECT document, word FROM dictionary").fetchall()
    total = len(all_documents)
    current = 0
    for row in all_documents:
        current += 1
        word = row[1]
        doc = json.loads(row[0])
        new_doc = migrate_doc(doc)
        cursor.execute("UPDATE dictionary SET document=? WHERE word=?", (json.dumps(new_doc), word))
        print(f"\033[A\033[KMigrating database... {current}/{total}")
    cursor.close()
    database.commit()


def migrate_doc(doc: dict | bool):
    if not doc:
        return doc
    for definition in doc['definitions']:
        plurals = definition['plurals']
        del definition['plurals']
        doc['plurals'] = plurals
    return doc


if __name__ == '__main__':
    print("Migration: plurals to global value")
    db = sqlite3.connect('data/remede.db', check_same_thread=False)
    migration(db)
    print("Done.")
