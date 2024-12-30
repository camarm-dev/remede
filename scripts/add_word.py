import datetime
import runpy
import sqlite3
import sys

from generate import safe_get_word_document, get_word_natures
from utils.scrap import get_word_metadata
from utils.dataset import get_words, get_custom_words, get_word2ipa
from utils.dictionary_database import RemedeDatabase
from utils.sanitize import sanitize_word


def add_to_wordlist(wordlist: list):
    with open('data/fr/IPA.txt', 'r') as file:
        content = file.read()
        words = content.split('\n')
    with open('data/fr/IPA.txt', 'w') as file:
        for element in wordlist:
            word, phoneme = element
            insert = f"{word}\t{phoneme}"
            if insert in content:
                print(f"Word \"{word}\" was found in the database. Skipping.")
                continue
            words.append(insert)
        words.sort(key=lambda val: sanitize_word(val))
        new_content = "\n".join(words)
        new_content = new_content.replace("\n", "", 1)
        file.write(new_content)


def getTimeDetails(time_object):
    days, seconds = time_object.days, time_object.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


def get_ipa(word: str):
    return all_ipa.get(word, '')


def add_to_database(word: str):
    if word in custom_words:
        document = custom_words_json[word]
        ipa = document["phoneme"]
    else:
        ipa = get_ipa(word)
        document = safe_get_word_document(word, ipa)
    elidable, feminine, syllables, min_syllables, max_syllables, nature = get_word_metadata(word, ipa)
    if not nature:
        nature = get_word_natures(document)
    database.insert(word, sanitize_word(word), ipa, nature, syllables, min_syllables, max_syllables, elidable, feminine, document)


if __name__ == '__main__':
    before = datetime.datetime.now()

    database = RemedeDatabase(sqlite3.connect('data/remede.db'))

    _, arg1, arg2 = sys.argv

    words_to_add = []

    if arg1 == '-f':
        with open(arg2, 'r') as file:
            for line in file.readlines():
                if line != '':
                    try:
                        word, phoneme = line.split("\t")
                    except:
                        print(line)
                    words_to_add.append((word, phoneme))
    else:
        words_to_add.append((arg1, arg2))
    try:
        print("- Ajout des mots à la liste de mots...")
        add_to_wordlist(words_to_add)
        print("Fait.")
        print("- Génération des ressources...")
        runpy.run_module('pre_generate_ressources', run_name='__main__')
        print("Fait.")

        # Wordlist
        all_words = get_words()
        # IPA.json
        all_ipa = get_word2ipa()
        # custom_words.json
        custom_words_json = get_custom_words()
        custom_words = custom_words_json.keys()

        for element in words_to_add:
            word, phoneme = element

            if not phoneme.startswith("/"):
                print(f"Phoneme must be formated like \"/ʁəmɛd/\", skipping {word}.")
                continue

            add_to_database(word)

        print("- Sauvegarde de la base de données...")
        database.save()
        print("Fait.")

    except Exception as e:
        raise e
        # print(f"Échec. Assurez vous d'avoir bien fourni les arguments nécessaires. \"{e}\"")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
