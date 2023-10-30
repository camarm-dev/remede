import datetime
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup


def get_words():
    with open('data/mots.txt') as file:
        return file.read().split(',')


def get_word2ipa():
    with open('data/ipa.json') as file:
        return json.loads(file.read())


def get_synonyms(word: str):
    if len(word) == 1:
        return []
    try:
        parser = BeautifulSoup(requests.get(f'http://www.synonymo.fr/synonyme/{word}').content, 'html.parser')
        results_list = parser.find('div', attrs={'class': 'fiche'})
        return [tag.text for tag in results_list.find_all('a', attrs={'class': 'word'})]
    except Exception:
        return []


def get_antonyms(word: str):
    if len(word) == 1:
        return []
    try:
        parser = BeautifulSoup(requests.get(f'http://www.antonyme.org/antonyme/{word}').content, 'html.parser')
        results_list = parser.find('div', attrs={'class': 'fiche'})
        return [tag.text for tag in results_list.find_all('a', attrs={'class': 'word'})]
    except Exception:
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
    return {
        "synonymes": get_synonyms(word),
        "antonymes": get_antonyms(word),
        "definitions": [
            {
                "genre": result['genre'][index],
                "classe": result['nature'][index],
                "explications": result['natureDef'][index][0],
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
        "ipa": get_ipa(word),
        "conjugaisons": {}
    }


def saveRemede(char: str, remede_dictionary):
    open(f'data/REMEDE_{char}.json', 'w+').write(json.dumps(remede_dictionary))


def remedize(word_list: list):
    remede_dictionary = {}
    total = len(word_list)
    errored = 0
    segments = 0
    accepted_char = {
        "a": ['â', 'à', 'æ'],
        'c': ['ç'],
        'i': ['î', 'ï'],
        'u': ['ù', 'û', 'ü'],
        "e": ['é', 'ê', 'è', 'ë']
    }
    current_char = 'a'
    for word in word_list:
        if not word.lower().startswith(current_char) and not any([word.lower().startswith(char) for char in accepted_char[current_char]]):
            saveRemede(current_char, remede_dictionary)
            del remede_dictionary
            remede_dictionary = {}
            current_char = word[0].lower()
            segments += 1
        inserted_word = get_word_document(word)
        if not inserted_word:
            errored += 1
        remede_dictionary[word] = inserted_word
        print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}: \"{word}\"{' ' * (22 - len(word))} | {errored} erreurs | {segments} segments sauvégardés")


def getTimeDetails(time):
    days, seconds = time.days, time.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


if __name__ == '__main__':
    print("Génération de la base Remède...\n")
    all_words = get_words()
    all_ipa = get_word2ipa()
    before = datetime.datetime.now()
    try:
        remedize(all_words)
    except KeyboardInterrupt:
        print("Annulation...")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
