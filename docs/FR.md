
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

### Installation de l'environnement de développement
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

- Construire le projet android:
```shell
ionic cap build android
```
- Continuer ensuite dans Android Studio pour construire l'APK

### Application Web

Ce projet utilise [ionic](https://ionicframework.com/docs).

- Lancer le projet
```shell
npm run dev
```


### API

- Installer python3
- Installer les dépendances
```shell
pip install fastapi uvicorn starlette python-frontmatter markdown
```
- Récupérer la base de données avec Git LFS
```shell
git lfs pull
```
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

- Les définitions par le [Wictionary français](https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil), via le wrapper de [Frederic Gainza](https://api-definition.fgainza.fr/) de l'API
- Les synonymes via [synonymo.fr](http://www.synonymo.fr)
- Les antonymes via [antonyme.org](http://www.antonyme.org)
- Les conjugaisons via [conjuguons.fr](http://www.conjuguons.fr)
- Les exemples de ???? (pas encore disponible)
- Les IPA de [Open Dict Data](https://github.com/open-dict-data/ipa-dict)

### Dataset

Le dossier `data` est destiné aux ressources linguistiques utilisées par Remède

`data/mots.txt`: Liste de 245 973 mots séparés de virgules

`data/ipa.json`: Pour une clé 'mot', renvoi l'IPA
- Généré depuis `data/IPA.txt`: un fichier sur le format `[mot]\t[ipa]`

`data/REMEDE_a.jon`: Le fichier d'indexation final (par lettre) ; pour une clé 'mot' renvoi [son document selon le schéma REMEDE](#schéma-de-document-remède)

`data/remede.db`: Une base sql ([référence](#base-sqlite))

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
  "image": {
    "url": "",
    "credits": ""
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
- `image` (`{}`): Objet contenant une image complémentaire à la définition
    - `url` (`string`): Url de l'image
    - `credits` (`string`): Url redirigeant vers les droits d'auteur de l'image
- `ipa` (`string`): Prononciation du mot selon l'International Phonetic Alphabet
- `conjugaisons` (`{}`): Objet contenant les conjugaisons du mot si c'est un verbe
    - `[nom du mode]` (`{}`): Objet contenant les temps du mode
        - `[nom du temps]` (`{}`): Objet contenant les formes verbales du temps
            - `[sujet]` (`string`): Forme verbale du verbe (de `mode, temps, sujet`)

### Base sqlite

Le fichier `data/remede.db`, généré par le script `generate_sqlite.py` contient une base de données contenant tous les mots Remède.

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

```markdown
---
nom: Exemple de fiche
description: Ceci est la première fiche
credits: http://example.com
tags: 
  - grammaire
  - orthographe
---

# Exemple

Ceci est un exemple de fiche.
```

Les tags disponibles sont: `grammaire`, `orthographe`
