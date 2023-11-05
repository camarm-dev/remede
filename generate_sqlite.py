import datetime
import json
import sqlite3


# Ce programme créé à partir de la base Remède un fichier remede.db


def get_remede_json(letter: str):
    return json.loads(open(f'data/REMEDE_{letter}.json').read())


def insert_document(word_document: dict, word: str):
    cursor.execute("INSERT INTO dictionary VALUES (?,?)", (word, json.dumps(word_document)))


def browse_words(dictionary: dict, letter: str):
    words = list(dictionary.keys())
    for word in words:
        insert_document(dictionary[word], word)
        print(f"\033[A\033[KLettre {letter} | Mot insérés {words.index(word)}/{len(words)}")


def setup():
    cursor.execute("DROP TABLE IF EXISTS dictionary")
    cursor.execute("CREATE TABLE IF NOT EXISTS dictionary (word TEXT NOT NULL , document TEXT NOT NULL)")


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
        'j': get_remede_json('j')
    }

    before = datetime.datetime.now()

    database = sqlite3.connect('data/remede.db')
    cursor = database.cursor()

    print("Génération de la base sql...")
    setup()

    for remede_letter in REMEDE.keys():
        remede = REMEDE[remede_letter]
        browse_words(remede, remede_letter)

    post_setup()

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')