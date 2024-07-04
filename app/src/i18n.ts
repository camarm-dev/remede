import  { createI18n } from 'vue-i18n'
import frenchTranslations from "@/data/translations/fr.json"

const globalizationList = {
    fr: frenchTranslations
}

export default createI18n({
    locale: 'fr',
    fallbackLocale: 'en',
    messages: globalizationList,
    preserveDirectiveContent: true
})
