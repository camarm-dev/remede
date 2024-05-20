import {getOfflineDictionaryStatus} from "@/functions/offline"
import {RemedeDatabase} from "@/functions/database"

function removeAccents(value: string) {
    return value.normalize("NFD").replace(/\p{Diacritic}/gu, "").replaceAll("-", " ").replaceAll("'", " ")
}

async function useApi() {
    return !(await getOfflineDictionaryStatus()).downloaded
}

async function getAutocompleteWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/autocomplete/${word}`).then(resp => resp.json())
}

async function getAutocompleteFromDatabase(word: string) {
    return await database?.getAutocomplete(removeAccents(word)) as any[]
}

async function getSearchResultsWithAPI(query: string) {
    return await fetch(`https://api-remede.camarm.fr/search/${query}`).then(resp => resp.json())
}

async function getSearchResultsFromDatabase(query: string) {
    return await database?.search(removeAccents(query)) as any[]
}

async function getWordWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/word/${word}`).then(resp => resp.json())
}

async function getWordFromDatabase(word: string) {
    return await database?.getWord(word) as any[]
}

async function getRandomWordWithAPI() {
    return await fetch("https://api-remede.camarm.fr/random").then(resp => resp.json())
}

async function getRandomWordFromDatabase() {
    return await database?.getRandomWord() as string
}

async function doesWordExistsWithAPI(word: string) {
    return (await fetch(`https://api-remede.camarm.fr/word/${word}`).then(resp => resp.json())).message != "Mot non trouvé"
}

async function doesWordExistsWithDatabase(word: string) {
    try {
        await database?.getWord(word)
        return true
    } catch (e) {
        return false
    }
}

async function getAutocomplete(word: string) {
    if (await useApi()) {
        return await getAutocompleteWithAPI(word)
    }
    return await getAutocompleteFromDatabase(word)
}


async function getSearchResults(query: string) {
    if (await useApi()) {
        return await getSearchResultsWithAPI(query)
    }
    return await getSearchResultsFromDatabase(query)
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

async function getTodayWord() {
    try {
        return await fetch("https://api-remede.camarm.fr/word-of-day").then(resp => resp.json())
    } catch (e) {
        return ""
    }
}

async function wordExists(word: string) {
    if (await useApi()) {
        return doesWordExistsWithAPI(word)
    }
    return doesWordExistsWithDatabase(word)
}

async function getWordRimes(word: string, maxSyllabes?: number, minSyllabes?: number, elide?: boolean) {
    if (await useApi()) {
        return {
            rhymes: [],
            success: false
        }
    }
    return {
        rhymes: await database?.getWordRimes(word, maxSyllabes, minSyllabes, elide) as any[],
        success: true
    }
}

const database = await useApi() ? null: new RemedeDatabase()

export {
    getWordDocument,
    getAutocomplete,
    getSearchResults,
    getRandomWord,
    getTodayWord,
    wordExists,
    getWordRimes
}
