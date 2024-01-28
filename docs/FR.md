
# Documentation

This page is also available in [english](/EN). 

Bienvenue sur la page de documentation de Remède. Naviguez à travers les contenus si-dessous

### Table des matières

- [Développement](#dévelopment)
  - [Setup](#installation-de-lenvironnement-de-développement) 
  - [Application mobile](#application-mobile) 
  - [Application Web](#application-web) 
  - [API](#api) 
- [Données](#données) 
  - [Données Remède](#données-remède) 
  - [Dataset](#dataset) 
  - [Schéma de données](#schéma-de-document-remède) 
  - [Base Sqlite](#base-sqlite) 
  - [Fiches de français](#fiches-de-francais) 

## Dévelopment

### Structure

- `app`: The ionic project
- `scripts`: Build, migrate and generate database
- `data`: Dataset and related ressources
- `builds`: Executables by platform

### Installation de l'environnement de développement
Dans le dossier `app`
- Installer les dépendances
```shell
npm i
```
- Installer ionic
```shell
npm i -g @ionic/cli
```
- Installer Git LFS
```shell
git lfs install
```

### Application mobile
Dans le dossier `app`
- Construire le projet android:
```shell
ionic cap build android
```
- Continuer ensuite dans Android Studio pour construire l'APK

### Application Web
Dans le dossier `app`

Ce projet utilise [ionic](https://ionicframework.com/docs).

- Lancer le projet
```shell
npm run dev
```


### API

À la racine du projet
- Installer python3
- Installer les dépendances python
```shell
pip install fastapi uvicorn starlette python-frontmatter markdown
```
- Récupérer la base de données avec Git LFS
```shell
git lfs pull
```

**Spécial**: Pour l'API ML
- Installer le service de TTS (non-implémenté)

- Lancer le serveur
```shell
python3 server.py
```
En ligne sur [localhost:8000](http:/localhost:8000) !

Documentation sur [localhost:8000/docs](http:/localhost:8000/docs).

> Veuillez [générer la base sqlite](#base-sqlite) pour fournir la dernière version de celle-ci !

## Données

Cette section est à propos des données utilisées et fournies par Remède.

### Données Remède
Remède créé sa propre base de mots, synonymes, antonymes français à partir de services tiers.

- Les définitions, exemples et étymologies par le [Wictionary français](https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil), via le wrapper de [Frederic Gainza](https://api-definition.fgainza.fr/) de l'API, réadapté par [Labse Software](https://github.com/LabseSoftware/api-definition)
- Les synonymes via [synonymo.fr](http://www.synonymo.fr)
- Les antonymes via [antonyme.org](http://www.antonyme.org)
- Les conjugaisons via [conjuguons.fr](http://www.conjuguons.fr)
- Les IPA de [Open Dict Data](https://github.com/open-dict-data/ipa-dict)
- Le service de TTS par [nanotts](https://github.com/gmn/nanotts)<sup>[Apache 2.0](https://github.com/gmn/nanotts/blob/master/LICENSE)</sup>, via l'API [opentts](https://github.com/synesthesiam/opentts)<sup>[Apache 2.0](https://github.com/gmn/nanotts/blob/master/LICENSE)</sup>, hébergée par nos soins
- Le service de correction par [languagetool.org](https://languagetool.org)<sup>[LGPL 2.1](https://github.com/languagetool-org/languagetool/blob/master/COPYING.txt)</sup>, hébergé par nos soins

### Dataset

Le dossier `data` est destiné aux ressources linguistiques utilisées par Remède

`data/mots.txt`: Liste de 245 973 mots séparés de virgules

`data/ipa.json`: Pour une clé 'mot', renvoi l'IPA
- Généré depuis `data/IPA.txt`: un fichier sur le format `[mot]\t[ipa]`

`data/REMEDE_a.jon`: Le fichier d'indexation final (par lettre) ; pour une clé 'mot' renvoi [son document selon le schéma REMEDE](#schéma-de-document-remède)

`data/remede.db`: Une base sql ([référence](#base-sqlite))

`data/remede-less.db`: Une base sql ([référence](#base-sqlite)) MAIS
- Sans les exemples
- Sans les étymologies
- Sans les rimes

### Schéma de document Remède
Schéma JSON d'un document de mot indexé par Remède

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

- `synonymes` (`[]string`): Liste des mots synonymes
- `antonymes` (`[]string`): Liste des mots antonymes
- `definitions` (`[]{}`): Liste d'objets contenants une définition du mot
    - `genre` (`string`): Genre du mot qui est défini
    - `classe` (`string`): Classe grammaticale du mot défini
    - `explications` (`[]string`): Listes des explications possibles de cette définition
    - `exemples` (`[]string`): Listes des exemples d'utilisation du mot (NON IMPLÉMENTÉ)
- `credits` (`{}`): Objet contenant les crédits relatifs à la définition
    - `name` (`string`): Nom de la source
    - `url` (`string`): Url de la source
- `ipa` (`string`): Prononciation du mot selon l'International Phonetic Alphabet
- `conjugaisons` (`{}`): Objet contenant les conjugaisons du mot si c'est un verbe
    - `[nom du mode]` (`{}`): Objet contenant les temps du mode
        - `[nom du temps]` (`{}`): Objet contenant les formes verbales du temps
            - `[sujet]` (`string`): Forme verbale du verbe (de `mode, temps, sujet`)

### Base sqlite

Le fichier `data/remede.db`, généré par le script `scripts/generate_sqlite.py` (à exécuter depuis la racine du project) contient une base de données contenant tous les mots Remède.

Elle s'organise ainsi
- Une table `dictionary`

- Les champs
    - word (`string`: le mot)
    - document (`string`: le document Remède en format JSON)

Un questionnement se pose: se schéma n'étant pas propre (stocker du JSON dans une base sql), faut-il retranscrire complètement le schéma de document Remède en plusieurs tables dnas une base ?

### Fiches de français

Des fiches de français sont écrites et référencées dans le dossier `data/fiches`.

Elles sont écrites en `markdown` et utilisent le `front-matter` pour fonctionner.

Exemple de fiche:

```yaml
---
nom: Exemple de fiche
description: Ceci est la première fiche
credits:
  attribution: Remède
  url: https://github.com/camarm-dev/remede
  text: "
Author(s): [camarm](https://github.com/camarm-dev)
Source: [Remède](https://github.com/camarm-dev/remede)
File historic and contributions: [On Github](https://github.com/camarm-dev/remede/commits/main/data/fiches/Exemple.md)
"
slug: exemple
tags: 
  - grammaire
  - orthographe
---

# Exemple

Ceci est un exemple de fiche.
```

Les tags disponibles sont: `grammaire`, `orthographe`, `conjugaison`, `lexique`, `style`, `typographie`

Pour créditer et permettre l'attribution de ces fiches, veuillez remplir correctement les champs `credits`.

- `credits.url`: L'url de la source (Le github Remède, ou lien du site source)
- `credits.attributions`: La personne ou le projet à citer en cas d'attribution
- `credits.text`: Les ressources annexes qui vous ont aidés, l'historique des modifications du fichier

Remplissez bien cette fiche, car elle permet la traçabilité et le respect de la propriété privée et intellectuelle concernant Rèmede et la provenance de ses données.