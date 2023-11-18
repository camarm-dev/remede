import json
import random
from hashlib import md5

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

version = "1.0.0"
app = FastAPI(title='Remède', description='Un dictionnaire libre.', version=version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
transformLetter = {
    'â': 'a',
    'æ': 'a',
    'à': 'a',
    'ç': 'c',
    'î': 'i',
    'ï': 'i',
    'ù': 'u',
    'û': 'u',
    'ü': 'u',
    'é': 'e',
    'ë': 'e',
    'ê': 'e',
    'è': 'e',
    'ô': 'o',
    'ö': 'o',
    'œ': 'o'
}


def get_remede_json(letter: str):
    return json.loads(open(f'data/REMEDE_{letter}.json').read())


def get_first_letter(word: str):
    first_letter = word[0]
    if first_letter not in transformLetter.keys():
        return first_letter
    return transformLetter[first_letter]


def get_random_word():
    random_letter = random.choice(list(REMEDE.keys()))
    random_word = random.choice(list(REMEDE[random_letter].keys()))
    return random_word


def get_remede_doc(word: str):
    return REMEDE[get_first_letter(word)].get(word, {'message': 'Mot non trouvé'})


@app.get('/')
def root():
    """
    ### Renvoie des informations utiles à propos de l'API:
    - Sa version
    - L'identifiant du dataset API (`dataset`)
    - Le hash du dataset de la base Sqlite (`hash`)
    """
    return {
        "version": version,
        "message": "Check /docs for documentation",
        "dataset": DATASET,
        "hash": HASH
    }


@app.get('/word/{word}')
def get_word_document(word: str):
    """
    Renvoie le document Remède du mot `word`
    """
    return get_remede_doc(word)


@app.get('/random')
def get_random_word_document():
    """
    Renvoie un mot au hasard
    """
    return get_random_word()


@app.get('/autocomplete/{query}')
def get_autocomplete(query: str):
    """
    Renvoie les 6 premiers mots commençant par `query`
    """
    json_object = get_remede_json(get_first_letter(query))
    keys: list = json_object.keys()
    return list(filter(lambda word: word.startswith(query), keys))[0:6]


@app.get('/download')
def download_database():
    """
    Télécharge la base Sqlite sous form de fichier.
    """
    return FileResponse('data/remede.db')


if __name__ == '__main__':
    REMEDE = {
        'a': get_remede_json('a'),
        'b': get_remede_json('b'),
        'c': get_remede_json('c'),
        'd': get_remede_json('d'),
        'e': get_remede_json('e'),
        'f': get_remede_json('f'),
        'g': get_remede_json('g'),
        'h': get_remede_json('h'),
        'i': get_remede_json('i'),
        'j': get_remede_json('j'),
        'k': get_remede_json('k'),
        'l': get_remede_json('l'),
        'm': get_remede_json('m'),
        'n': get_remede_json('n'),
        'o': get_remede_json('o'),
        'p': get_remede_json('p'),
        'q': get_remede_json('q'),
        'r': get_remede_json('r'),
        's': get_remede_json('s'),
        't': get_remede_json('t'),
        'u': get_remede_json('u'),
        'v': get_remede_json('v'),
        'w': get_remede_json('w'),
        'x': get_remede_json('x'),
        'y': get_remede_json('y'),
        'z': get_remede_json('z')
    }
    DATASET = md5(open('data/remede.db','rb').read()).hexdigest()[0:7]
    HASH = str(md5(str(REMEDE).encode()).hexdigest())[0:7]
    uvicorn.run(app, host='0.0.0.0')
