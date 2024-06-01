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

    async getAutocomplete(query: string) {
        const statement = `SELECT word FROM wordlist WHERE indexed LIKE '${query}%' LIMIT 5`
        return await this.query(statement)
    }

    async search(query: string) {
        const statement = `SELECT word FROM wordlist WHERE indexed LIKE '${query}%'`
        return await this.query(statement)
    }

    async getRandomWord() {
        const statement = "SELECT word FROM dictionary ORDER BY RANDOM() LIMIT 1"
        const response = await this.query(statement)
        return response[0]
    }

    async getRimesAutocomplete(query: string) {
        const statement = `SELECT word FROM rimes WHERE word LIKE '${query}%' OR word = '${query}' ORDER BY freq DESC LIMIT 5`
        return await this.query(statement) as any as Promise<string[]>
    }

    async getWordRimes(word: string, maxSyllabes = 0, minSyllabes = 0, elide = false, feminine = false, quality: number = 0, nature: string[], page = 0) {
        const statement = `SELECT phon_end, phon FROM rimes WHERE word = '${word}'`
        const response = await this.rawQuery(statement) as any[]
        const document = response[0]

        if (!document) return []

        const phonEnd = document[0]
        const phon = document[1]

        const splicedPhon = phon.slice(phon.length - quality)
        const qualityFilter = `(${quality === 0} OR phon LIKE '%${splicedPhon}')`

        let natureFilter = `(${nature.length === 0}`
        for (const string of nature) {
            natureFilter += ` OR orgi LIKE '%${string}:%' OR orgi LIKE '%${string}|%'`
        }
        natureFilter += ')'

        const query = `SELECT word, phon, feminine, elidable FROM rimes WHERE (phon_end = '${phonEnd}')
             AND ((${maxSyllabes === 0 || maxSyllabes === undefined} OR max_nsyl >= ${minSyllabes})
             AND (${minSyllabes === 0 || minSyllabes === undefined} OR min_nsyl <= ${maxSyllabes} OR (elidable AND min_nsyl - 1 <= ${maxSyllabes} AND ${elide}))
             AND (feminine OR ${!feminine})
             AND ${qualityFilter}
             AND ${natureFilter})
             ORDER BY freq DESC LIMIT 50 OFFSET ${page * 50}`
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
    verbe = 'VER',
    nom = 'NOM',
    aux = 'AUX',
    adverbe = 'ADV',
    adjectif = 'ADJ',
    preposition = 'PRE',
    conjonction = 'CON',
    pronom = 'PRO',
    onomatopee = 'ONO'
}

export {
    RemedeDatabase
}
