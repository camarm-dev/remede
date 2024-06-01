# Generate a weighted rime graph
import datetime
import sqlite3

import requests
from bs4 import BeautifulSoup


# The database is built as following:

# Node 1, Node 2, Weight (number of syllables, from 1 to 3)
# manger, parler, 1
# manger, ranger, 2

def execute(command: str):
    try:
        cursor.execute(command)
        return True
    except:
        return False


def insert_rimes(commands: list):
    total = len(commands)
    errored = 0
    for command in commands:
        row = commands.index(command)
        command = command.replace('INSERT INTO words', 'INSERT INTO rimes')
        success = execute(command)
        if not success:
            errored += 1
        print(f"\033[A\033[KLigne n°{row + 1}/{total} | {errored} erreurs")


def setup():
    cursor.execute("DROP TABLE IF EXISTS rimes")
    cursor.execute("CREATE TABLE IF NOT EXISTS rimes (word TEXT NOT NULL , phon TEXT NOT NULL, orgi TEXT NOT NULL, freq FLOAT NOT NULL, min_nsyl INT NOT NULL, max_nsyl INT NOT NULL, word_end TEXT NOT NULL, phon_end TEXT NOT NULL, elidable BOOLEAN NOT NULL, feminine BOOLEAN NOT NULL)")


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

    with open('rimes/drime.sql', 'r') as drime_database:
        sql_queries = drime_database.read().split('\n')
    database = sqlite3.connect('data/remede.db')
    cursor = database.cursor()

    print('Génération de la base de rimes...\n')
    setup()
    try:
        insert_rimes(sql_queries)
    except Exception as e:
        print(f"Exiting... {e}")
        post_setup()
        exit()
    post_setup()

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
