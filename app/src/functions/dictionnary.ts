import REMEDE from "../../../data/REMEDE.json"

const autocomplete = Object.keys(REMEDE)

function getWordDocument(word: string) {
    return REMEDE[word]
}

function getAutocomplete(query: string) {
    return autocomplete.filter(word => word.startsWith(query)).slice(0, 6)
}

function getRandomWord() {
    return autocomplete[Math.floor(Math.random() * autocomplete.length)]
}

export {
    getWordDocument,
    getAutocomplete,
    getRandomWord
}
