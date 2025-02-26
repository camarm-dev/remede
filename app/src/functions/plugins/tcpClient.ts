import { registerPlugin } from "@capacitor/core"

export interface TCPClientPlugin {
    request(options: { host: string, port: number, messages: string[] }): Promise<{ responses: string[] }>;
}

const TCPClient = registerPlugin<TCPClientPlugin>("TCPClient")

export default TCPClient
