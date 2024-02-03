# Generate a weighted rime graph
import datetime
import sqlite3

import requests
from bs4 import BeautifulSoup


# The database is built as following:

# Node 1, Node 2, Weight (number of syllables, from 1 to 3)
# manger, parler, 1
# manger, ranger, 2

def get_words():
    with open('data/mots.txt') as file:
        return file.read().split(',')


def get_page(word: str):
    url = f"https://www.dicodesrimes.com/rime/{word}"
    return requests.get(url).content


def get_document(word: str):
    page = BeautifulSoup(get_page(word), 'html.parser')

    high_rhymes = page.find('div', attrs={'class': 'panel-danger'}).find_all('a', attrs={'class': 'resultitem'})
    medium_rhymes = page.find('div', attrs={'class': 'panel-success'}).find_all('a', attrs={'class': 'resultitem'})
    low_rhymes = page.find('div', attrs={'class': 'panel-info'}).find_all('a', attrs={'class': 'resultitem'})

    rhymes_list = []

    for rhyme in high_rhymes:
        rhymes_list.append((word, rhyme.text, 3))

    for rhyme in medium_rhymes:
        rhymes_list.append((word, rhyme.text, 2))

    for rhyme in low_rhymes:
        rhymes_list.append((word, rhyme.text, 1))

    if len(rhymes_list) == 0:
        raise NameError('Word not found')

    return rhymes_list


def safe_get_document(word: str):
    try:
        return get_document(word), True
    except KeyboardInterrupt:
        print("Exiting...")
        post_setup()
        exit()
    except:
        return [], False


def iterate_words(word_list: list):
    total = len(word_list)
    errored = 0
    for word in word_list:
        result, success = safe_get_document(word)
        if success:
            for row in result:
                word1, word2, _ = row
                existing = cursor.execute('SELECT * FROM dictionary WHERE word2 = ? AND word1 = ?', (word2, word1)).fetchall()
                if len(existing) > 0:
                    continue
                cursor.execute("INSERT INTO dictionary VALUES (?,?,?)", row)
        else:
            errored += 1
        print(f"\033[A\033[KMot n°{word_list.index(word) + 1}/{total}: \"{word}\"{' ' * (22 - len(word))} | {errored} erreurs")


def setup():
    cursor.execute("DROP TABLE IF EXISTS dictionary")
    cursor.execute("CREATE TABLE IF NOT EXISTS dictionary (word1 TEXT NOT NULL , word2 TEXT NOT NULL, type INT NOT NULL)")


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

    words = get_words()
    database = sqlite3.connect('data/rimes.db')
    cursor = database.cursor()

    print('Génération de la base de rimes...')
    setup()
    iterate_words(words)
    post_setup()

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
