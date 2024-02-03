# Dictionnaire des rimes

Remède génère aussi son dictionnaire de rimes !

Grâce à `scripts/generate_rime_graph.py`, une base `data/rimes.db` est générée. Elle suit le schéma si-dessous:

| word1  | word2  | type |
|--------|--------|------|
| string | string | int  |

`word1` est un mot qui rime avec `word2`; c'est une rime `type` = **`1` pauvre**, **`2` suffisante**, **`3` riches**

## Rimes service

L'API écrite en FastAPI, contenue dans `serve.py` et exécutable [avec Docker](#docker), expose:
- Un endpoint (`/<word>`), qui renvoie toutes les lignes contenant `<word>`
- Une interface (`/graph`)

## Docker

1. Build
```shell
docker build -t remede-rhymes .
```
2. Run
```shell
docker run -d -p 8000:8000 --name remede-rhymes --restart unless-stopped remede-rhymes
```
3. Visit [`localhost:8000`](http://localhost:8000)
