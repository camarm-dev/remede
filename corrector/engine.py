from sqlite3 import Connection


class RemedeCorrectorEngine:

    def __init__(self, database: Connection, transform_letters: dict):
        self.db = database.cursor()
        self.aliases = transform_letters

    def __does_word_exist(self, word: str) -> bool:
        """
        Returns True if the words exists. Returns True if word startswith an uppercase letter.
        :param word: str
        :return: bool
        """
        self.db.execute("SELECT word FROM dictionary WHERE word = ?", (word,))
        row = self.db.fetchone()
        return row is not None

    def __find_other_word(self, word: str) -> list:
        """
        Find words that looks like :word
        :param word: str
        :return: list
        """
        self.db.execute("SELECT word FROM dictionary WHERE word LIKE ? + '%'", (word,))
        words = self.db.fetchall()
        print(words)
        return []

    def correct(self, text: str) -> list:
        """
        Correct :text:
        :param text: text to correct: str
        :return:
        """
        corrections = []

        tokenized_text = text.split(' ')
        for token in tokenized_text:
            word = token.replace(',', '').lower()
            if not self.__does_word_exist(word):
                corrections.append({
                    "startIndex": text.index(token),
                    "endIndex": 0,
                    "type": "orthographe",
                    "errorWord": word,
                    "suggestions": self.__find_other_word(word),
                    "message": "Ce mot n'a pas été trouvé dans la base Remède."
                })
        return corrections
