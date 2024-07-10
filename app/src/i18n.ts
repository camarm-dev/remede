import  { createI18n } from "vue-i18n"
import frenchTranslations from "@/data/translations/fr.json"
import englishTranslations from "@/data/translations/en.json"

const globalizationList = {
    fr: frenchTranslations,
    en: englishTranslations
}

export default createI18n({
    locale: "fr",
    fallbackLocale: "en",
    messages: globalizationList,
    preserveDirectiveContent: true
})
