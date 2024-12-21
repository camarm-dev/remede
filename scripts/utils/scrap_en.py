from typing import Tuple

from bs4 import BeautifulSoup
import requests
from mlconjug3 import Conjugator
from utils.scrap import count_syllables

conjugator = Conjugator('en')
headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0'
}


def get_word_metadata(word: str, _: str) -> Tuple[None, None, int, int, int, bool]:
    """
    Get the number of syllables, the elidable property and if the word end phoneme is feminine.
    :param word: string of word
    :param _: formally the phoneme of the word. this parameter is useless
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
    conjugations = {}
    data = conjugator.conjugate([verb], 'pronoun')
    if data:
        for verb in data:
            for mood_name, mood in verb.full_forms.items():
                conjugations[mood_name.title()] = {}
                for tense_name, tense in mood.items():
                    conjugations[mood_name.title()][tense_name.title()] = {}
                    if type(tense) == str:
                        conjugations[mood_name.title()][tense_name.title()]["(No subject)"] = tense
                    else:
                        for subject, form in tense.items():
                            conjugations[mood_name.title()][tense_name.title()][subject.title()] = form
    return conjugations
