import json
import os
import sqlite3
import re

LICENSE = ""


def delete_tags(string: str, tags: list):
    for tag in tags:
        string = string.replace(f'<{tag}>', '').replace(f'</{tag}>', '')
    return string

def sanitize(definition: str, total: list):
    index = total.index(definition)
    if type(definition) == list:
        if type(definition[0]) == list:
            definition = definition[0]
        definition = "\n\t".join(definition)
    sanitized = delete_tags(definition, ['b', 'abbr']).replace('<a', '<A').replace('/a>', '/A>').replace('<reference', '<A').replace('/reference>', '/A>')
    return f"\n\t{index + 1}. {sanitized}"


if __name__ == '__main__':
    databases = list(filter(lambda x: x.endswith('.db') and "remede" in x and "legacy" not in x, os.listdir('data')))
    print("\n")
    for file in databases:
        print(f"\033[A\033[KGenerating dictd dictionary for {file} [{databases.index(file) + 1}/{len(databases)}]... Word [0/0]")
        db_name = ".".join(file.split(".")[:-1])
        dict_file = open(f"dictd/dictionaries/{db_name}.txt", "w+")
        dict_file.writelines(LICENSE)

        db = sqlite3.connect(f"data/{file}", check_same_thread=False)
        rows = db.execute("SELECT word, document FROM dictionary").fetchall()
        total = len(rows)
        for index, [word, raw_document] in enumerate(rows):
            document = json.loads(raw_document)
            if document:
                for obj in document['definitions']:
                    heading = f"<B>{word} - </B> {obj['nature']}{', ' + obj['gender'] if obj['gender'] != '' else ''}"
                    defs = list(map(lambda expl: sanitize(expl, obj['explanations']), obj['explanations']))
                    dict_file.writelines([f"\n<A NAME=\"{word}\">\n", heading, *defs, "\n"])
            print(f"\033[A\033[KGenerating dictd dictionary for {file} [{databases.index(file) + 1}/{len(databases)}]... Word [{index + 1}/{total}]")

        dict_file.close()
        db.close()
