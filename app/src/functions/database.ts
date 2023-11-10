import { CapacitorSQLite } from '@capacitor-community/sqlite'

async function openDatabase() {
    await CapacitorSQLite.open({ database: 'remede' })
}

class RemedeDatabase {

    constructor() {
        openDatabase()
    }

    async getWord(word: string) {
        const statement = 'SELECT * FROM  dictionary WHERE word = ?'
        const response = await this.query(statement, [word])
        return response.values
    }

    async getAutocomplete(query: string) {
        const statement = "SELECT * FROM  dictionary WHERE word LIKE ? + '%'"
        const response = await this.query(statement, [query])
        return response.values
    }

    async getRandomWord() {
        const statement = "SELECT word FROM dictionary ORDER BY RANDOM() LIMIT 1"
        const response = await this.query(statement, [])
        return response.values
    }

    async query(statement: string, values: string[]) {
        return await CapacitorSQLite.query({
          statement: statement,
          values: values
        })
    }
}

export {
    RemedeDatabase
}
