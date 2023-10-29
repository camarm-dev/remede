import json
import urllib.parse

import requests
from PyMultiDictionary import MultiDictionary
from pprint import pprint


def get_words():
    with open('data/mots.txt') as file:
        return file.read().split(',')


def get_word2ipa():
    with open('data/ipa.json') as file:
        return json.loads(file.read())


def get_synonyms(word: str):
    return []


def get_antonyms(word: str):
    return []


def get_ipa(word: str):
    return all_ipa.get(word, '')


def get_examples(word: str):
    # {
    #     "contenu": "",
    #     "credits": ""
    # }
    return []


def get_wictionary_doc(word: str):
    response = requests.post('https://api-definition.fgainza.fr/app/api_wiki.php', data={'motWiki': urllib.parse.quote(word)})
    try:
        result = response.json()
        if result['error'] != '':
            return {}, False
        return result, True
    except Exception:
        return {}, False


def get_word_document(word: str):
    result, success = get_wictionary_doc(word)
    if not success:
        return False
    meaning = dictionary.meaning('fr', word)
    return {
        "synonymes": get_synonyms(word),
        "antonymes": get_antonyms(word),
        "definitions": [
            {
                "genre": result['genre'][index],
                "classe": result['nature'][index],
                "definitions": result['natureDef'][index][0],
                "exemples": [

                ]
            }
            for index in range(len(result['nature']))
        ],
        "credits": {
            "name": "page Wiktionnaire",
            "url": result['direct_link']
        },
        "image": {
            "url": result["url_img"],
            "credits": result["url_credits"]
        },
        "ipa": get_ipa(word)
    }


def remedize(word_list: list):
    remede_dictionary = {}
    total = len(word_list)
    errored = 0
    for word in word_list:
        inserted_word = get_word_document(word)
        if not inserted_word:
            errored += 1
        remede_dictionary[word] = inserted_word
        print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}: \"{word}\"{' ' * (22 - len(word))} | {errored} erreurs")
    return remede_dictionary


if __name__ == '__main__':
    print("Génération de la base Remède...\n")
    all_words = get_words()[0:1000]
    all_ipa = get_word2ipa()
    dictionary = MultiDictionary()
    dictionary.set_words_lang('fr')
    try:
        remede = remedize(all_words)
        open('data/REMEDE.json', 'w+').write(json.dumps(remede))
    except KeyboardInterrupt:
        print("Annulation...")
