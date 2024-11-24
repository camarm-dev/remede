/**
 * A Remède word document schema. This document represent all the word metadata.
 */
export interface RemedeWordDocument {
    /**
     * The synonyms of the word.
     */
    synonyms: string[]
    /**
     * The antonyms of the word.
     */
    antonyms: string[]
    /**
     * The etymologies of the word.
     */
    etymologies: string[]
    /**
     * The word's definitions.
     */
    definitions: {
        /**
         * Word gender for this definition.
         */
        gender: string
        /**
         * Word nature for this definition.
         */
        nature: string
        /**
         * Different explanations of the word.
         */
        explanations: (string | string[])[]
        /**
         * Different examples usages of the word.
         */
        examples: {
            /**
             * The example content.
             */
            content: string
            /**
             * The example source.
             */
            sources: string
        }[]
        /**
         * Plurals orthography of the word.
         */
        plurals: {
            /**
             * The label of the plural (example: "Masculins" or "Variant 1").
             */
            label?: string
            /**
             * The singular form.
             */
            singular?: string
            /**
             * The plural form.
             */
            plural?: string
        }[]
    }[]
    /**
     * The sources ids. Used to display sources link on the interface. See https://docs.remede.camarm.fr/docs/database/schema#sourcesids
     */
    sources: string[]
    /**
     * The word IPA notation. Can be a list of IPA notations, comma separated.
     */
    phoneme: string
    /**
     * The word pronunciation audio URL.
     */
    pronunciation: {
        /**
         * An URL pointing to the pronunciation audio file.
         */
        audio: string
        /**
         * URL pointing to credits page.
         */
        credits: string
    } | null
    /**
     * The word's conjugations if it is a verb.
     */
    conjugations: {
        [k: string]: {
            [k: string]: {
                [k: string]: string
            }
        }
    }
}
