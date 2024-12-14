import {getRawDictionary} from "@/functions/offline"
import initSqlJS, {Database} from "sql.js"
import {toastController} from "@ionic/vue"

async function openDatabase() {
    try {
        const SQL = await initSqlJS({
            locateFile: () => "/sql-wasm.wasm"
        })
        const raw = await getRawDictionary()
        return new SQL.Database(raw)
    } catch (e) {
        const message = await toastController.create({
            header: "Erreur",
            message: `L'ouverture de la BDD à échouée: ${e}`,
            duration: 5000,
            color: "danger"
        })

        await message.present()
    }
}

class RemedeDatabase {

    private db?: Database

    constructor() {
        this.getDatabase().then(() => {
            console.log("Database loaded !")
        })
    }

    private async getDatabase() {
        this.db = await openDatabase()
    }

    async getWord(word: string) {
        const statement = `SELECT document FROM dictionary WHERE word = '${word.replaceAll("'", "''")}'`
        const response = await this.query(statement)
        return JSON.parse(response[0])
    }

    async getSource(identifier: string) {
        const statement = `SELECT label,url FROM sources WHERE identifier = '${identifier}'`
        const response = await this.rawQuery(statement) as string[][]
        return {
            label: response[0][0],
            url: response[0][1]
        }
    }

    async getAutocomplete(query: string) {
        const statement = `SELECT word FROM dictionary WHERE indexed LIKE '${query}%' ORDER BY word COLLATE NOCASE ASC LIMIT 5`
        return await this.query(statement)
    }

    async search(query: string, page = 0) {
        const statement = `SELECT word FROM dictionary WHERE indexed LIKE '${query}%' ORDER BY word COLLATE NOCASE ASC LIMIT 50 OFFSET ${page * 50}`
        return await this.query(statement)
    }

    async getRandomWord() {
        const statement = "SELECT word FROM dictionary WHERE nature != 'VER' AND nature != '' ORDER BY RANDOM() LIMIT 1"
        const response = await this.query(statement)
        return response[0]
    }

    async getRimesAutocomplete(query: string) {
        const statement = `SELECT word FROM dictionary WHERE word LIKE '${query}%' OR word = '${query}' ORDER BY freq DESC LIMIT 5`
        return await this.query(statement) as any as Promise<string[]>
    }

    async getWordsWithPhoneme(phoneme: string) {
        const statement = `SELECT word, document FROM dictionary WHERE phoneme = '${phoneme}'`
        const response = await this.rawQuery(statement) as string[][]
        return response.flatMap(document => [document[0], JSON.parse(document[1])])
    }

    async getWordRimes(word: string, maxSyllabes = 0, minSyllabes = 0, elide = false, feminine = false, quality = 0, nature: string[], page = 0) {
        const statement = `SELECT phoneme FROM dictionary WHERE word = '${word}'`
        const response = await this.rawQuery(statement) as any[]
        const document = response[0]

        if (!document) return []

        const phon = document[0]

        const splicedPhon = phon.slice(phon.length - quality)
        const qualityFilter = `(phon LIKE '%${quality === 0 ? phon.slice(phon.length - 1): splicedPhon}')`

        let natureFilter = `(${nature.length === 0}`
        for (const string of nature) {
            natureFilter += ` OR nature LIKE '%${string}:%' OR nature LIKE '%${string}|%'`
        }
        natureFilter += ")"

        const query = `SELECT word, phoneme, feminine, elidable FROM dictionary WHERE
             ((${maxSyllabes === 0 || maxSyllabes === undefined} OR max_syllables >= ${minSyllabes})
             AND (${minSyllabes === 0 || minSyllabes === undefined} OR min_syllables <= ${maxSyllabes} OR (elidable AND min_syllables - 1 <= ${maxSyllabes} AND ${elide}))
             AND (feminine OR ${!feminine})
             AND ${qualityFilter}
             AND ${natureFilter})
             ORDER BY word ASC LIMIT 50 OFFSET ${page * 50}`
        return await this.rawQuery(query)
    }

    async rawQuery(statement: string) {
        if (!this.db) {
            return await new Promise((resolve) => {
                setTimeout(() => {
                    resolve(this.rawQuery(statement))
                }, 500)
            })
        }

        const parsed = []
        const results = this.db.exec(statement)
        for (const document of results) {
            for (const value of document.values) {
                parsed.push(value)
            }
        }

        return parsed
    }

    async query(statement: string): Promise<Array<string>> {
        if (!this.db) {
            return await new Promise((resolve) => {
                setTimeout(() => {
                    resolve(this.query(statement))
                }, 500)
            })
        }
        const results = this.db.exec(statement)
        const parsed = []

        for (const queryExecResult of results) {
            for (const value of queryExecResult.values) {
                parsed.push(value[0])
            }
        }

        return parsed as string[]
    }
}

export enum wordsNature {
    verbe = "VER",
    nom = "NOM",
    aux = "AUX",
    adverbe = "ADV",
    adjectif = "ADJ",
    preposition = "PRE",
    conjonction = "CON",
    pronom = "PRO",
    onomatopee = "ONO"
}

export {
    RemedeDatabase
}
