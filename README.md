<div align="center">
<br>
<br>
<img alt="Remede icon" src=".github/icon.png" height="100" width="100">

# Remède
Open Source and free alternative to Antidote.

[Data credits](#données-remède) • [License](https://github.com/camarm-dev/remede/blob/main/LICENSE)

</div>

## Buts

- [x] Interface de recherche
- [x] Marques pages
- [x] Partager un mot
- [x] Complétion automatique sur la recherche
- [x] Lire un mot
- [x] Conjugaisons
- [x] Dans un doc Remède
- [x] Afficher
- [x] Référencer tous les mots (#21)
- [ ] Page de présentation
- [ ] Applications de bureaux
  -  [ ] Windows 
  -  [ ] MAC 
  -  [ ] Linux 
- [ ] API publique
  - [ ] Mot du jour
  - [x] Obtenir document d'un mot
- [ ] Fiches de français (#4)

## Télécharger

Téléchargez les exécutables pour votre plateforme depuis [la page releases](/releases)

SOON: Disponible sur Play Store


## Development

- Installer les dépendances
```shell
npm i
```
- Installer ionic
```shell
npm i -g @ionic/cli
```

### Application mobile

- Construire un fichier APK:
```shell
ionic cap build android
```

### Données Remède
Remède créé sa propre base de mots, synonymes, antonymes français à partir de services tiers.

- Les définitions par le [Wictionary français](https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil), vie le wrapper de [Frederic Gainza](https://api-definition.fgainza.fr/) de l'API
- Les synonymes via [synonymo.fr](http://www.synonymo.fr)
- Les antonymes via [antonyme.org](http://www.antonyme.org)
- Les conjugaisons via [conjuguons.fr](http://www.conjuguons.fr)
- Les exemples de ???? (pas encore disponible)
- Les IPA de [Open Dict Data](https://github.com/open-dict-data/ipa-dict)

### Dataset

Le dossier `data` est destiné aux ressources linguistiques utilisées par Remède

`data/mots.txt`: Liste de 245 973 mots séparés de virgules

`data/ipa.json`: Pour une clé 'mot', renvoi l'IPA

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

### API

- Installer python3
- Installer les dépendances
```shell
pip install fastapi uvicorn starlette
```
- Lancer le serveur
```shell
python3 server.py
```
En ligne sur [localhost:8000](http:/localhost:8000) !

Documentation sur [localhost:8000/docs](http:/localhost:8000/docs).

## Base sqlite

Le fichier `data/remede.db`, généré par le script `generate_sqlite.py` contient une base de données contenant tous les mots Remède.

Elle s'organise ainsi
- Une table `dictionary`

- Les champs
  - word (`string`: le mot)
  - document (`string`: le document Remède en format JSON)

Un questionnement se pose: se schéma n'étant pas propre (stocker du JSON dans une base sql), faut-il retranscrire complètement le schéma de document Remède en plusieurs tables dnas une base ?
