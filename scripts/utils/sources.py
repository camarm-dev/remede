SOURCES = {
    "antonyme_org": {
        "identifier": "antonyme_org",
        "label": "definition.antonyms",
        "url": "http://www.antonyme.org/antonyme/{word}"
    },
    "synonymo_fr": {
        "identifier": "synonymo_fr",
        "label": "definition.synonyms",
        "url": "http://synonymo.fr/synonyme/{word}"
    },
    "conjuguons_fr": {
        "identifier": "conjuguons_fr",
        "label": "definition.conjugation",
        "url": "http://conjuguons.fr/conjugaison/verbe/{word}"
    },
    "fr_wik": {
        "identifier": "fr_wik",
        "label": "Wiktionnaire",
        "url": "https://fr.wiktionary.org/wiki/{word}"
    },
    "en_wik": {
        "identifier": "en_wik",
        "label": "Wiktionary",
        "url": "https://en.wiktionary.org/wiki/{word}"
    },
    "thesaurus_com": {
        "identifier": "thesaurus_com",
        "label": "definition.synonyms_and_antonyms",
        "url": "https://www.thesaurus.com/browse/{word}"
    },
    "mlconjug3": {
        "identifier": "mlconjug3",
        "label": "definition.conjugation",
        "url": "https://github.com/Ars-Linguistica/mlconjug3"
    }
}

FRENCH_SOURCES = ["antonyme_org", "synonymo_fr", "conjuguons_fr", "fr_wik"]
ENGLISH_SOURCES = ["thesaurus_com", "en_wik", "mlconjug3"]
