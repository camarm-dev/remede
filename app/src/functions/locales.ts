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
        ]
    }
}

export function hasDialect(locale: string) {
    return locales.dialects.hasOwnProperty(locale)
}

export default locales
