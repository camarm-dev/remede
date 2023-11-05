import json
from hashlib import md5

import uvicorn
from fastapi import FastAPI

version = "1.0.0"
app = FastAPI(title='Remède', description='Un dictionnaire libre.', version=version)
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
    'è': 'e'
}


def get_remede_json(letter: str):
    return json.loads(open(f'data/REMEDE_{letter}.json').read())


def get_first_letter(word: str):
    first_letter = word[0]
    if first_letter not in transformLetter.keys():
        return first_letter
    return transformLetter[first_letter]


def get_remede_doc(word: str):
    return REMEDE[get_first_letter(word)].get(word, {'message': 'Mot non trouvé'})


@app.get('/')
def root():
    return {
        "version": version,
        "message": "Check /docs for documentation",
        "dataset": str(md5(str(REMEDE).encode()).hexdigest())[0:7]
    }


@app.get('/word/{word}')
def get_word_document(word: str):
    return get_remede_doc(word)


@app.get('/autocomplete/{query}')
def get_autocomplete(query: str):
    json_object = get_remede_json(get_first_letter(query))
    keys: list = json_object.keys()
    return list(filter(lambda word: word.startswith(query), keys))[0:6]


if __name__ == '__main__':
    REMEDE = {
        'a': get_remede_json('a'),
        'b': get_remede_json('b'),
        'c': get_remede_json('c'),
        'd': get_remede_json('d'),
        'e': get_remede_json('e'),
        'f': get_remede_json('f')
    }
    uvicorn.run(app, host='0.0.0.0')
