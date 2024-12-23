import {getDownloadedDictionaries} from "@/functions/offline"
import {RemedeDatabase} from "@/functions/database"
import {FilledRemedeWordDocument, RemedeSource, RemedeWordDocument} from "@/functions/types/remede"
import {InformationsResponse, RemedeDictionaryOption} from "@/functions/types/apiResponses"

function removeAccents(value: string) {
    return value.normalize("NFD").replace(/\p{Diacritic}/gu, "").replaceAll("-", " ").replaceAll("'", " ").trim()
}

async function useApi() {
    return (await getDownloadedDictionaries()).length == 0
}

async function getAutocompleteWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/autocomplete/${word}?database=${databaseSlug}`).then(resp => resp.json())
}

async function getAutocompleteFromDatabase(word: string) {
    return await database?.getAutocomplete(removeAccents(word)) as any[]
}

async function getSearchResultsWithAPI(query: string, page: number) {
    return await fetch(`https://api-remede.camarm.fr/search/${query}?page=${page}&database=${databaseSlug}`).then(resp => resp.json())
}

async function getSearchResultsFromDatabase(query: string, page: number) {
    return await database?.search(removeAccents(query), page) as any[]
}

async function getWordWithAPI(word: string) {
    return await fetch(`https://api-remede.camarm.fr/word/${word}?database=${databaseSlug}`).then(resp => resp.json())
}

async function getWordFromDatabase(word: string) {
    return await database?.getWord(word) as any
}

async function getRandomWordWithAPI() {
    return await fetch(`https://api-remede.camarm.fr/random?database=${databaseSlug}`).then(resp => resp.json())
}

async function getRandomWordFromDatabase() {
    return await database?.getRandomWord() as string
}

async function doesWordExistsWithAPI(word: string) {
    return (await fetch(`https://api-remede.camarm.fr/word/${word}?database=${databaseSlug}`).then(resp => resp.json()).catch(() => { return { message: "Mot non trouvé" } })).message != "Mot non trouvé"
}

async function getWordsWithPhonemeWithAPI(phoneme: string) {
    return await fetch(`https://api-remede.camarm.fr/phoneme/${phoneme}?database=${databaseSlug}`).then(resp => resp.json())
}

async function getAvailableDictionariesWithAPI() {
    const response = await fetch("https://api-remede.camarm.fr").then(resp => resp.json()) as InformationsResponse
    return Object.values(response.dictionaries)
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


async function getSearchResults(query: string, page: number) {
    if (await useApi()) {
        return await getSearchResultsWithAPI(query, page)
    }
    return await getSearchResultsFromDatabase(query, page)
}

async function getWordDocument(word: string): Promise<FilledRemedeWordDocument> {
    if (await useApi()) {
        return await getWordWithAPI(word) as FilledRemedeWordDocument
    }
    const document = await getWordFromDatabase(word) as RemedeWordDocument
    if (!document) return document
    const sources: RemedeSource[] = []
    for (const source of document.sources) {
        sources.push(await getSource(source))
    }
    return {
        ...document,
        sources
    }
}

async function getRandomWord() {
    if (await useApi()) {
        return await getRandomWordWithAPI()
    }
    return await getRandomWordFromDatabase()
}

async function getTodayWord() {
    try {
        return await fetch(`https://api-remede.camarm.fr/word-of-day?database=${databaseSlug}`).then(resp => resp.json())
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

async function getWordRimes(word: string, maxSyllabes?: number, minSyllabes?: number, elide?: boolean, feminine?: boolean, quality = 0, nature: string[] = [], page = 0) {
    if (await useApi()) {
        return {
            rhymes: [],
            success: false
        }
    }
    return {
        rhymes: await database?.getWordRimes(word, maxSyllabes, minSyllabes, elide, feminine, quality, nature, page) as any[],
        success: true
    }
}

async function getRimesAutocomplete(query: string) {
    if (await useApi()) {
        return []
    }
    return await database?.getRimesAutocomplete(query) as any as Promise<string[]>
}

async function getWordsWithPhoneme(phoneme: string) {
    if (await useApi()) {
        return await getWordsWithPhonemeWithAPI(phoneme) as any as Promise<[string, RemedeWordDocument][]>
    }
    return await database?.getWordsWithPhoneme(phoneme) as any as Promise<[string, RemedeWordDocument][]>
}


async function getSource(source: string | RemedeSource): Promise<RemedeSource> {
    if (await useApi()) {
        // Source doc is returned already built by the API
        return source as RemedeSource
    }
    return await database?.getSource(source as string) as any as Promise<RemedeSource>
}

async function getAvailableDictionaries(): Promise<RemedeDictionaryOption[]> {
    if (await useApi()) {
        return await getAvailableDictionariesWithAPI()
    }
    return await getDownloadedDictionaries()
}

async function getFavoriteDictionary(dictionaries: RemedeDictionaryOption[]): Promise<RemedeDictionaryOption> {
    if (await useApi()) {
        return dictionaries[0]
    }
    return (await getDownloadedDictionaries()).find(downloadedDictionary => downloadedDictionary.favorite) || dictionaries[0]
}

let database = await useApi() ? null: new RemedeDatabase()
let databaseSlug = "remede"

async function setDictionary(dictionary: RemedeDictionaryOption) {
    console.log(`[Dictionary] Setting dictionary to ${dictionary.name} (${dictionary.slug})`)
    database = await useApi() ? null: new RemedeDatabase(dictionary)
    databaseSlug = dictionary.slug
}

export {
    getWordDocument,
    getAutocomplete,
    getSearchResults,
    getRandomWord,
    getTodayWord,
    wordExists,
    getWordRimes,
    getRimesAutocomplete,
    getWordsWithPhoneme,
    getAvailableDictionaries,
    getFavoriteDictionary,
    setDictionary
}
