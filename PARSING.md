## Générer les données Remède

Générer les données Remède consiste à générer **les fichiers JSON**, pour chaque lettre (`data/REMEDE_a.json`) mais aussi **la base Sqlite** `data.remede.db`.

> [!NOTE]
> La base `data/remede-less.json` est une ancienne version, qui ne contient pas les champs `exemples`, `etymologies` et `rimes`. Elle est utilisée comme base **light**, pour les appareils avec peu de place.

**Organisation d'une génération de données:**
1. `parse.py` génère un fichier JSON par lettre (plusieurs heures)
2. `generate_sqlite.py` génère la base Sqlite, depuis les fichiers JSON (plusieurs dizaines de minutes)

> [!IMPORTANT]
> Tous les programmes contenus dans le dossier `scripts` doivent être executés **à la racine du project** (eg. `python3 scripts/parse.py`)

## Parse.py

**Comment ça fonctionne ?**
1. Il itère + 250 000 mots (depuis `data/mots.txt`)
2. Pour chaque mot, il trouve sa définition avec [`api-definition`](#api-définition) et des services tiers
3. Il génère le document Remède
4. Il enregistre sous format `JSON`

```mermaid
flowchart TB
  words[(Word\ndatabase)] --> Loop
  Loop(Parser loop) --> def[Definition API]
  Loop --> syn[aynonymo.fr]
  Loop --> ant[antonymes.org]
  Loop .-> conj[conjuguons.fr]
  def --> doc{{Remède document}}
  syn --> doc
  conj .-> doc
  ant --> doc
  doc --> json[[Remède\nJSON]]
  json --> db[(Remède\nDatabase)]
```

### Lancer le parsing

1. Lancer [api-definition](#api-définition) en local
2. Lancer `parse.py`
```shell
python3 scripts/parse.py
```
Cette opération prend plusieurs jours !

## Api Définition

Cette API, originellement écrite par [Frederic Gainza](https://api-definition.fgainza.fr/), scrap les données du [Wictionary français](https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil).

Pour ce projet, **une réadaptation a été effectuée** par [Labse Software](https://github.com/LabseSoftware/api-definition)

### Lancer avec docker

Le code de cette API est contenu dans `api-definition` (c'est un submodule git).

Dans `api-definition`
```shell
docker build -t remede-definition-api . && docker run -p 8089:80 remede-definition-api
```