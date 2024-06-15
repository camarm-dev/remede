import datetime
import sys
from bs4 import BeautifulSoup
import requests


def get_phoneme(word: str):
    result = requests.get(f'https://fr.wiktionary.org/wiki/{word}').content
    bs = BeautifulSoup(result, 'html.parser')
    anchor = bs.find('a', attrs={'title': 'Annexe:Prononciation/français'})
    return anchor.text.replace('\\', '/')


def iterate():
    result = ""
    total = len(TO_CHECK)
    for word in TO_CHECK:
        print(f"\033[A\033[KMot {TO_CHECK.index(word)}/{total} | Mot \"{word}\"")
        if word in WORDLIST:
            continue
        try:
            phoneme = get_phoneme(word)
            result += f"{word}\t{phoneme}\n"
        except KeyboardInterrupt:
            print("Exiting")
            exit()
        except:
            continue
    with open('.words_to_add', 'w+') as file:
        file.write(result)


def getTimeDetails(time_object):
    days, seconds = time_object.days, time_object.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


if __name__ == '__main__':

    before = datetime.datetime.now()

    WORDLIST = open('data/mots.txt').read().split(",")

    try:
        TO_CHECK = open(sys.argv[1]).read().split("\n")
        print("Iterating wordlist...")
        iterate()
    except Exception as e:
        print(f"Échec. Assurez vous d'avoir bien fourni les arguments nécessaires. \"{e}\"")

    after = datetime.datetime.now()
    time = after - before
    hour, minute, second = getTimeDetails(time)
    print(f'Fini en {hour} heures {minute} minutes et {second} secondes.')
