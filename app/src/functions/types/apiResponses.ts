import {RemedeWordDocument} from "@/functions/types/remede"

interface RemedeDictionaryOption {
    name: string
    slug: string
    hash: string
    total: number
}

interface RemedeAvailableDictionaries {
    [key: string]: RemedeDictionaryOption
}

interface InformationsResponse {
    version: string
    message: string
    dataset: string
    dictionaries: RemedeAvailableDictionaries
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
