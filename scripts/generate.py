import datetime
import sqlite3
import sys
import urllib.parse
import requests

from scripts.utils.dataset import get_words, get_word2ipa, get_custom_words
from scripts.utils.dictionary_database import RemedeDatabase
from scripts.utils.sanitize import sanitize_word
from scripts.utils.scrap import get_conjugaisons, get_synonyms, get_antonyms, get_word_metadata

modes_conjugation_subjects = {
    "Participe_Présent": "(en)",
    "Participe_Passé": "(a / est)"
}


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


def get_word_document(word: str, ipa: str):
    result, success = get_wictionary_doc(word)
    if not success:
        return False

    conjugations = {}
    if 'Verbe' in result['genre']:
        conjugations = get_conjugaisons(word)

    synonyms = get_synonyms(word)
    antonyms = get_antonyms(word)

    sources = ["fr_wik"]
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
                "genre": result['genre'][index] if result['genre'][index] != result['nature'][index] else '',
                "classe": result['nature'][index],
                "explanations": result['natureDef'][index][0],
                "examples": result['natureDef'][index][1][:3] if len(result['natureDef'][index][1]) > 3 else result['natureDef'][index][1],
                "plurals": []
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
    for word in word_list:
        if word in custom_words:
            document = custom_words_json[word]
            ipa = document["phoneme"]
        else:
            ipa = get_ipa(word)
            document = safe_get_word_document(word, ipa)
        if not document:
            errored += 1
        # TODO nature
        elidable, feminine, syllables, min_syllables, max_syllables = get_word_metadata(word, ipa)
        database.insert(word, sanitize_word(word), ipa, "", syllables, min_syllables, max_syllables, elidable, feminine, document)
        print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}: \"{word}\"{' ' * (22 - len(word))} | {errored} erreurs")


def getTimeDetails(time_object):
    days, seconds = time_object.days, time_object.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


if __name__ == '__main__':

    # Resume option
    letters = []
    if '--resume' in sys.argv:
        pass
    print(f"Generating Remède database...\n")

    # Wordlist
    all_words = get_words()
    # IPA.json
    all_ipa = get_word2ipa()
    # custom_words.json
    custom_words_json = get_custom_words()
    custom_words = custom_words_json.keys()
    before = datetime.datetime.now()

    database = RemedeDatabase(sqlite3.connect('data/remede.db'))

    try:
        remedize(all_words)
    except KeyboardInterrupt:
        print("Saving and exit...")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Ends in {hour} hours {minute} minutes and {second} seconds.')
