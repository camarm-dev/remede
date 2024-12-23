import {RemedeDictionaryOption} from "@/functions/types/apiResponses"
import {Directory, Filesystem} from "@capacitor/filesystem"
import {Preferences} from "@capacitor/preferences"
import {Capacitor} from "@capacitor/core"

type DownloadedDictionaryStatus = RemedeDictionaryOption & { path: string, favorite: boolean }

async function setFavoriteDictionary(dictionary: RemedeDictionaryOption) {
    const dictionaries = await getDownloadedDictionaries()
    for (const downloadedDictionary of dictionaries) {
        downloadedDictionary.favorite = downloadedDictionary.slug == dictionary.slug
    }
    await Preferences.set({
        key: "offlineDictionaries",
        value: JSON.stringify(dictionaries)
    })
}

async function getOfflineDictionaryStatus(dictionary: RemedeDictionaryOption) {
    return (await getDownloadedDictionaries()).find(downloadedDictionary => downloadedDictionary.slug == dictionary.slug)
}

async function getDownloadedDictionaries(): Promise<DownloadedDictionaryStatus[]> {
    const dictionaries = JSON.parse((await Preferences.get({ key: "offlineDictionaries" })).value || "[]")
    if (dictionaries.length == 0) {
        await Preferences.set({
            key: "offlineDictionaries",
            value: JSON.stringify([])
        })
        return []
    }
    return dictionaries as DownloadedDictionaryStatus[]
}

async function downloadDictionary(dictionary: RemedeDictionaryOption) {
    const downloadResponse = await Filesystem.downloadFile({
        path: dictionary.slug + ".db",
        url: `https://api-remede.camarm.fr/download?variant=${dictionary.slug}`,
        directory: Directory.Data,
        progress: true
    })

    const offlineDictionary: DownloadedDictionaryStatus = {
        path: downloadResponse.path || "",
        favorite: false,
        ...dictionary
    }

    const downloadedDictionaries = await getDownloadedDictionaries()
    downloadedDictionaries.push(offlineDictionary)

    await Preferences.set({
        key: "offlineDictionaries",
        value: JSON.stringify(downloadedDictionaries)
    })
    return
}

async function deleteDictionary(dictionary: RemedeDictionaryOption) {
    const dictionaries = await getDownloadedDictionaries()
    const toDeleteIndex = dictionaries.findIndex(element => element.slug == dictionary.slug)
    dictionaries.splice(toDeleteIndex, 1)
    await Preferences.set({
        key: "offlineDictionaries",
        value: JSON.stringify(dictionaries)
    })
    await Filesystem.deleteFile({
        path: dictionary.slug + ".db",
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
    setFavoriteDictionary,
    downloadDictionary,
    deleteDictionary,
    getOfflineDictionaryStatus,
    getDownloadedDictionaries,
    getRawDictionary
}
