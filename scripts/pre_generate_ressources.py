import json


# Ce programme créé ipa.json et mots.txt à partir de IPA.txt

def get_ipas():
    with open('data/IPA.txt') as file:
        return file.read().split('\n')


def write_wordlist(data: list):
    with open('data/mots.txt', 'w') as file:
        return file.write(','.join(data))


def write_word2ipa(data: dict):
    with open('data/ipa.json', 'w') as file:
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
    print("Création des ressources [0/2]...")
    IPAs = get_ipas()
    print("\033[A\033[KCréation des ressources [1/2]...")
    wordlist, word2ipa = generate_wordlist(IPAs)
    print("\033[A\033[KSauvegarde des ressources [2/2]...")
    write_wordlist(wordlist)
    write_word2ipa(word2ipa)
    print("\033[A\033[KCréation des ressources [2/2]... Terminé.")
