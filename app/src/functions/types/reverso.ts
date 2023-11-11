
interface ReversoCorrectionSuggestion {
    text: string
}

interface ReversoCorrection {
    type: string
    shortDescription: string
    longDescription: string
    mistakeText: string
    suggestions: ReversoCorrectionSuggestion[]
    startIndex: Number
    endIndex: Number
}

interface ExplainSegment {
    text: string
    correction: ReversoCorrection
}

export type {
    ReversoCorrection,
    ExplainSegment
}
