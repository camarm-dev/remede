import {RemedeWordDocument} from "@/functions/types/remede";

interface RemedeDictionaryOption {
    nom: string
    slug: string
    hash: string
}

interface RemedeAvailableDictionaries {
    [key: string]: RemedeDictionaryOption
}

interface InformationsResponse {
    version: string
    message: string
    dataset: string
    dictionnaires: RemedeAvailableDictionaries
}

type AutocompleteResponse = string[]

type WordResponse = RemedeWordDocument


export type {
    InformationsResponse,
    AutocompleteResponse,
    WordResponse,
    RemedeAvailableDictionaries,
    RemedeDictionaryOption
}
