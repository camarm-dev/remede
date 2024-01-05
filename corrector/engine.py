
class RemedeCorrectorEngine:

    def __int__(self, remede_database: dict, transform_letters: dict):
        self.db = remede_database
        self.aliases = transform_letters

    def __does_word_exist(self, word: str) -> bool:
        """
        Returns True if the words exists
        :param word: str
        :return: bool
        """
        first_letter = word[0] if word[0] not in self.aliases.keys() else self.aliases[word[0]]
        return self.db[first_letter].get(word, False) != False

    def __find_other_word(self, word: str) -> list:
        """
        Find words that looks like :word
        :param word: str
        :return: list
        """
        return []

    def correct(self, text: str) -> dict:
        """
        Correct :text:
        :param text: text to correct: str
        :return:
        """
        corrections = []

        tokens = text.split(' ')
        for word in tokens:
            if not self.__does_word_exist(word):
                corrections.append({
                    "startIndex": text.index(word),
                    "endIndex": 0,
                    "type": "orthographe",
                    "errorWord": word,
                    "suggestions": self.__find_other_word(word)
                })
        return {

        }
