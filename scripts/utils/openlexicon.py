import sqlite3

database = sqlite3.connect('../../data/drime.db')
openlexicon = database.cursor()


class WordStats:
    nature: str
    min_syllables: int
    max_syllables: int
    elidable: bool
    feminine: bool

    def __init__(self, nature, min_syllables, max_syllables, elidable, feminine):
        self.nature = ','.join([string.split('|')[0] for string in nature.split(',')]) # Transform "NOM|manger,VER|manger" into "NOM,VER"
        self.min_syllables = min_syllables
        self.max_syllables = max_syllables
        self.elidable = elidable == 1
        self.feminine = feminine == 1


def get_word_stats(word: str):
    result = openlexicon.execute("SELECT orgi,min_nsyl,max_nsyl,elidable,feminine FROM words WHERE word = (?)", [word]).fetchone()
    if result:
        return WordStats(*result)
    return False

