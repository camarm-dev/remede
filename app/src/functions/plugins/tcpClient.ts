import {Capacitor, registerPlugin} from "@capacitor/core"

const isAndroid = Capacitor?.getPlatform() == "android"

export interface TCPClientPlugin {
    request(options: { host: string, port: number, messages: string[] }): Promise<{ responses: string[] }>;
}

// We use native fetch if platform is android. If not, we send DICT requests through the Remède DICT server proxy
const TCPClient = isAndroid ? registerPlugin<TCPClientPlugin>("TCPClient") : {
    async request(options: { host: string, port: number, messages: string[] }): Promise<{ responses: string[] }> {
        return {
            responses: await fetch("https://api-remede.camarm.fr/proxy/dict", {
                method: "POST",
                body: JSON.stringify({
                    server: options.host,
                    port: options.port,
                    commands: options.messages
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
        }
    }
}

export default TCPClient
