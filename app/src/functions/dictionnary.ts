// import REMEDE from "../../../data/REMEDE.json"
import REMEDE_a from "../../../data/REMEDE_a.json"

const autocomplete = Object.keys(REMEDE_a)
const REMEDE = {
    'a': REMEDE_a
}

const transformLetter = {
    'â': 'a',
    'æ': 'a',
    'à': 'a',
    'ç': 'c',
    'î': 'i',
    'ï': 'i',
    'ù': 'u',
    'û': 'u',
    'ü': 'u',
    'é': 'e',
    'ë': 'e',
    'ê': 'e',
    'è': 'e'
}


function getRemedeByWord(word: string) {
    return REMEDE[word[0]] || REMEDE[transformLetter[word[0]]] || {}
}

function getAutocompleteByWord(word: string) {
    return Object.keys(getRemedeByWord(word.toLowerCase()))
}

function getWordDocument(word: string) {
    return getRemedeByWord(word)[word]
}

function getAutocomplete(query: string) {
    return getAutocompleteByWord(query).filter(word => word.startsWith(query)).slice(0, 6)
}

function getRandomWord() {
    return autocomplete[Math.floor(Math.random() * autocomplete.length)]
}

export {
    getWordDocument,
    getAutocomplete,
    getRandomWord
}
