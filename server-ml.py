import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from corrector import RemedeCorrectorEngine
from data.utils import transformLetter
from tts import RemedeIPAToSpeechEngine


class Correction(BaseModel):
    texte: str


class Pronunciation(BaseModel):
    ipa: str


version = "1.0.0"
app = FastAPI(title='Remède ML', description='Machine Learning API for Remède: corrector and TTS.', version=version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    """
    ### Renvoie des informations utiles à propos de l'API:
    - Sa version
    """
    return {
        "version": version,
        "message": "Check /docs for documentation"
    }


@app.post('/correct')
def correct_text(body: Correction):
    """
    Corrige le texte `texte` dans le corps de requête.
    """
    return {
        "corrections": corrector.correct(body.texte)
    }


@app.post('/pronunciation')
def tts(body: Pronunciation):
    """
    Renvoie une base64 d'un audio lisant le mot du champ `mot` du corps de requête.
    """
    return TTS.generate_audio(body.ipa)


if __name__ == '__main__':
    database = sqlite3.connect('data/remede.db', check_same_thread=False)
    corrector = RemedeCorrectorEngine(database, transformLetter)
    TTS = RemedeIPAToSpeechEngine()
    uvicorn.run(app, host='0.0.0.0')
