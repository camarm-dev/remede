import unidecode

def sanitize_word(word: str):
    return unidecode.unidecode(word.lower().replace("-", " ").replace("'", " "))
