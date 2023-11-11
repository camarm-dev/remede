import {CapacitorSQLite, SQLiteConnection, SQLiteDBConnection} from '@capacitor-community/sqlite'

async function openDatabase() {
    const sqlite = new SQLiteConnection(CapacitorSQLite)
    const db = await sqlite.createConnection('remedeSQLite', false, '', 1, true)
    await db.open()
    return db
}

class RemedeDatabase {

    private db: SQLiteDBConnection | any

    constructor() {
        this.getDatabase()
    }

    private async getDatabase() {
        this.db = await openDatabase()
    }

    async getWord(word: string) {
        const statement = 'SELECT * FROM dictionary WHERE word = ?'
        const response = await this.query(statement, [word])
        return response.values
    }

    async getAutocomplete(query: string) {
        const statement = "SELECT word FROM dictionary WHERE word LIKE ? + '%'"
        const response = await this.query(statement, [query])
        return response.values
    }

    async getRandomWord() {
        const statement = "SELECT word FROM dictionary ORDER BY RANDOM() LIMIT 1"
        const response = await this.query(statement, [])
        return response.values
    }

    async query(statement: string, values: string[]) {
        return await this.db.query(statement, values)
    }
}

export {
    RemedeDatabase
}
