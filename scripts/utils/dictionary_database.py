import json
from sqlite3 import Cursor, Connection


class RemedeDatabase:

    def __init__(self, database: Connection):
        self.database = database
        self.cursor: Cursor = database.cursor()

    def save(self):
        self.cursor.close()
        self.database.commit()
        self.database.close()

    def init_dictionary(self):
        self.cursor.execute("DROP TABLE IF EXISTS dictionary")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS dictionary (word TEXT NOT NULL, indexed TEXT NOT NULL, phoneme TEXT NOT NULL, nature TEXT NOT NULL, syllables INT NOT NULL, min_syllables INT NOT NULL, max_syllables INT NOT NULL, elidable BOOLEAN, feminine BOOLEAN, document TEXT NOT NULL)")
        self.cursor.execute("DROP TABLE IF EXISTS sources")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sources (identifier TEXT NOT NULL, label TEXT NOT NULL, url TEXT NOT NULL)")

    def add_source(self, source: dict):
        self.cursor.execute("INSERT INTO sources VALUES (?,?,?)", (source['identifier'], source['label'], source['url']))
    def insert(self, word: str, sanitized_word: str, phoneme: str, nature: str, syllables: int, min_syllables: int, max_syllables: int, elidable: bool, feminine: bool, document: dict):
        self.cursor.execute("INSERT INTO dictionary VALUES (?,?,?,?,?,?,?,?,?,?)", (word, sanitized_word, phoneme, nature, syllables, min_syllables, max_syllables, elidable, feminine, json.dumps(document)))
