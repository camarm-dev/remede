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
- [ ] Page de présentation
- [ ] Référencer tous les mots
- [ ] API publique
  - [ ] Mot du jour
  - [ ] Obtenir document d'un mot
- [ ] Conjugaisons
  - [x] Dans un doc Remède
  - [ ] Afficher
- [ ] Exemples
- [ ] Lire un mot
- [ ] Fiches de français

## Development

### Application mobile

[//]: # (TODO)

Rien ici pour le moment

### Données Remède
Remède créé sa propre base de mots, synonymes, antonymes français à partir de service tiers.

- Les définitions par le [Wictionary français](), vie le wrapper de [Frederic Gainza]() de l'API
- Les synonymes via [synonymo.fr](https://www.synonymo.fr)
- Les antonymes via [antonyme.org](https://www.antonyme.org)
- Les exemples de ???? (pas encore disponible)
- Les IPA de [Open Dict Data](https://github.com/open-dict-data/ipa-dict)

### Dataset

Le dossier `data` est destiné aux ressources linguistiques utilisées par Remède

`data/mots.txt`: Liste de 245 973 mots séparés de virgules

`data/ipa.json`: Pour une clé 'mot', renvoi l'IPA

`data/REMEDE.jon`: Le fichier d'indexation final; pour une clé 'mot' renvoi [son document selon le schéma REMEDE](#schéma-de-document-remède)

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
- `conjugaisons` (`{}`): Objet contenant les conjugaisons du mot si c'est un verbe (NON IMPLÉMENTÉ)
  - `[nom du mode]` (`{}`): Objet contenant les temps du mode
    - `[nom du temps]` (`{}`): Objet contenant les formes verbales du temps
      - `[sujet]` (`string`): Forme verbale du verbe (de `mode, temps, sujet`)