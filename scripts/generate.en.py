import datetime
import sqlite3
import sys
import urllib.parse
import requests

from utils.dataset_en import get_words, get_word2ipa, get_saved_wordlist, \
    save_progression_wordlist
from utils.dataset import get_custom_words
from utils.dictionary_database import RemedeDatabase
from utils.sanitize import sanitize_word
from utils.scrap import get_conjugaisons, get_word_metadata
from generate import parse_examples

natures_keywords = {
    "Letter": "LETTRE",
    "Verb": "VER",
    "Noun": "NOM",
    "Adjective": "ADJ",
    "Adverb": "ADV",
    "Preposition": "PRO",
    "Conjunction": "CON",
    "Pronoun": "PRO",
    "Interjection": "INT"
}


def get_word_natures(document: dict):
    natures = []
    for definition in document.get('definitions', []):
        if definition['nature'] != '':
            nature = definition.get('nature', '').split(' ')[0]  # "Nom commun 1" will be Nom
            if nature in natures_keywords.keys():
                natures.append(natures_keywords[nature])
    return ','.join(natures)


def get_ipa(word: str):
    return all_ipa.get(word, '')


def get_wictionary_doc(word: str):
    response = requests.post('http://localhost:8089/app/api_wiki_en.php', data={'motWiki': urllib.parse.quote(word)})
    try:
        result = response.json()
        if result['error'] != '':
            return {}, False
        return result, True
    except Exception:
        return {}, False


def get_synonyms_antonyms(word: str):
    # TODO
    return [], []


def get_word_document(word: str, ipa: str):
    result, success = get_wictionary_doc(word)
    if not success:
        return False

    conjugations = {}
    if 'Verbe' in result['nature'] or 'Verbe 1' in result['nature']:
        conjugations = get_conjugaisons(word)

    synonyms, antonyms = get_synonyms_antonyms(word)

    sources = ["en_wik"]
    if len(synonyms) > 0:
        sources.append("synonymo_fr")
    if len(antonyms) > 0:
        sources.append("antonyme_org")
    if conjugations != {}:
        sources.append("conjuguons_fr")

    return {
        "synonyms": synonyms,
        "antonyms": antonyms,
        "etymologies": result['etymologies'],
        "definitions": [
            {
                "gender": result['genre'][index] if result['genre'][index] != result['nature'][index] else '',
                "nature": result['nature'][index],
                "explanations": list(result['natureDef'][index][0].values()) if type(result['natureDef'][index][0]) is dict else [],
                "examples": parse_examples(result['natureDef'][index][1][:3] if len(result['natureDef'][index][1]) > 3 else result['natureDef'][index][1]),
                "plurals": result['plurals']
            }
            for index in range(len(result['nature']))
        ],
        "sources": sources,
        "phoneme": ipa,
        "conjugations": conjugations
    }


def safe_get_word_document(word: str, ipa: str):
    try:
        return get_word_document(word, ipa)
    except Exception as e:
        print(f'Pausing: errored with {e}. Enter to retry')
        input()
        return safe_get_word_document(word, ipa)


def remedize(word_list: list):
    total = len(word_list)
    errored = 0
    try:
        for word in word_list:
            if word in custom_words:
                document = custom_words_json[word]
                ipa = document["phoneme"]
            else:
                ipa = get_ipa(word)
                document = safe_get_word_document(word, ipa)
            if not document:
                errored += 1
            elidable, feminine, syllables, min_syllables, max_syllables, nature = get_word_metadata(word, ipa)
            # No Openlexicon data, need to find by ourselves
            if not nature and document:
                nature = get_word_natures(document)
            # Multiple pronunciations, phoneme will be set as the first phoneme, while "phoneme" field will contains both
            if ',' in ipa:
                ipa = ipa.split(',')[0]
            database.insert(word, sanitize_word(word), ipa.replace('/', ''), nature, syllables, min_syllables, max_syllables, elidable, feminine, document)
            print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}: \"{word}\"{' ' * (35 - len(word))} | {errored} erreurs")
    except Exception as e:
        print(f"Program raised error {e}. Saving progression...")
        save = word_list[word_list.index(word):]
        save_progression_wordlist(save)
        raise KeyboardInterrupt



def getTimeDetails(time_object):
    days, seconds = time_object.days, time_object.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


if __name__ == '__main__':
    print(f"Generating Remède database...\n")
    # Wordlist
    all_words = get_words()
    # IPA.json
    all_ipa = get_word2ipa()
    # custom_words.json
    custom_words_json = get_custom_words()
    custom_words = custom_words_json.keys()
    before = datetime.datetime.now()

    # Resume option: replace wordlist
    if '--resume' in sys.argv:
        all_words = get_saved_wordlist()
        print(f"Resumed at word {all_words[0]}. Continuing generation...\n")

    database = RemedeDatabase(sqlite3.connect('data/remede.en.db'))
    database.init_dictionary()

    try:
        remedize(all_words)
    except KeyboardInterrupt:
        print("Received exit signal.")

    database.save()
    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Ends in {hour} hours {minute} minutes and {second} seconds.')