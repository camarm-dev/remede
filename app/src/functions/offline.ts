import {RemedeDictionaryOption} from "@/functions/types/apiResponses"
import {Directory, Filesystem} from "@capacitor/filesystem"
import {Preferences} from "@capacitor/preferences"
import {Capacitor} from "@capacitor/core"

type DownloadedDictionaryStatus = RemedeDictionaryOption & { path: string, favorite: boolean }

async function getOfflineDictionaryStatus(dictionary: RemedeDictionaryOption) {
    return (await getDownloadedDictionaries()).find(downloadedDictionary => downloadedDictionary.slug == dictionary.slug)
}

async function getDownloadedDictionaries(): Promise<DownloadedDictionaryStatus[]> {
    const dictionaries = JSON.parse((await Preferences.get({ key: "offlineDictionary" })).value || "[]")
    if (dictionaries.length == 0) {
        await Preferences.set({
            key: "offlineDictionary",
            value: JSON.stringify([])
        })
        return []
    }
    return dictionaries as DownloadedDictionaryStatus[]
}


async function downloadDictionary(dictionary: RemedeDictionaryOption) {
    const downloadResponse = await Filesystem.downloadFile({
        path: dictionary.slug,
        url: `https://api-remede.camarm.fr/download?variant=${dictionary.slug}`,
        directory: Directory.Data,
        progress: true
    })

    const offlineDictionary: DownloadedDictionaryStatus = {
        path: downloadResponse.path || "",
        favorite: false,
        ...dictionary
    }

    await Preferences.set({
        key: "offlineDictionary",
        value: JSON.stringify(offlineDictionary)
    })
    return
}

async function deleteDictionary(dictionary: RemedeDictionaryOption) {
    await Preferences.set({
        key: "offlineDictionary",
        value: JSON.stringify({
            "downloaded": false,
            "path": "",
            "hash": "",
            "slug": ""
        })
    })
    await Filesystem.deleteFile({
        path: dictionary.slug,
        directory: Directory.Data
    })
}


async function getRawDictionary(dictionary: RemedeDictionaryOption) {
    if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() === "electron") {
        const file = await Filesystem.readFile({
            path: dictionary.slug + ".db",
            directory: Directory.Data
        })

        const fileData = file.data as Blob

        return await fileData.arrayBuffer().then(buf => new Uint8Array(buf))
    }

    const path = (await getOfflineDictionaryStatus(dictionary))?.path || ""
    const newSrc = Capacitor.convertFileSrc(`${path}`)

    const file = await fetch(newSrc).then(resp => resp.arrayBuffer())

    return new Uint8Array(file)
}

export {
    downloadDictionary,
    deleteDictionary,
    getOfflineDictionaryStatus,
    getDownloadedDictionaries,
    getRawDictionary
}
