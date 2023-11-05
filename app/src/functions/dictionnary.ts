import {getOfflineDictionaryStatus} from "@/functions/offline";

async function useApi() {
    return !(await getOfflineDictionaryStatus()).downloaded
}

async function getAutocompleteWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/autocomplete/${word}`).then(resp => resp.json())
}

async function getAutocompleteFromDatabase(word: string) {
    // TODO
    return []
}

async function getWordWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/word/${word}`).then(resp => resp.json())
}

async function getWordFromDatabase(word: string) {
    // TODO
    return {}
}

async function getAutocomplete(word: string) {
    if (await useApi()) {
        return await getAutocompleteWithAPI(word)
    }
    return await getAutocompleteFromDatabase(word)
}

async function getWordDocument(word: string) {
    if (await useApi()) {
        return await getWordWithAPI(word)
    }
    return await getWordFromDatabase(word)
}

function getRandomWord() {
    // TODO
    return {}
}

export {
    getWordDocument,
    getAutocomplete,
    getRandomWord
}
