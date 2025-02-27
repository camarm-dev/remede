import TCPClient from "@/functions/plugins/tcpClient"

export type DictServer = {
    name: string
    host: string
    port: number
    description: string
}

export type DictDefinition = {
    word: string
    databaseId: string
    database: string
    definition: string,
    server?: string,
    port?: number
}

export enum DictRequestType {
    Match = "MATCH",
    Define = "DEFINE"
}

export type DictDatabase = {
    name: string
    id: string
}

export type DictStrategy = {
    name: string
    id: string
}

export type DictRequest = {
    server: string
    port: number
    database: string
    word: string
    auth: boolean
    username?: string
    password?: string
    strat?: string
    method: DictRequestType
}

enum ResponseLineType {
    Header = "HEADER",
    Status = "STATUS",
    Data = "DATA",
    Command = "COMMAND"
}

export type DictResponseLine = {
    type: ResponseLineType
    success: boolean
    raw: string
    code?: string
    codeMeaning?: string
}

function getValueAt<T, D>(list: T[], index: number, _default: D): T | D {
    if (list[index]) {
        return list[index]
    }
    return _default
}


const successCodes = [110, 111, 112, 113, 114, 130, 150, 151, 152, 210, 220, 221, 230, 250, 330]
// const errorCodes = [420, 421, 500, 501, 502, 503, 530, 531, 532, 550, 552, 554, 555]


/*
  @param request "Request looks like dict:// "<user>;<auth>@<host>:<port>/<c>:<word>:<database>:<strategy>:<n>""
 */
export function decodeRequest(request: string) {
    const decodedRequest: DictRequest = {
        server: "",
        port: 2628,
        database: "!",
        word: "",
        auth: false,
        method: DictRequestType.Define
    }

    // Clear protocol
    request = request.replace("dict://", "")

    // Contains auth
    if (request.includes("@")) {
        decodedRequest.auth = true
        const [user, auth] = request.split("@")[0].split(";")
        decodedRequest.username = user
        decodedRequest.password = auth // This is auth type (AUTH or SASLAUTH)
        request = request.split("@")[1]
    }

    if (!request.includes("/")) { // Just specify a dict server URL
        const [server, port] = request.split(":")
        decodedRequest.server = server
        decodedRequest.port = Number(port || 2628)
        return decodedRequest
    }

    const [host, req] = request.split("/")
    if (host.includes(":")) {
        const [server, port] = host.split(":")
        decodedRequest.server = server
        decodedRequest.port = Number(port)

    } else {
        decodedRequest.server = host
    }

    const requestParts = req.split(":")

    const method = getValueAt(requestParts, 0, "d")
    switch (method) {
        case "m":
            decodedRequest.method = DictRequestType.Match
            break
        case "d":
        default:
            decodedRequest.method = DictRequestType.Define
            break
    }

    decodedRequest.word = getValueAt(requestParts, 1, "none")

    decodedRequest.database = getValueAt(requestParts, 2, "!")
    // It was not the strat def but the nth definition
    if (/^\d+$/.test(decodedRequest.database)) {
        decodedRequest.database = "!"
    }

    decodedRequest.strat = getValueAt(requestParts, 3, ".")

    // It was not the strat def but the nth definition
    if (/^\d+$/.test(decodedRequest.strat)) {
        decodedRequest.strat = undefined
    }

    return decodedRequest
}

function buildDICTRequests(request: DictRequest): string[] {
    const requests: string[] = []
    if (request.auth) {
        // TODO
    }
    switch (request.method) {
        case "DEFINE":
            requests.push(`${request.method} ${request.database} "${request.word}"`)
            break
        case "MATCH":
            requests.push(`${request.method} ${request.database} ${request.strat} "${request.word}"`)
    }
    return requests
}

function decodeRawResponse(responses: string[], commands: string[] = []) {
    const rawDecoded: DictResponseLine[] = []
    const data = []
    const definitions: DictDefinition[] = []
    for (const command of commands) {
        rawDecoded.push({
            raw: command,
            type: ResponseLineType.Command,
            success: true
        })
    }
    for (const line of responses) {
        const code = line.substring(0, 3)
        if (code == "220") {
            rawDecoded.push({
                raw: responses[0],
                type: ResponseLineType.Header,
                success: true
            })
        } else if (/^\d+$/.test(code)) { // The line is a status info : it starts with a xxx status code
            rawDecoded.push({
                raw: line,
                code,
                success: successCodes.includes(Number(code)),
                type: ResponseLineType.Status
            })
        } else if (line.startsWith(".")) { // End of data
            rawDecoded.push({
                raw: line,
                success: true,
                type: ResponseLineType.Data
            })
        } else {
            data.push(line)
            rawDecoded.push({
                raw: line,
                success: true,
                type: ResponseLineType.Data
            })
        }

        // Special case to retrieve definitions
        if (code == "151") {
            const groups = line.replace("151 ", "").match(/[\w\-.]+|"(?:\\"|[^"])+"/g) as any as string[]
            const [word, databaseId, database] = [groups[0].replaceAll("\"", ""), groups[1], groups[2].replaceAll("\"", "")]
            let definition = ""
            for (const definitionLine of responses.slice(responses.indexOf(line) + 1)) {
                if (definitionLine == ".") {
                    break
                }
                definition += `${definitionLine}\n\n`
            }
            definitions.push({
                database,
                databaseId,
                definition,
                word
            })
        }

        // Special case to matches
        if (code == "152") {
            for (const matchLine of responses.slice(responses.indexOf(line) + 1)) {
                if (matchLine == ".") {
                    break
                }
                const [db, match] = matchLine.match(/[\w\-.]+|"(?:\\"|[^"])+"/g) || ["null", "null"]
                definitions.push({
                    database: db,
                    databaseId: db,
                    definition: "",
                    word: match.replaceAll("\"", "")
                })
            }
        }
    }
    return {
        data,
        rawDecoded,
        definitions
    }
}

export async function getDictionaries(server: string, port: number): Promise<DictDatabase[]> {
    const databases: DictDatabase[] = []
    const request = await TCPClient.request({
        host: server,
        port: port,
        messages: ["SHOW DB"]
    })
    const { data } = decodeRawResponse(request.responses)
    for (const line of data) {
        const [id, name] = line.match(/[\w\-.]+|"(?:\\"|[^"])+"/g) || ["null", "null"]
        databases.push({
            id,
            name: name.replaceAll("\"", "")
        })
    }
    return databases
}

export async function getStrategies(server: string, port: number): Promise<DictStrategy[]> {
    const strategies: DictStrategy[] = []
    const request = await TCPClient.request({
        host: server,
        port: port,
        messages: ["SHOW STRAT"]
    })
    const { data } = decodeRawResponse(request.responses)
    for (const line of data) {
        const [id, name] = line.match(/[\w\-.]+|"(?:\\"|[^"])+"/g) || ["null", "null"]
        strategies.push({
            id,
            name: name.replaceAll("\"", "")
        })
    }
    return strategies
}

export async function makeRequest(dictRequest: DictRequest): Promise<{ data: string[], rawDecoded: DictResponseLine[], definitions: DictDefinition[] }> {
    const commands = buildDICTRequests(dictRequest)
    const request = await TCPClient.request({
        host: dictRequest.server,
        port: dictRequest.port,
        messages: commands
    })
    return decodeRawResponse(request.responses, commands)
}

export async function getDictServersAutocomplete(query: string, servers: DictServer[]) {
    const results: DictDefinition[] = []
    for (const server of servers) {
        const request: DictRequest = {
            word: query,
            method: DictRequestType.Match,
            strat: "prefix",
            server: server.host,
            port: server.port,
            database: "*",
            auth: false
        }
        const { definitions } = await makeRequest(request)
        results.push(...definitions.map(def => {
            return {
                ...def,
                server: server.host,
                port: server.port
            }
        }))
    }
    return results
}

export async function getDictServerDefinition(server: DictServer, word: string, database: string) {
    const request: DictRequest = {
        word,
        database,
        method: DictRequestType.Define,
        server: server.host,
        port: server.port,
        auth: false
    }
    return await makeRequest(request)
}
