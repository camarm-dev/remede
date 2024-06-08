interface LanguageToolRule {
    id: string
    description: string
    category: LanguageToolCategory
}

interface LanguageToolCategory {
    id: string
    name: string
}

interface LanguageToolContext {
    text: string
    offset: number
    length: number
}

interface LanguageToolReplacement {
    value: string
}

interface LanguageToolCorrection {
    shortMessage: string
    message: string
    offset: number
    length: number
    rule: LanguageToolRule
    replacements: LanguageToolReplacement[]
    context: LanguageToolContext
}

interface ExplainSegment {
    text: string
    ignored: boolean
    correction: LanguageToolCorrection
}

export type {
    ExplainSegment,
    LanguageToolCorrection
}
