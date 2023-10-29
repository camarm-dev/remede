import REMEDE from "../../../data/REMEDE.json"
import words from "../../../data/mots.txt"

const autocomplete = Object.keys(REMEDE)

function getWordDocument(word: string) {
    return REMEDE[word]
}

function getAutocomplete(query: string) {
    return autocomplete.filter(word => word.startsWith(query)).slice(0, 6)
}

export {
    getWordDocument,
    getAutocomplete
}
