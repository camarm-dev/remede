import datetime
import runpy
import sqlite3
import sys

from utils.dictionary_database import RemedeDatabase
from utils.sanitize import sanitize_word


def add_to_wordlist(wordlist: list):
    with open('data/IPA.txt', 'r') as file:
        content = file.read()
        words = content.split('\n')
    with open('data/IPA.txt', 'w') as file:
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
        for element in words_to_add:
            word, phoneme = element

            if not phoneme.startswith("/"):
                print(f"Phoneme must be formated like \"/ʁəmɛd/\", skipping {word}.")
                continue

            print(f"Ajout du mot \"{word}\"...")

            print("- Construction du document Remède...")
            document = get_word_document(word, phoneme)
            print("Fait.")

            print("- Insertion du document Remède...")
            database.insert(word, phoneme)
            print("Fait.")

        print("- Sauvegarde de la base de données...")
        database.save()
        print("Fait.")
        print("- Génération des ressources...")
        runpy.run_module('pre_generate_ressources', run_name='__main__')
        print("Fait.")

    except Exception as e:
        print(f"Échec. Assurez vous d'avoir bien fourni les arguments nécessaires. \"{e}\"")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
