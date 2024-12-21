const locales = {
    en: "English",
    fr: "Français",
    dialects: {
        en: [
            "en-GB",
            "en-US",
            "en-CA",
            "en-AU",
            "en-NZ"
        ],
        fr: undefined
    }
}

export type localeCode = "en" | "fr"

export function hasDialect(locale: keyof typeof locales["dialects"]) {
    return locales.dialects[locale]
}

export default locales
