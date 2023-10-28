import json
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


def get_word_document(word: str):
    meaning = dictionary.meaning('fr', word)
    return {
        "synonymes": get_synonyms(word),
        "antonymes": get_antonyms(word),
        "definitions": [
            {
                "class": meaning[0][index],
                "definition": meaning[index + 1]
            }
            for index in range(len(meaning[0]))
        ],
        "ipa": get_ipa(word),
        "exemples": get_examples(word)
    }


def remedize(word_list: list):
    remede_dictionary = {}
    total = len(word_list)
    for word in word_list:
        inserted_word = get_word_document(word)
        remede_dictionary[word] = inserted_word
        print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}")
    return remede_dictionary


if __name__ == '__main__':
    print("Génération de la base Remède...\n")
    all_words = get_words()[0:100]
    all_ipa = get_word2ipa()
    dictionary = MultiDictionary()
    dictionary.set_words_lang('fr')
    try:
        remede = remedize(all_words)
        open('data/REMEDE.json', 'w+').write(json.dumps(remede))
    except KeyboardInterrupt:
        print("Annulation...")
