import json


# Ce programme créé ipa.json et mots.txt à partir de IPA.txt

def get_ipas(lang: str):
    with open(f'data/{lang}/IPA.txt') as file:
        return file.read().split('\n')


def write_wordlist(data: list, lang: str):
    with open(f'data/{lang}/words.txt', 'w') as file:
        return file.write(';'.join(data))


def write_word2ipa(data: dict, lang: str):
    with open(f'data/{lang}/ipa.json', 'w') as file:
        return file.write(json.dumps(data))


def generate_wordlist(data_list: list):
    wordlist_ = []
    word2ipa_ = {}
    for raw in data_list:
        if raw == '':
            continue
        word, ipa = raw.split('\t')
        wordlist_.append(word)
        word2ipa_[word] = ipa
    return wordlist_, word2ipa_


if __name__ == '__main__':
    langs = ['fr']
    total_steps = len(langs) * 2
    for lang in langs:
        step = langs.index(lang) * 2
        print(f"Generating resources ({lang}) [{step}/{total_steps}]...")
        IPAs = get_ipas(lang)
        print(f"\033[A\033[KCreating resources ({lang}) [{step + 1}/{total_steps}]...")
        wordlist, word2ipa = generate_wordlist(IPAs)
        print(f"\033[A\033[KSaving resources ({lang}) [{step + 2}/{total_steps}]...")
        write_wordlist(wordlist, lang)
        write_word2ipa(word2ipa, lang)
        print(f"\033[A\033[KGenerating resources ({lang}) [{step + 2}/{total_steps}]... Done.")
