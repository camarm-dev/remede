// import REMEDE from "../../../data/REMEDE.json"
import REMEDE_a from "../../../data/REMEDE_a.json"

const autocomplete = Object.keys(REMEDE_a)
const REMEDE = {
    ...REMEDE_a
}


function getRemedeByWord(word: string) {
    // console.log(REMEDE[word[0]])
    // return REMEDE[word[0]]
    return REMEDE
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
