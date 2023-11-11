import {RemedeWordDocument} from "@/functions/types/remede";

interface InformationsResponse {
    version: string
    message: string
    dataset: string
}

type AutocompleteResponse = string[]

type WordResponse = RemedeWordDocument


export type {
    InformationsResponse,
    AutocompleteResponse,
    WordResponse
}
