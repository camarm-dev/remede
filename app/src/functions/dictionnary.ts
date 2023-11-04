import {RemedeDictionaryIndex} from "@/functions/types/remede";

const REMEDE = {
    'a': import("../../../data/REMEDE_a.json"),
    'b': import("../../../data/REMEDE_b.json"),
    'c': import("../../../data/REMEDE_c.json")
} as RemedeDictionaryIndex

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
    const autocomplete = Object.keys(REMEDE['c'])
    return autocomplete[Math.floor(Math.random() * autocomplete.length)]
}

export {
    getWordDocument,
    getAutocomplete,
    getRandomWord
}
