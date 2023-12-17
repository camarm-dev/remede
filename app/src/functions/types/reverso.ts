
interface ReversoCorrectionSuggestion {
    text: string
}

interface ReversoCorrection {
    type: string
    shortDescription: string
    longDescription: string
    mistakeText: string
    suggestions: ReversoCorrectionSuggestion[]
    replacementText: string
    startIndex: number
    endIndex: number
}

interface ExplainSegment {
    text: string
    correction: ReversoCorrection
}

export type {
    ReversoCorrection,
    ExplainSegment
}
