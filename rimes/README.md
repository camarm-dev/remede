# Dictionnaire des rimes

Remède génère aussi son dictionnaire de rimes !

## Comment ça marche ?

Remède utilise le projet [drime](https://a3nm.net/git/drime) (2011-2020 by Antoine
Amarilli, [GPL-v3](https://a3nm.net/git/drime/file/COPYING.html)) pour générer une base de rimes françaises, puis
réorganise cette base grâce au script `scripts/build_rimes.py`.

---

## Base de données

Grâce à `scripts/generate_rime_graph.py`, une base `data/rimes.db` est générée. Elle suit le schéma si-dessous:

| word   | phon   | orgi   | freq  | min_nsyl | max_nsyl | word_end | phon_end | elidable | feminine |
|--------|--------|--------|-------|----------|----------|----------|----------|----------|----------|
| string | string | string | float | int      | int      | string   | string   | boolean  | boolean  |

`word1` est un mot qui rime avec `word2`; c'est une rime `type` = **`1` pauvre**, **`2` suffisante**, **`3` riches**

### Construire la base

Nous fournissons une version de la base `drime.sql` mais il vous est possible de construire vous-même cette base grâce 
aux instructions du [README drime](https://a3nm.net/git/drime/README)

Pour construire la base de données, il faut exécuter `scripts/build_rimes.py`.

## Service de rimes

La base de rimes est intégrée dans la base `data/remede.db` avec le script `scripts/build_rimes.py`.

Quand cette base est téléchargée, l'onglet "rimes" se débloque.
