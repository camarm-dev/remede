from bs4 import BeautifulSoup
import requests


def count_syllables(word: str):
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
            if word.endswith("e"):
                count -= 1
    if count == 0:
        count += 1
    return count


def get_word_stats(word: str, phoneme: str):
    """
    Get the number of syllables, the elidable property and if the word end phoneme is feminine.
    :param word: string of word
    :param phoneme: phoneme of word
    :return: Elidable, Feminine, Syllable count
    """
    return False, phoneme[-1] == 'e', count_syllables(word.lower())


def get_synonyms(word: str):
    if len(word) == 1:
        return []
    try:
        parser = BeautifulSoup(requests.get(f'http://www.synonymo.fr/synonyme/{word}').content, 'html.parser')
        results_list = parser.find('div', attrs={'class': 'fiche'})
        return [tag.text for tag in results_list.find_all('a', attrs={'class': 'word'})]
    except Exception:
        return []


def get_antonyms(word: str):
    if len(word) == 1:
        return []
    try:
        parser = BeautifulSoup(requests.get(f'http://www.antonyme.org/antonyme/{word}').content, 'html.parser')
        results_list = parser.find('div', attrs={'class': 'fiche'})
        return [tag.text for tag in results_list.find_all('a', attrs={'class': 'word'})]
    except Exception:
        return []


def get_conjugaisons(verb: str):
    try:
        verb_conjugaisons = {}
        parser = BeautifulSoup(requests.get(f'http://conjuguons.fr/conjugaison/verbe/{verb}').content, 'html.parser')
        table = parser.find('div', attrs={'id': 'toustemps'})
        modes_conjugaison = table.find_all('div', attrs={'class': 'modeConjugue'})
        for mode in modes_conjugaison:
            nom_mode = ' '.join(mode.attrs.get('class')).replace('modeConjugue ', '')
            temps_conjugaison = mode.find_all('div', attrs={'class': 'temps'})
            if nom_mode == 'Infinitif':
                continue
            verb_conjugaisons[nom_mode] = {}
            for temps in temps_conjugaison:
                nom_temps = ' '.join(temps.attrs.get('class')).replace('temps ', '')
                formes_verbales = temps.find_all('li')
                verb_conjugaisons[nom_mode][nom_temps] = {}
                for forme in formes_verbales:
                    element_sujet = forme.find('span', attrs={'class': 'pronom'})
                    sujet = element_sujet.text if element_sujet else modes_conjugaison_sujets.get(f'{nom_mode}_{nom_temps}', '(Pas de sujet)')
                    forme_verbale = forme.text.replace(sujet + ' ', '')
                    verb_conjugaisons[nom_mode][nom_temps][sujet] = forme_verbale
        return verb_conjugaisons
    except Exception:
        return {}

