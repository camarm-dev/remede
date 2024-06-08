---
layout: post
title: "Utiliser les données Remède"
date: 2023-11-19
readable_date: 19 Novembre 2023
cover: /assets/blog_useremede.png
author: Armand, maintainer of Remède
tags: 
  - Documentation
---

Ce poste est destiné à vous apprendre comment intégrer notre dictionnaire dans vos applications...

## Table des matières

- [Pourquoi utiliser Remède ?](#pourquoi-utiliser-remède-)
- [Utilisation de nos services](#utiliser-nos-services)
  - [Avec l'API](#avec-lapi)
    - [Déployer votre propre instance](#lancez-votre-propre-instance)
  - [Avec nos fichiers JSON](#avec-les-fichiers-json)
  - [Avec notre base Sqlite](#avec-la-base-sqlite)
- [Attributions](#attributions)

## Pourquoi utiliser Remède ?

Si vous avez besoins de chercher une définition, des synonymes, des antonymes et plus d'informations à propos d'un mot Remède est fait pour vous:
- 100% open source
- Français
- Tout type de support (JSON, API, Sqlite)
- +220 000 mots 

## Utiliser nos services

Vous avez désormais trouvé l'outil parfait pour s'intégrer dans votre projet.
Vous verrez ci-dessous comment procéder pour chaque support disponible...

Chaque support renvoie un document JSON suivant le [schéma REMEDE](/FR#schéma-de-document-remède)

### Avec l'API

Remède possède sa propre API écrite en python avec Fastapi.

Une instance publique est accessible à [api-remede.camarm.fr](https://api-remede.camarm.fr) (retrouvez la documentation [ici](https://api-remede.camarm.fr/docs)).

Elle vous permet de:

- Rechercher un mot (renvoie 6 mots commençant par `query `): `/autocomplete/[query]`
- Obtenir le document d'un mot: `/word/[word]`
- Obtenir un mot aléatoire: `/random`
- Télécharger la base Sqlite: `/download`
- Obtenir des informations sur l'API: `/`

Cette option est conseillée pour les applications **web**, **basées sur le web**, **light**.

#### Lancez votre propre instance

Il est possible que vous vouliez garder le contrôle et la maintenance de votre propre API. C'est pour cela que vous pouvez facilement lancer votre propre instance.
1. Clonez [le dépôt](https://github.com/camarm-dev/remede)
2. Suivez la documentation [configurer et lancer l'api](/FR#api)


### Avec les fichiers JSON

Remède stocke par défaut ses mots indexés dans des fichiers JSON.


Ils sont disponibles depuis la racine du projet dans le dossier [data](https://github.com/camarm-dev/remede/tree/main/data), sous les noms [REMEDE_[lettre].json](https://github.com/camarm-dev/remede/tree/main/data).
Le ficher [REMEDE_a.json](https://github.com/camarm-dev/remede/tree/main/data/REMEDE_a.json) contient tous les mots commençants par 'a' et ainsi de suite...


Ils contiennent chaque mot, représentés par une clé du dictionnaire, qui est associée au document Remède de ce mot.

Cette option est conseillée pour les applications **javascript**, **python**, **expérimentales**.

- [Télécharger](/assets/REMEDE_json.zip)

### Avec la base Sqlite

Une base Sqlite peut être générée depuis les données JSON avec le script `generate_sqlite.py`, placé à la racine du projet.

Elle est formée ainsi:
- Une table dictionary
- Avec les champs
  - `word`: le mot
  - `document`: le document associé, en format JSON

Cette option est conseillée pour les applications **backend**, **utilitaire**, **natives**.

- <a href="https://api-remede.camarm.fr/download" download="remede.db">Télécharger</a>

## Attributions

Merci de préciser que vous utilisez nos services dans vos applications:
- Nom et url du repo
- eg: par Remède <https://github.com/camarm-dev/remede>

Licence [Cecill V2.1](https://github.com/camarm-dev/remede/blob/main/LICENSE)
