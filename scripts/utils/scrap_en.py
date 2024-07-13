from typing import Tuple

from bs4 import BeautifulSoup
import requests

from utils.scrap import count_syllables


headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0'
}


def get_word_metadata(word: str, _: str) -> Tuple[None, None, int, int, int, bool]:
    """
    Get the number of syllables, the elidable property and if the word end phoneme is feminine.
    :param word: string of word
    :param _: formally the phoneme og the word. this parameter is useless
    :return: Elidable, Feminine, Syllable count, Min syllables count, Max syllables count and Nature
    """
    syllables_count = count_syllables(word.lower())
    return None, None, syllables_count, syllables_count, syllables_count, False


def get_synonyms_and_antonyms(word: str):
    synonyms = []
    antonyms = []
    try:
        url = f'https://dictionary.cambridge.org/thesaurus/{word}'
        response = requests.get(url, headers=headers).content
        html = BeautifulSoup(response, 'html.parser')
        synonyms_elements = html.select('.pr.sense.dsense .ddef_block .hax .tlcs.lmt-10.lmb-20 .item.lc.lc1 .synonym')
        antonyms_elements = html.select('.pr.sense.dsense .ddef_block .hax .tlcs.lmt-10.lmb-20 .item.lc.lc1 .opposite')
        for el in synonyms_elements:
            synonyms.append(el.text)
        for el in antonyms_elements:
            antonyms.append(el.text)
    except:
        pass
    return synonyms, antonyms


def get_conjugations(verb: str):
    # TODO
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
                    sujet = element_sujet.text if element_sujet else modes_conjugation_subjects.get(f'{nom_mode}_{nom_temps}', '(Pas de sujet)')
                    forme_verbale = forme.text.replace(sujet + ' ', '')
                    verb_conjugaisons[nom_mode][nom_temps][sujet] = forme_verbale
        return verb_conjugaisons
    except Exception as e:
        return {}

