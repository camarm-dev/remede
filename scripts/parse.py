import datetime
import json
import sys
import urllib.parse

import requests
from bs4 import BeautifulSoup

accepted_char = {
    "a": ['â', 'à', 'æ'],
    'c': ['ç'],
    'i': ['î', 'ï'],
    'u': ['ù', 'û', 'ü'],
    "e": ['é', 'ê', 'è', 'ë'],
    'o': ['ô', 'ö', 'œ']
}

reverse_accepted_char = {
    'â': 'a',
    'à': 'a',
    'æ': 'a',
    'ç': 'c',
    'î': 'i',
    'ï': 'i',
    'ù': 'u',
    'ü': 'u',
    'û': 'u',
    'é': 'e',
    'è': 'e',
    'ê': 'e',
    'ë': 'e',
    'ô': 'o',
    'ö': 'o',
    'œ': 'o'
}


def get_words():
    with open('data/mots.txt') as file:
        return file.read().split(',')


def get_custom_words():
    with open('data/custom_words.json') as file:
        return json.loads(file.read())


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


def get_wictionary_doc(word: str):
    response = requests.post('http://localhost:8089/app/api_wiki.php', data={'motWiki': urllib.parse.quote(word)})
    try:
        result = response.json()
        if result['error'] != '':
            return {}, False
        return result, True
    except Exception:
        return {}, False


def get_conjugaisons(verb: str):
    try:
        verb_conjugaisons = {}
        parser = BeautifulSoup(requests.get(f'http://conjuguons.fr/conjugaison/verbe/{verb}').content, 'html.parser')
        table = parser.find('div', attrs={'id': 'toustemps'})
        modes_conjugaison = table.find_all('div', attrs={'class': 'modeConjugue'})
        for mode in modes_conjugaison:
            nom_mode = ' '.join(mode.attrs.get('class')).replace('modeConjugue ', '')
            temps_conjugaison = mode.find_all('div', attrs={'class': 'temps'})
            if nom_mode == 'Infinitif':
                continue
            verb_conjugaisons[nom_mode] = {}
            for temps in temps_conjugaison:
                nom_temps = ' '.join(temps.attrs.get('class')).replace('temps ', '')
                formes_verbales = temps.find_all('li')
                verb_conjugaisons[nom_mode][nom_temps] = {}
                for forme in formes_verbales:
                    element_sujet = forme.find('span', attrs={'class': 'pronom'})
                    sujet = element_sujet.text if element_sujet else modes_conjugaison_sujets.get(f'{nom_mode}_{nom_temps}', '(Pas de sujet)')
                    forme_verbale = forme.text.replace(sujet + ' ', '')
                    verb_conjugaisons[nom_mode][nom_temps][sujet] = forme_verbale
        return verb_conjugaisons
    except Exception:
        return {}


def get_word_document(word: str, ipa: str = None):
    result, success = get_wictionary_doc(word)
    if not success:
        return False
    conjugaisons = {}
    if 'Verbe' in result['genre'] or 'Verbe 1' in result['genre']:
        conjugaisons = get_conjugaisons(word)
    return {
        "synonymes": get_synonyms(word),
        "antonymes": get_antonyms(word),
        "etymologies": result['etymologies'],
        "definitions": [
            {
                "genre": result['genre'][index],
                "classe": result['nature'][index],
                "explications": result['natureDef'][index][0],
                "exemples": result['natureDef'][index][1][:3] if len(result['natureDef'][index][1]) > 3 else result['natureDef'][index][1]
            }
            for index in range(len(result['nature']))
        ],
        "credits": {
            "name": "page Wiktionnaire",
            "url": result['direct_link']
        },
        "ipa": ipa if ipa else get_ipa(word),
        "conjugaisons": conjugaisons
    }


def safe_get_word_document(word: str):
    try:
        return get_word_document(word)
    except Exception as e:
        print(f'Pausing: errored with {e}. Enter to retry')
        input()
        return safe_get_word_document(word)


def saveRemede(char: str, remede_dictionary):
    open(f'data/REMEDE_{char}.json', 'w+').write(json.dumps(remede_dictionary))


def remedize(word_list: list):
    remede_dictionary = {}
    total = len(word_list)
    errored = 0
    segments = 0
    current_char = 'a'
    for word in word_list:
        if not any([word.lower().startswith(letter) for letter in letters]) and letters != []:
            continue
        if word in custom_words:
            remede_dictionary[word] = custom_words_json[word]
            continue
        if not word.lower().startswith(current_char) and not any([word.lower().startswith(char) for char in accepted_char.get(current_char, [current_char])]):
            if remede_dictionary == {}:
                current_char = reverse_accepted_char.get(word[0].lower(), word[0].lower())
                continue
            saveRemede(current_char, remede_dictionary)
            del remede_dictionary
            remede_dictionary = {}
            current_char = reverse_accepted_char.get(word[0].lower(), word[0].lower())
            segments += 1
        inserted_word = safe_get_word_document(word)
        if not inserted_word:
            errored += 1
        remede_dictionary[word] = inserted_word
        print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}: \"{word}\"{' ' * (22 - len(word))} | {errored} erreurs | {segments} segments sauvégardés")
    saveRemede(current_char, remede_dictionary)


def getTimeDetails(time_object):
    days, seconds = time_object.days, time_object.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


if __name__ == '__main__':
    letters = []
    if '--letters' in sys.argv:
        args = sys.argv[2].split(',')
        letters = []
        for accepted_letter in args:
            letters.append(accepted_letter)
            for special_char in accepted_char.get(accepted_letter, []):
                letters.append(special_char)

    print(f"Génération de la base Remède ({','.join(letters) if letters != [] else 'toutes lettres'})...\n")
    all_words = get_words()
    all_ipa = get_word2ipa()
    custom_words_json = get_custom_words()
    custom_words = custom_words_json.keys()
    before = datetime.datetime.now()
    modes_conjugaison_sujets = {
        "Participe_Présent": "(en)",
        "Participe_Passé": "(a / est)"
    }
    try:
        remedize(all_words)
    except KeyboardInterrupt:
        print("Annulation...")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
