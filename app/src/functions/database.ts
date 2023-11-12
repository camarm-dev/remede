import {getRawDictionary} from "@/functions/offline";
import initSqlJS, {Database} from "sql.js"

async function openDatabase() {
    const SQL = await initSqlJS({
        locateFile: file => `/sql-wasm.wasm`
    })
    const raw = await getRawDictionary()
    return new SQL.Database(raw)
}

class RemedeDatabase {

    private db: Database

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
        const response = this.query(statement)
        return JSON.parse(response[0])
    }

    async getAutocomplete(query: string) {
        const statement = `SELECT word FROM dictionary WHERE word LIKE '${query}%' LIMIT 6`
        return this.query(statement)
    }

    async getRandomWord() {
        const statement = "SELECT word FROM dictionary ORDER BY RANDOM() LIMIT 1"
        return this.query(statement)[0]
    }

    query(statement: string) {
        const results = this.db.exec(statement)
        const parsed = []

        for (const queryExecResult of results) {
            for (const value of queryExecResult.values) {
                parsed.push(value[0])
            }
        }

        return parsed
    }
}

export {
    RemedeDatabase
}
