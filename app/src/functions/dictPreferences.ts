import {Preferences} from "@capacitor/preferences"
import {DictServer} from "@/functions/dictProtocol"
import dictServers from "@/data/dictServers.json"

export type DictServerPreferences = {
    enabled: boolean
    enabledDicts: string[]
}

export function getDictServerId(server: DictServer) {
    return server.host + server.port.toString() + "-" + server.name.replaceAll(" ", "").trim().toLowerCase()
}

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
    const toDelete = savedServers.find(el => getDictServerId(el) === getDictServerId(server))
    if (toDelete) {
        savedServers.splice(savedServers.indexOf(toDelete), 1)
        await Preferences.set({
            key: "savedDictServers",
            value: JSON.stringify(savedServers)
        })
    }
}

export async function getDictServerPreferences(): Promise<DictServerPreferences> {
    const response = await Preferences.get({
        key: "dictServerPreferences"
    })
    const preferences = JSON.parse(response.value || "false")
    if (!preferences) {
        const defaultPreferences: DictServerPreferences = {
            enabled: false,
            enabledDicts: []
        }
        await Preferences.set({
            key: "dictServerPreferences",
            value: JSON.stringify(defaultPreferences)
        })
        return await getDictServerPreferences()
    }
    return preferences
}

export async function toggleDictServer(server: DictServer) {
    const preferences = await getDictServerPreferences()
    const serverId = getDictServerId(server)
    if (preferences.enabledDicts.includes(serverId)) {
        preferences.enabledDicts.splice(preferences.enabledDicts.indexOf(serverId), 1)
    } else {
        preferences.enabledDicts.push(serverId)
    }
    await Preferences.set({
        key: "dictServerPreferences",
        value: JSON.stringify(preferences)
    })
}

export async function toggleDictServerSearch() {
    const preferences = await getDictServerPreferences()
    preferences.enabled = !preferences.enabled
    await Preferences.set({
        key: "dictServerPreferences",
        value: JSON.stringify(preferences)
    })
}

export async function getEnabledDictServers(): Promise<DictServer[] | undefined> {
    const preferences = await getDictServerPreferences()
    if (!preferences.enabled)
        return undefined
    const allDictServers: DictServer[] = [
        ...await getSavedDictServers(),
        ...dictServers
    ]
    return allDictServers.filter(server => preferences.enabledDicts.includes(getDictServerId(server)))
}
