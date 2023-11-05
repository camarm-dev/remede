import { CapacitorSQLite, SQLiteConnection } from '@capacitor-community/sqlite'
import {getOfflineDictionaryStatus} from "@/functions/offline";

async function openDatabase() {
    const dictionary = await getOfflineDictionaryStatus()
    await CapacitorSQLite.open({ database: dictionary.path })
}

class RemedeDatabase {

    constructor() {
        openDatabase()
    }

    async getWord(word: string) {
        const statement = 'SELECT * FROM  dictionary WHERE word IS ?'
        const response = await this.query(statement, [word])
        return response.values
    }

    async getAutocomplete(query: string) {
        const statement = "SELECT * FROM  dictionary WHERE word LIKE ? + '%'"
        const response = await this.query(statement, [query])
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
