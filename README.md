<div align="center">
<br>
<br>
<img alt="Remede icon" src=".github/icon.png" height="100" width="100">

# Remède
Open Source and free alternative to Antidote.

</div>


## Development

### Application mobile

[//]: # (TODO)

Rien ici pour le moment

### Données Remède
Remède créé sa propre base de mots, synonymes, antonymes français à partir de service tiers.

- Les définitions par le dictionnaire Educalingo
- Les synonymes des [synonymo.fr](https://synonymo.fr)
- Les antonymes des [antonymo.fr](https://antonymo.fr)
- Les exemples de ????
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
  "synonymes": [],
  "antonymes": [],
  "definitions": [
    {
      "class": "",
      "definition": ""
    }
  ],
  "ipa": "",
  "prononciation": {
    "audio": "",
    "credits": ""
  },
  "exemples": {
    "contenu": "",
    "credits": ""
  }
}
```