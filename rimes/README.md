# Dictionnaire des rimes

Remède génère aussi son dictionnaire de rimes !

## Table of content
- [FR](#français)
  - [Service de rimes](#service-de-rimes)
- [EN](#english)
    - [Rhymes service](#rhymes-service)
- [Docker](#docker)

---

## Français

Grâce à `scripts/generate_rime_graph.py`, une base `data/rimes.db` est générée. Elle suit le schéma si-dessous:

| word1  | word2  | type |
|--------|--------|------|
| string | string | int  |

`word1` est un mot qui rime avec `word2`; c'est une rime `type` = **`1` pauvre**, **`2` suffisante**, **`3` riches**

### Service de rimes

L'API écrite en FastAPI, contenue dans `serve.py` et exécutable [avec Docker](#docker), expose:
- Un endpoint (`/<word>`), qui renvoie toutes les lignes contenant `<word>`

---

## English

With `scripts/generate_rime_graph.py`, a database `data/rimes.db` is generated. It follows this schema:

| word1  | word2  | type |
|--------|--------|------|
| string | string | int  |

`word1` is a word which rhymes with `word2`; it's a rhyme `type` = **`1` "poor"**, **`2` "medium"**, **`3` "rich"**

### Rhymes service

The API written in FastAPI, in `serve.py` (executable [with Docker](#docker)), serve:
- An endpoint (`/<word>`), which returns all the row that includes `<word>`

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
