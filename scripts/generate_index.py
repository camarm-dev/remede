import datetime
import sqlite3

import unidecode


def insert(word: str, indexed: str):
    cursor.execute("INSERT INTO wordlist VALUES (?,?)", (word, indexed))


def create_index():
    rows = cursor.execute("SELECT word FROM dictionary").fetchall()
    total = len(rows)
    for row in rows:
        word = row[0]
        safe_word = unidecode.unidecode((word.lower()))
        insert(word, safe_word)
        print(f"\033[A\033[KLigne {rows.index(row)}/{total} | Mot \"{word}\"")


def setup():
    cursor.execute("DROP TABLE IF EXISTS wordlist")
    cursor.execute("CREATE TABLE IF NOT EXISTS wordlist (word TEXT NOT NULL, indexed TEXT NOT NULL)")


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

    before = datetime.datetime.now()

    database = sqlite3.connect('data/remede.db')
    cursor = database.cursor()

    print("Création de l'index de recherche...")
    setup()

    create_index()

    post_setup()

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
