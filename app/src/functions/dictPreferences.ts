import {Preferences} from "@capacitor/preferences"
import {DictServer} from "@/functions/dictProtocol"

export async function getSavedDictServers(): Promise<DictServer[]> {
    const response = await Preferences.get({
        key: "savedDictServers"
    })
    return JSON.parse(response.value || "[]")
}

export async function addServer(server: DictServer) {
    const savedServers = await getSavedDictServers()
    savedServers.push(server)
    await Preferences.set({
        key: "savedDictServers",
        value: JSON.stringify(savedServers)
    })
}


export async function deleteServer(server: DictServer) {
    const savedServers = await getSavedDictServers()
    const toDelete = savedServers.find(el => el === server)
    if (toDelete) {
        savedServers.splice(savedServers.indexOf(toDelete), 1)
        await Preferences.set({
            key: "savedDictServers",
            value: JSON.stringify(savedServers)
        })
    }
}
