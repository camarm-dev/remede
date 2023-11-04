
interface RemedeWordDefinition {
    genre: string
    classe: string
    explications: string[]
    exemples: string[]
}

interface RemedeDefinitionCredits {
    name: string
    url: string
}

interface RemedeImage {
    url: string
    credits: string
}

interface RemedeConjugatePersons {
    [key: string]: string
}

interface RemedeConjugateTemps {
    [key: string]: RemedeConjugatePersons
}

interface RemedeConjugateModes {
    [key: string]: RemedeConjugateTemps
}

interface RemedeConjugateDocument {
    [key: string]: RemedeConjugateModes
}


interface RemedeWordDocument {
    synonymes: string[]
    antonymes: string[]
    definitions: RemedeWordDefinition[]
    credits: RemedeDefinitionCredits
    image: RemedeImage
    ipa: string
    conjugaisons: RemedeConjugateDocument
}

interface RemedeDictionary {
    [key: string]: RemedeWordDocument
}

interface RemedeDictionaryIndex {
    [key: string]: RemedeDictionary
}


export type {
    RemedeDictionary,
    RemedeDictionaryIndex,
    RemedeWordDocument
}