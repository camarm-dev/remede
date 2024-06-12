import datetime
import json
import runpy
import sqlite3
import sys

from generate_sqlite import get_remede_json
from generate_index import sanitize_word
from parse import get_word_document, reverse_accepted_char, saveRemede


def insert_document(word_document: dict, word: str):
    cursor.execute("INSERT INTO dictionary VALUES (?,?)", (word, json.dumps(word_document)))


def add_to_wordlist(word: str, phoneme: str):
    with open('data/IPA.txt', 'r') as file:
        content = file.read()
    with open('data/IPA.txt', 'w') as file:
        insert = f"{word}\t{phoneme}"
        if insert in content:
            print(f"Word \"{word}\" was found in the database. Skipping.")
            return False
        words = content.split('\n')
        words.append(insert)
        words.sort(key=lambda val: sanitize_word(val))
        new_content = "\n".join(words)
        new_content = new_content.replace("\n", "", 1)
        file.write(new_content)
    return True


def add_to_json(word: str, document: dict):
    letter = reverse_accepted_char.get(word[0], word[0])
    REMEDE[letter][word] = document
    saveRemede(letter, REMEDE[letter])


def post_setup():
    cursor.close()
    database.commit()
    database.close()


def getTimeDetails(time_object):
    days, seconds = time_object.days, time_object.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


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

    before = datetime.datetime.now()

    database = sqlite3.connect('data/remede.db')
    cursor = database.cursor()

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
        for element in words_to_add:
            word, phoneme = element

            if not phoneme.startswith("/"):
                print(f"Phoneme must be formated like \"/ʁəmɛd/\", skipping {word}.")
                continue

            print(f"Ajout du mot \"{word}\"...")

            print("- Ajout dans la liste de mots...")
            exists = add_to_wordlist(word, phoneme)
            if exists:
                continue
            print("Fait.")

            print("- Construction du document Remède...")
            document = get_word_document(word, phoneme)
            print("Fait.")

            print("- Ajout du document aux bases JSON")
            add_to_json(word, document)
            print("Fait.")

            print("- Ajout du document à la base Sqlite")
            insert_document(document, word)
            print("Fait.")

            print("- Mise à jour de l'index...")
            cursor.execute("INSERT INTO wordlist VALUES (?,?)", (word, sanitize_word(word)))
            print("Fait.")

        post_setup()

        print("- Génération des ressources...")
        runpy.run_module('pre_generate_ressources', run_name='__main__')
        print("Fait.")

    except Exception as e:
        print(f"Échec. Assurez vous d'avoir bien fourni les arguments nécessaires. \"{e}\"")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
