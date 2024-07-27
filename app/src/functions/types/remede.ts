interface RemedeSheet {
    nom: string
    description: string
    contenu: string
    tags: string[]
    slug: string
}

interface RemedeExample {
    contenu: string
    sources: string
}


interface RemedeExplication {
    [key: string]: string | string[]
}

interface RemedeWordDefinition {
    genre: string | string[]
    classe: string
    explications: RemedeExplication
    exemples: RemedeExample[]
}

interface RemedeDefinitionCredits {
    name: string
    url: string
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
    etymologies: string[]
}

interface RemedeDictionary {
    [key: string]: RemedeWordDocument
}

interface RemedeDictionaryIndex {
    [key: string]: RemedeDictionary
}

type RemedeRhymeRow = string[] & number[]

interface RemedeSource {
    label: string
    url: string
}

export type {
    RemedeDictionary,
    RemedeDictionaryIndex,
    RemedeWordDocument,
    RemedeConjugateDocument,
    RemedeSheet,
    RemedeWordDefinition,
    RemedeRhymeRow,
    RemedeSource
}
