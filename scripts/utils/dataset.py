import json


def get_words():
    with open('data/mots.txt') as file:
        return file.read().split(',')


def get_saved_wordlist():
    with open('data/missing-wordlist.txt') as file:
        return file.read().split(',')


def get_custom_words():
    with open('data/custom_words.json') as file:
        return json.loads(file.read())


def get_word2ipa():
    with open('data/ipa.json') as file:
        return json.loads(file.read())
