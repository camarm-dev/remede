import json
import math
import os
import random
import sqlite3
import time
from hashlib import md5

import frontmatter
import markdown
import requests
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

version = "1.0.0"
app = FastAPI(title='Remède, rimes', description='Un dictionnaire des rimes libre.', version=version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_word_rhymes(word: str):
    edges = []
    edges1 = cursor.execute('SELECT word2, type FROM dictionary WHERE word1 = ?', (word,)).fetchall()
    edges2 = cursor.execute('SELECT word1, type FROM dictionary WHERE word2 = ?', (word,)).fetchall()
    edges.extend(edges1)
    edges.extend(edges2)
    return edges


@app.get('/{word}')
def get_word_rhymes_document(word: str):
    """
    Renvoie toutes les rimes du mot `word`
    """
    return get_word_rhymes(word)


if __name__ == '__main__':
    database = sqlite3.connect('../data/rimes.db')
    cursor = database.cursor()
    uvicorn.run(app, host='0.0.0.0')
