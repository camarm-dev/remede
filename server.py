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

lock = threading.Lock()
version = "1.3.0"
app = FastAPI(title='Remède', description='Un dictionnaire libre.', version=version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


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


def fetch_random_word():
    lock.acquire(True)
    # TODO, change query to new "SELECT word FROM dictionary WHERE nature != 'VER' AND nature != '' ORDER BY RANDOM() LIMIT 1"
    return cursor.execute("SELECT word FROM dictionary ORDER BY RANDOM() LIMIT 1").fetchone()[0]


def fetch_words_with_phoneme(phoneme: str):
    lock.acquire(True)
    results = cursor.execute("SELECT document FROM dictionary WHERE phoneme = ?", (phoneme,)).fetchall()
    return list(map(lambda x: json.loads(x[0]), results))


def fetch_remede_word_of_day():
    global WORD_OF_DAY
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    if today != WORD_OF_DAY['date']:
        WORD_OF_DAY['date'] = today
        WORD_OF_DAY['word'] = fetch_random_word()
        lock.release()
    return WORD_OF_DAY['word']


def fetch_remede_doc(word: str):
    lock.acquire(True)
    response = cursor.execute("SELECT document FROM dictionary WHERE word = ?", (word,)).fetchone()
    return response[0] if response else json.dumps({'message': 'Mot non trouvé'})


def fetch_autocomplete(query: str, limit: bool = False, page: int = 0):
    lock.acquire(True)
    if limit:
        response = cursor.execute(
            "SELECT word FROM wordlist WHERE indexed LIKE ? + '%' ORDER BY word ASC LIMIT 5", (query,)).fetchall()
    else:
        response = cursor.execute(
            "SELECT word FROM wordlist WHERE indexed LIKE ? + '%' ORDER BY word ASC LIMIT 50 OFFSET ?", (query, page * 50)).fetchall()
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
    return unidecode.unidecode(q.lower().replace('-', ' ').replace("'", " "))


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
def get_words_by_phoneme(phoneme: str):
    """
    Returns a list of words with phoneme `phoneme`
    """
    return fetch_words_with_phoneme(phoneme)


@app.get('/word/{word}')
def get_word_document(word: str):
    """
    Returns the Remède document of `word`.
    """
    # document = fetch_remede_doc(word.replace("'", "''"))
    # lock.release()
    json_doc = {
        "synonyms": [
            "acupuncture",
            "électuaire",
            "émulsion",
            "antidote",
            "épithème",
            "bain",
            "baume",
            "biais",
            "bouillon",
            "calmant",
            "cataplasme",
            "cautère",
            "charme",
            "compresse",
            "confection",
            "contrepoison",
            "cure",
            "diète",
            "douche",
            "drogue",
            "emplâtre",
            "enveloppement",
            "expédient",
            "friction",
            "fumigation",
            "gargarisme",
            "grog",
            "implantation",
            "infusion",
            "inhalation",
            "injection",
            "instillation",
            "insufflation",
            "lavement",
            "médecine",
            "médicament",
            "médication",
            "manoeuvre",
            "mithridate",
            "moyen",
            "onguent",
            "orviétan",
            "palliatif",
            "panacée",
            "pansement",
            "parade",
            "perfusion",
            "piqûre",
            "placebo",
            "pommade",
            "ponction",
            "potion",
            "préparatif",
            "préparation",
            "préservatif",
            "purgation",
            "purge",
            "rééducation",
            "régime",
            "recette",
            "recours",
            "refuge",
            "relaxation",
            "ressource",
            "saignée",
            "sérum",
            "sinapisme",
            "solution",
            "soulagement",
            "spécialité",
            "spécifique",
            "suralimentation",
            "thérapeutique",
            "thériaque",
            "tisane",
            "topique",
            "traitement",
            "transfusion"
        ],
        "antonyms": [
            "embrocation",
            "expédient",
            "mal",
            "maladie"
        ],
        "etymologies": [
            "Du latin <i>remĕdium</i>."
        ],
        "definitions": [
            {
                "gender": "",
                "nature": "Nom propre",
                "explanations": [
                    "(Informatique) Dictionnaire libre multiplateforme qui a pour objectif de remplacer Antidote."
                ],
                "examples": [
                    {
                        "content": "Tu connais pas <b>Remède</b> ? C'est le meilleur dictionnaire mobile !",
                        "sources": "Un utilisateur de Remède, 2024"
                    },
                    {
                        "content": "<b>Remède</b> mérite une <i>star</i> sur Github !",
                        "sources": "Un utilisateur de Remède, 2024"
                    }
                ]
            },
            {
                "gender": "masculin",
                "nature": "Nom commun",
                "explanations": [
                    "(Médecine) Substance qui sert à guérir un mal ou une maladie. ",
                    "(Sens figuré) Ce qui sert à guérir les maladies de l’âme. ",
                    "(Sens figuré) Ce qui sert à prévenir, surmonter ou faire cesser un malheur, un inconvénient ou une disgrâce. ",
                    "(En particulier) Lavement. "
                ],
                "examples": [
                    {
                        "content": "<i>Le suc d'une certaine plante appelée par les Caraïbes </i>touloula<i>, et par les Français </i>herbes aux flèches<i>, est, dit-on, le seul <b>remède</b> contre les plaies faites par les flèches empoisonnées avec le suc de mancenilier.</i> ",
                        "sources": "(R. P. Jean-Baptiste Labat, <i>Voyages aux iles françaises de l'Amérique</i>, nouvelle édition d'après celle de 1722, Paris&#160;: chez Lefebvre &amp; chez A.-J. Ducollet, 1831, page 75)"
                    },
                    {
                        "content": "<i>Ce fut M. de Chalvet-Rochemonteix qui apprit aux paysans à se prémunir contre les ravages de la carie dans les grains par le sulfatage de la semence, dont les résultats furent souverains. Le mal cessa avec l’application de ce <b>remède</b>.</i> ",
                        "sources": "(Abbé Henri-Dominique Larrondo, <i>Monographie de la commune de Merville (Haute-Garonne)</i>, dans <i>Monographies de communes</i>, concours ouvert en 1897 par la Société des agriculteurs de France, Paris &amp; Lille&#160;: J. Lefort - A. Taffin-Lefort, successeur, 1898, page 96)"
                    },
                    {
                        "content": "<i>Et, s’il acceptait qu’on le soignât, il refusait rudement tout <b>remède</b>, dans le doute où il était tombé de la médecine.</i> ",
                        "sources": "(Émile Zola, <i>Le Docteur Pascal</i>, G. Charpentier, 1893, chapitre VI)"
                    }
                ]
            }
        ],
        "plurals": [
            {
                "label": "Masculin",
                "singular": "religieux  <phoneme>\\ʁə.li.ʒjø\\</phoneme>",
                "plural": "religieux  <phoneme>\\ʁə.li.ʒjø\\</phoneme>"
            },
            {
                "label": "Féminin",
                "singular": "<reference href=\"religieuse\">religieuse</reference>  <phoneme>\\ʁə.li.ʒjøz\\</phoneme>",
                "plural": "<reference href=\"religieuses\">religieuses</reference>  <phoneme>\\ʁə.li.ʒjøz\\</phoneme>"
            }
        ],
        "sources": [
            "fr_wik",
            "antonyme_org",
            "synonymo_fr"
        ],
        "phoneme": "/ʁəmɛd/",
        "pronunciation": {
            "audio": "https://upload.wikimedia.org/wikipedia/commons/2/27/Fr-rem%C3%A8de.ogg",
            "credits": "https://commons.wikimedia.org/w/index.php?curid=3043985"
        },
        "conjugations": {}
    }
    sources = []
    for source in json_doc['sources']:
        sources.append(SOURCES[source])
    json_doc['sources'] = sources
    return json_doc


@app.get('/random')
def get_random_word_document():
    """
    Returns a random word.
    """
    word = fetch_random_word()
    lock.release()
    return in_json(word)


@app.get('/word-of-day')
def get_word_of_day():
    """
    Returns the word of day.
    """
    return in_json(fetch_remede_word_of_day())


@app.get('/autocomplete/{query}')
def get_autocomplete(query: str):
    """
    Returns the 6 first word starting by `query`. Not case and accent sensible !
    """
    safe_query = sanitize_query(query)
    results = fetch_autocomplete(safe_query, True)
    lock.release()
    return in_json(results)


@app.get('/search/{query}')
def get_search_results(query: str, page: int = 0):
    """
    Returns the word starting with `query`. Not case and accent sensible !
    """
    safe_query = sanitize_query(query)
    results = fetch_autocomplete(safe_query, False, page)
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

    WORD_OF_DAY = {
        "date": "",
        "word": ""
    }
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
            "name": "Remède (EN)",
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
