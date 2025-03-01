import  { createI18n } from "vue-i18n"
import frenchTranslations from "@/data/translations/fr.json"
import englishTranslations from "@/data/translations/en.json"
import esperantoTranslations from "@/data/translations/eo.json"

const globalizationList = {
    fr: frenchTranslations,
    en: englishTranslations,
    eo: esperantoTranslations
}

export default createI18n({
    locale: "fr",
    fallbackLocale: "en",
    messages: globalizationList,
    preserveDirectiveContent: true
})
