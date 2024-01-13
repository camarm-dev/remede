interface RemedeSheet {
    nom: string
    description: string
    contenu: string
    tags: string[]
}

interface RemedeWordDefinition {
    genre: string | string[]
    classe: string
    explications: string[] | string[][]
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
    RemedeWordDocument,
    RemedeConjugateDocument,
    RemedeSheet
}