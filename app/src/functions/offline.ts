import {RemedeDictionaryOption} from "@/functions/types/apiResponses"
import {Directory, Filesystem} from "@capacitor/filesystem"
import {Preferences} from "@capacitor/preferences"
import {Capacitor} from "@capacitor/core"

async function getOfflineDictionaryStatus() {
    const status = JSON.parse((await Preferences.get({ key: "offlineDictionary" })).value || "{}")
    if (JSON.stringify(status) == "{}") {
        await Preferences.set({
            key: "offlineDictionary",
            value: JSON.stringify({
                "downloaded": false,
                "path": "",
                "hash": "",
                "slug": "",
                "name": ""
            })
        })
        return {
            downloaded: false,
            hash: "",
            slug: "",
            name: ""
        }
    }
    return status
}


async function downloadDictionary(dictionary: RemedeDictionaryOption) {
    const downloadResponse = await Filesystem.downloadFile({
        path: "remedeSQLite.db",
        url: `https://api-remede.camarm.fr/download?variant=${dictionary.slug}`,
        directory: Directory.Data,
        progress: true
    })

    const offlineDictionary = {
        downloaded: true,
        path: downloadResponse.path,
        hash: dictionary.hash,
        slug: dictionary.slug,
        name: dictionary.name
    }

    await Preferences.set({
        key: "offlineDictionary",
        value: JSON.stringify(offlineDictionary)
    })
    return
}

async function deleteDictionary() {
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
        path: "remedeSQLite.db",
        directory: Directory.Data
    })
}


async function getRawDictionary() {
    if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() === "electron") {
        const file = await Filesystem.readFile({
            path: "remedeSQLite.db",
            directory: Directory.Data
        })

        const fileData = file.data as Blob

        return await fileData.arrayBuffer().then(buf => new Uint8Array(buf))
    }

    const path = (await getOfflineDictionaryStatus()).path
    const newSrc = Capacitor.convertFileSrc(`${path}`)

    const file = await fetch(newSrc).then(resp => resp.arrayBuffer())

    return new Uint8Array(file)
}

export {
    downloadDictionary,
    deleteDictionary,
    getOfflineDictionaryStatus,
    getRawDictionary
}
