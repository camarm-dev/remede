const locales = {
    en: "English",
    fr: "Français",
    eo: "Esperanto",
    dialects: {
        fr: undefined,
        en: [
            "en-GB",
            "en-US",
            "en-CA",
            "en-AU",
            "en-NZ"
        ],
        eo: undefined
    }
}

export type localeCode = "en" | "fr" | "eo"

export function hasDialect(locale: keyof typeof locales["dialects"]) {
    return locales.dialects[locale]
}

export default locales
