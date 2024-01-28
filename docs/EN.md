
# English Documentation

This page is also available in [french](/FR).

Welcome on the documentation page of Remède ! Navigate through the contents below 

### Table of content

- [Development](#development)
    - [Setup](#setting-up-development-environment)
    - [Mobile application](#mobile-application)
    - [Web application](#web-application)
    - [API](#api)
- [Datas](#datas)
    - [Remède's data](#remèdes-data)
    - [Dataset](#dataset)
    - [Remede document schema](#remède-document-schema)
    - [Sqlite Database](#sqlite-database)
    - [Cheatsheets](#cheatsheets)

## Development

### Structure

- `app`: The ionic project
- `scripts`: Build, migrate and generate database
- `data`: Dataset and related ressources
- `builds`: Executables by platform

### Setting up development environment
In `app` folder
- Install dependencies
```shell
npm i
```
- Install ionic
```shell
npm i -g @ionic/cli
```
- Install Git LFS
1. Install extension [here](https://packagecloud.io/github/git-lfs/install)
2. Setup extension
```shell
git lfs install
```

### Mobile application
In `app` folder
- Build the project for android:
```shell
ionic cap build android
```
- Then continue in Android Studio to build APK

### Web Application
In `app` folder

This project uses [ionic](https://ionicframework.com/docs).

- Run the project
```shell
npm run dev
```


### API

At project root

- Install python3
- Install dependencies
```shell
pip install fastapi uvicorn starlette python-frontmatter markdown
```
- Fetch database with Git LFS
```shell
git lfs pull
```
- Start the server
```shell
python3 server.py
```
Running on [localhost:8000](http:/localhost:8000) !

Documentation available at [localhost:8000/docs](http:/localhost:8000/docs).

> Please [generate the sqlite database](#sqlite-database) to serve the latest version of this one through the API !

## Datas

This section is destined to the data used and distributed by Remède.

### Remède's data
Remède creates is own base of french words, synonyms, antonyms with extern services.

- Definitions, examples and etymologies by the [french Wictionary](https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil), with the API wrapper made by [Frederic Gainza](https://api-definition.fgainza.fr/), modified by [Labse Software](https://github.com/LabseSoftware/api-definition) for Remède.
- Synonyms from [synonymo.fr](http://www.synonymo.fr)
- Antonyms from [antonyme.org](http://www.antonyme.org)
- Conjugations from [conjuguons.fr](http://www.conjuguons.fr)
- Examples from ???? (not implemented)
- IPA from [Open Dict Data](https://github.com/open-dict-data/ipa-dict)
- The TTS service from [nanotts](https://github.com/gmn/nanotts)<sup>[Apache 2.0](https://github.com/gmn/nanotts/blob/master/LICENSE)</sup>, implemented in the API [opentts](https://github.com/synesthesiam/opentts)<sup>[Apache 2.0](https://github.com/gmn/nanotts/blob/master/LICENSE)</sup>, hosted by us
- The corrector service by [languagetool.org](https://languagetool.org)<sup>[LGPL 2.1](https://github.com/languagetool-org/languagetool/blob/master/COPYING.txt)</sup>, hosted by us


### Dataset

The `data` folder is destined to the linguistics ressources used by Remède.

`data/mots.txt`: List of 245 973 words, comma separated

`data/ipa.json`: For a key 'word', returns his IPA
- Generated from `data/IPA.txt`: a text file of format `[word]\t[ipa]`

`data/REMEDE_a.jon`: The final indexed file ; for a key 'word' returns [his document following the REMEDE schema](#remède-document-schema)

`data/remede.db`: A sqlite database ([reference](#sqlite-database))

`data/remede-less.db`: A sqlite database ([reference](#sqlite-database)) BUT
- Without examples
- Without etymologies
- Without rimes

### Remède document schema
JSON schema of an indexed word by Remède.

```json
{
  "synonymes": [
    ""
  ],
  "antonymes": [
    ""
  ],
  "definitions": [
    {
      "genre": "",
      "classe": "",
      "explications": [
        ""
      ],
      "exemples": [
        ""
      ]
    }
  ],
  "credits": {
    "name": "page Wiktionnaire",
    "url": ""
  },
  "ipa": "//",
  "conjugaisons": {
    "indicatif": {
      "present": {
        "je": "",
        "tu": ""
      }
    }
  }
}
```

- `synonymes` (`[]string`): List of synonyms
- `antonymes` (`[]string`): List of antonyms
- `definitions` (`[]{}`): List of objects containing a word definition
    - `genre` (`string`): The 'genre' of defined word
    - `classe` (`string`): The grammar class of defined word
    - `explications` (`[]string`): List of possible explanation of defined word
    - `exemples` (`[]string`): List of examples sentences using this word (NOT IMPLEMENTED)
- `credits` (`{}`): Object containing credits of the definitions
    - `name` (`string`): Source name
    - `url` (`string`): Source Url
- `ipa` (`string`): International Phonetic Alphabet pronunciation of the word
- `conjugaisons` (`{}`): Object containing word's conjugations
    - `[nom du mode]` (`{}`): Object containing conjugations' tenses for mode
        - `[nom du temps]` (`{}`): Object containing subjects of tense
            - `[sujet]` (`string`): Verbal form (of `mode, tense, subject`)

### Sqlite database

The file `data/remede.db`, generated by `scripts/generate_sqlite.py` (execute at project root) contains a database of every indexed Remède word.

His schema is:
- A `dictionary` table

- With fields
    - word (`string`: the mot)
    - document (`string`: the Remède document in JSON format)

### Cheatsheets

Cheatsheet containing french orthography and grammar lessons are written in the `data/fiches` folder.

They are written in `markdown` and use `fronr-matter` to work.

Cheatsheet example:

```markdown
---
nom: Exemple de fiche
description: Ceci est la première fiche
credits: https://remede.camarm.fr/sheets-credits#example
slug: exemple
tags: 
  - grammaire
  - orthographe
---

# Exemple

Ceci est un exemple de fiche.
```

Available tags: `grammaire`, `orthographe`, `conjugaison`, `lexique`, `style`, `typographie`

To credit and permit right attribution of these sheets, please **fill correctly** the `credits` fields in the frontmatter.
- `credits.url`: Source URL (Remède GitHub link or source website url)
- `credits.attributions`: The person or project to attribute
- `credits.text`: The ressources that helped you, the file modification historic.

Please fill correctly this file, because it tracks authors and contributions, and is here to respect privacy policies and copyrights about Rèmede and the sources of its data ! 
