import {getOfflineDictionaryStatus} from "@/functions/offline";
import {RemedeDatabase} from "@/functions/database";

async function useApi() {
    return !(await getOfflineDictionaryStatus()).downloaded
}

async function getAutocompleteWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/autocomplete/${word}`).then(resp => resp.json())
}

async function getAutocompleteFromDatabase(word: string) {
    return await database?.getAutocomplete(word) as any[]
}

async function getWordWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/word/${word}`).then(resp => resp.json())
}

async function getWordFromDatabase(word: string) {
    const results = await database?.getWord(word) as any[]
    return results[0]
}

async function getRandomWordWithAPI() {
    return await fetch(`https://api-remede.camarm.fr/random`).then(resp => resp.json())
}

async function getRandomWordFromDatabase() {
    const results = await database?.getRandomWord() as any[]
    return results[0]
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

async function getRandomWord() {
    if (await useApi()) {
        return await getRandomWordWithAPI()
    }
    return await getRandomWordFromDatabase()
}

const database = await useApi() ? null: new RemedeDatabase()

export {
    getWordDocument,
    getAutocomplete,
    getRandomWord
}
