import datetime
import json
import os
import sqlite3
import xml.etree.ElementTree as ET
from xml import etree

LICENSE = """
This is a ¶ Remède Dictionary. This dictionary is a converted version of the Remède dictionary. 
Data comes from The Remède Project, © CECILL-2.1. Remède and its contributors <https://remede.camarm.fr>.
For more information, please contact <software@camarm.dev>.
"""

AUTHORS = [
    {
        "name": "Armand CAMPONOVO",
        "role": "developer"
    }
]

DICTS = {
    "remede.en": {
        "text": "English",
        "lang": "en"
    },
    "remede": {
        "text": "Français",
        "lang": "fr"
    }
}


def get_xdxf_default(variant: str) -> ET.Element:
    xdxf_root = ET.Element("xdxf", {"revision": "34"})
    meta = ET.Element("meta_info")
    variant_meta = DICTS.get(variant, {
        "text": "unknown",
        "lang": "en"
    })

    title = ET.Element("title")
    title.text = f"Remède {variant_meta['text']}"
    meta.append(title)

    full_title = ET.Element("full_title")
    full_title.text = f"Remède dictionary, version \"{variant_meta['text']}\"."
    meta.append(full_title)

    description = ET.Element("description")
    description.text = LICENSE
    meta.append(description)

    publisher = ET.Element("publisher")
    publisher.text = "The Remède Project"
    meta.append(publisher)

    file_ver = ET.Element("file_ver")
    file_ver.text = "0.0"
    meta.append(file_ver)

    creation_date = ET.Element("creation_date")
    creation_date.text = "24-02-2025"
    meta.append(creation_date)

    last_edited_date = ET.Element("last_edited_date")
    last_edited_date.text = datetime.datetime.now().strftime("%d-%m-%Y")
    meta.append(last_edited_date)

    dict_src_url = ET.Element("dict_src_url")
    dict_src_url.text = "https://remede.camarm.fr"
    meta.append(dict_src_url)

    languages = ET.Element("languages")
    from_lang = ET.Element("from", {"xml:lang": variant_meta['lang']})
    to_lang = ET.Element("to", {"xml:lang": variant_meta['lang']})
    languages.append(from_lang)
    languages.append(to_lang)
    meta.append(languages)

    authors = ET.Element("authors")
    for person in AUTHORS:
        el = ET.Element("author", {"role": person["role"]})
        el.text = person["name"]
        authors.append(el)
    meta.append(authors)

    xdxf_root.append(meta)
    return xdxf_root


if __name__ == '__main__':
    databases = list(filter(lambda x: x.endswith('.db') and "remede" in x and "legacy" not in x, os.listdir('data')))
    print("\n")
    for file in databases:
        print(f"\033[A\033[KGenerating dictd dictionary for {file} [{databases.index(file) + 1}/{len(databases)}]... Word [0/0]")
        db_name = ".".join(file.split(".")[:-1])
        dict_file = open(f"convert/dictionaries/{db_name}.xdxf", "wb+")

        xdxf = get_xdxf_default(db_name)

        # db = sqlite3.connect(f"data/{file}", check_same_thread=False)
        # rows = db.execute("SELECT word, document FROM dictionary").fetchall()
        # total = len(rows)
        # for index, [word, raw_document] in enumerate(rows):
        #     document = json.loads(raw_document)
        #     if document:
        #         for obj in document['definitions']:
        #             pass
        #     print(f"\033[A\033[KGenerating XDXF dictionary for {file} [{databases.index(file) + 1}/{len(databases)}]... Word [{index + 1}/{total}]")
        ET.ElementTree(xdxf).write(dict_file, 'utf-8', xml_declaration=True)
        dict_file.close()

        # db.close()
