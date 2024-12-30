import datetime
import json
import os
import sqlite3
import threading
from enum import Enum
from hashlib import md5

import frontmatter
import markdown
import requests
import unidecode
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from scripts.utils.sources import SOURCES
from sqlite3 import Cursor

lock = threading.Lock()
version = "1.4.0"
app = FastAPI(title='Remède', description='Un dictionnaire libre.', version=version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

default_cursor = sqlite3.connect(':memory:').cursor()

DATABASES = {
    "remede": default_cursor,
    "remede.en": default_cursor
}

class BinariesVariant(str, Enum):
    aarch_dmg = "aarch64.dmg"
    aarch_app = "aarch64.app.tar.gz"
    x64_dmg = "x64.dmg"
    x64_app = "x64.app.tar.gz"
    apk = "apk"
    deb = "deb"
    exe = "exe"
    msi = "msi"


def get_stats(db_path: str):
    db = sqlite3.connect(db_path, check_same_thread=False)
    db_cursor = db.cursor()
    total = db_cursor.execute("SELECT COUNT(*) FROM dictionary").fetchone()[0]
    db_cursor.close()
    return total


def check_validity(slug: str):
    with open('validity.json', 'r') as f:
        data = json.loads(f.read())
        return data.get(slug, {'valid': False, 'schema': 'schema.json', 'hash': ''})


def in_json(response: str | list):
    return json.loads(json.dumps(response))


def fetch_random_word(database: Cursor = DATABASES['remede']):
    lock.acquire(True)
    return database.execute("SELECT word FROM dictionary WHERE nature != 'VER' AND nature != '' ORDER BY RANDOM() LIMIT 1").fetchone()[0]


def fetch_words_with_phoneme(phoneme: str, database: Cursor = DATABASES['remede']):
    lock.acquire(True)
    results = database.execute("SELECT word, document FROM dictionary WHERE phoneme = ?", (phoneme,)).fetchall()
    return list(map(lambda x: (x[0], json.loads(x[1])), results))  # [('word' {..doc})]


def fetch_remede_word_of_day(database: Cursor = DATABASES['remede'], database_identifier: str = 'remede'):
    global WORD_OF_DAY
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    if today != WORD_OF_DAY['date'] or not WORD_OF_DAY.get(f'word.{database_identifier}', None):
        WORD_OF_DAY['date'] = today
        WORD_OF_DAY[f'word.{database_identifier}'] = fetch_random_word(database)
        lock.release()
    return WORD_OF_DAY[f'word.{database_identifier}']


def fetch_remede_doc(word: str, database: Cursor = DATABASES['remede']):
    lock.acquire(True)
    response = database.execute("SELECT document FROM dictionary WHERE word = ?", (word,)).fetchone()
    return response[0] if response else json.dumps({'message': 'Mot non trouvé'})


def fetch_autocomplete(query: str, limit: bool = False, page: int = 0, database: Cursor = DATABASES['remede']):
    lock.acquire(True)
    if limit:
        response = database.execute(
            "SELECT word FROM dictionary WHERE indexed LIKE ? ORDER BY lower(word) ASC LIMIT 5", (query + '%',)).fetchall()
    else:
        response = database.execute(
            "SELECT word FROM dictionary WHERE indexed LIKE ? ORDER BY lower(word) ASC LIMIT 50 OFFSET ?", (query + '%', page * 50)).fetchall()
    return list(map(lambda row: row[0], response))


def get_sheets():
    files = os.listdir('data/fiches')
    sheets = []
    for filename in files:
        with open(f'data/fiches/{filename}') as file:
            metadata = frontmatter.load(file)
            metadata['credits']['text'] = markdown.markdown(metadata['credits']['text'])
            sheets.append({
                'nom': metadata['nom'],
                'description': metadata['description'],
                'tags': metadata['tags'],
                'credits': metadata['credits'],
                'slug': metadata['slug'],
                'contenu': markdown.markdown(metadata.content),
                'path': f'data/fiches/{filename}'
            })
    return sheets


def get_github_config():
    with open('.github.json') as file:
        return json.loads(file.read())


def register_new_word_idea(word: str):
    try:
        config = get_github_config()
        repo = config['repo']
        token = config['token']
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        data = {
            "title": f"📘 [Anonymous:Word] Add word \"{word}\"",
            "body": f"Word \"{word}\" was searched on Remède but no definition was found so an anonymous user reported it !",
            "labels": config['labels'],
            "assignees": config['assignees']
        }
        response = requests.post(f"https://api.github.com/repos/{repo}/issues", headers=headers, json=data)
        return response.status_code == 201
    except:
        return False


def sanitize_query(q: str):
    return unidecode.unidecode(q.lower().replace('-', ' ').replace("'", " ")).strip()


@app.get('/')
def root():
    """
    ### Returns useful information about API and datasets
    - Its version
    - The available dictionaries
        - Their name (`name`)
        - Their unique identifier (hash) (`hash`)
        - Their slug; used to download or search in specific database (`slug`)
        - The number of words in the database (`total`)
        - Does the database respect the Remède JSON Schema (`valid`)
        - Which schema does it follow (`schema`)
        - Database readable size (`size`)
    """
    return {
        "version": version,
        "message": "Check /docs for documentation",
        "dictionaries": DICTIONARIES
    }


@app.get('/validity/{slug}')
def get_validity(slug: str):
    """
    Returns the dictionary `slug` validity (`true`/`false`). It's a check to know if it follows his JSON Schema. If state is unknown returns null.
    """
    return DICTIONARIES.get(slug, {"valid": {"message": "Slug not found"}})["valid"]


@app.get('/phoneme/{phoneme}')
def get_words_by_phoneme(phoneme: str, database: str = 'remede'):
    """
    Get th list of words with phoneme `phoneme`. It returns a list of tuples containing the word as the first element, and its document as the second element.
    """
    db = DATABASES.get(database, DATABASES['remede'])
    return fetch_words_with_phoneme(phoneme.replace('.', ''), db)


@app.get('/word/{word}')
def get_word_document(word: str, database: str = 'remede'):
    """
    Returns the Remède document of `word`.
    """
    db = DATABASES.get(database, DATABASES['remede'])
    document = fetch_remede_doc(word.replace("'", "''"), db)
    lock.release()
    json_doc = json.loads(document)
    if not json_doc:
        return False
    sources = []
    for source in json_doc['sources']:
        sources.append(SOURCES[source])
    json_doc['sources'] = sources
    return json_doc


@app.get('/random')
def get_random_word_document(database: str = 'remede'):
    """
    Returns a random word.
    """
    db = DATABASES.get(database, DATABASES['remede'])
    word = fetch_random_word(db)
    lock.release()
    return in_json(word)


@app.get('/word-of-day')
def get_word_of_day(database: str = 'remede'):
    """
    Returns the word of day.
    """
    db = DATABASES.get(database, DATABASES['remede'])
    identifier = database if database in DATABASES.keys() else 'remede'
    return in_json(fetch_remede_word_of_day(db, identifier))


@app.get('/autocomplete/{query}')
def get_autocomplete(query: str, database: str = 'remede'):
    """
    Returns the 6 first word starting by `query`. Not case and accent sensible !
    """
    db = DATABASES.get(database, DATABASES['remede'])
    safe_query = sanitize_query(query)
    results = fetch_autocomplete(safe_query, True, 0, db)
    lock.release()
    return in_json(results)


@app.get('/search/{query}')
def get_search_results(query: str, page: int = 0, database: str = 'remede'):
    """
    Returns the word starting with `query`. Not case and accent sensible !
    """
    db = DATABASES.get(database, DATABASES['remede'])
    safe_query = sanitize_query(query)
    results = fetch_autocomplete(safe_query, False, page, db)
    lock.release()
    return in_json(results)


@app.get('/ask-new-word/{query}')
def send_new_word(query: str):
    """
    Save the word `query` as a word to add to the dictionary.
    """
    success = register_new_word_idea(query)
    if success:
        return {
            "message": "Successfully added word to words to add."
        }
    return {
        "message": "Failed to add word to list..."
    }


@app.get('/sheets')
def get_cheatsheets():
    """
    Returns all grammar & orthography sheets.
    """
    return SHEETS


@app.get('/sheets/{slug}')
def get_cheatsheet_by_slug(slug: str):
    """
    Returns the grammar sheet / orthography with slug `slug`.
    """
    return SHEETS_BY_SLUG.get(slug, {
        "contenu": "",
        "description": "La fiche n'a pas été trouvée !",
        "nom": "Pas de fiche",
        "tags": [],
        "slug": "",
        "credits": ""
    })


@app.get('/sheets/download/{slug}')
def download_cheatsheet_by_slug(slug: str):
    """
    Returns the markdown file corresponding to sheet with slug `slug`.
    """
    fiche = SHEETS_BY_SLUG.get(slug, {
        "contenu": "",
        "description": "La fiche n'a pas été trouvée !",
        "nom": "Pas de fiche",
        "tags": [],
        "slug": "",
        "credits": "",
        "path": None
    })
    if fiche['path']:
        return FileResponse(fiche['path'], filename=f"{slug}.md")
    return HTTPException(status_code=404, detail='Fiche non trouvée !')


@app.get('/download')
def download_database(variant: str = 'remede'):
    """
    Download the Sqlite database as a file.
    """
    return FileResponse(f'data/{variant}.db')


@app.get('/release/{variant}')
def download_binary(variant: BinariesVariant):
    """
    Download the latest builds.
    """
    return FileResponse(f'builds/remede.{variant}', filename=f"remede.{variant}", media_type="multipart/form-data")


if __name__ == '__main__':
    print("Starting API | Opening databases... [1/3]")
    remede_database = sqlite3.connect('data/remede.db', check_same_thread=False)
    cursor = remede_database.cursor()
    remede_en_database = sqlite3.connect('data/remede.en.db', check_same_thread=False)
    cursor_en = remede_en_database.cursor()

    WORD_OF_DAY = {
        "date": "",
        "word.remede": "",
        "word.remede.en": ""
    }
    DATABASES = {
        "remede": cursor,
        "remede.en": cursor_en
    }

    del default_cursor

    print("\033[A\033[KStarting API | Calculating databases size... [2/3]")
    DICTIONARIES = {
        "remede": {
            "name": "Remède (FR)",
            "slug": "remede",
            "total": get_stats('data/remede.db'),
            "hash": md5(open('data/remede.db', 'rb').read()).hexdigest()[0:7],
            "valid": False,
            "schema": "",
            "size": f"{int(os.path.getsize('data/remede.db') * 10e-7)}Mb"
        },
        "remede.legacy": {
            "name": "Remède 1.2.3 (FR)",
            "slug": "remede.legacy",
            "total": get_stats('data/remede.legacy.db'),
            "hash": md5(open('data/remede.legacy.db', 'rb').read()).hexdigest()[0:7],
            "valid": False,
            "schema": "",
            "size": f"{int(os.path.getsize('data/remede.legacy.db') * 10e-7)}Mb"
        },
        "remede.en": {
            "name": "Remède (EN) Beta",
            "slug": "remede.en",
            "total": get_stats('data/remede.en.db'),
            "hash": md5(open('data/remede.en.db', 'rb').read()).hexdigest()[0:7],
            "valid": False,
            "schema": "",
            "size": f"{int(os.path.getsize('data/remede.en.db') * 10e-7)}Mb"
        }
    }

    print("\033[A\033[KStarting API | Checking JSON schemas validity... Can take a while... [3/3]")
    for slug, data in DICTIONARIES.items():
        validity = check_validity(slug)
        if data["hash"] != validity["hash"]:
            print(f"Validity check is outdated for database {slug}.")
            data["valid"] = None
            continue
        data["valid"] = validity["valid"]
        data["schema"] = validity["schema"]

    SHEETS = get_sheets()
    SHEETS_BY_SLUG = {f"{sheet['slug']}": sheet for sheet in SHEETS}

    print("\033[A\033[KStarting API | Done. [3/3]")
    uvicorn.run(app, host='0.0.0.0')
