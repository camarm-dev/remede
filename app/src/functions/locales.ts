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
    return Object.prototype.hasOwnProperty.call(locales.dialects, locale)
}

export default locales
