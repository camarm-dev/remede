import json


def get_words():
    with open('data/en/words.txt') as file:
        return file.read().split(';')


def get_saved_wordlist():
    with open('data/missing-wordlist-en.txt') as file:
        return file.read().split(';')


def save_progression_wordlist(save: list):
    with open('data/missing-wordlist-en.txt', 'w+') as file:
        file.write(';'.join(save))


def get_custom_words():
    with open('data/en/custom_words.json') as file:
        return json.loads(file.read())


def get_word2ipa():
    with open('data/en/ipa.json') as file:
        return json.loads(file.read())
