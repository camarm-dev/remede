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
        const statement = `SELECT document FROM dictionary WHERE word = '${word}'`
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

export {
    RemedeDatabase
}
