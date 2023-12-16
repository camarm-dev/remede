import {InformationsResponse} from "@/functions/types/api_responses";
import {Directory, Filesystem} from '@capacitor/filesystem'
import {Preferences} from '@capacitor/preferences'
import {Capacitor} from "@capacitor/core";

async function getOfflineDictionaryStatus() {
    const status = JSON.parse((await Preferences.get({ key: 'offlineDictionary' })).value || '{}')
    if (JSON.stringify(status) == '{}') {
        await Preferences.set({
            key: 'offlineDictionary',
            value: JSON.stringify({
                'downloaded': false,
                'path': '',
                'hash': ''
            })
        })
        return {
            downloaded: false,
            hash: ''
        }
    }
    return status
}


async function downloadDictionary() {
    const datasetInformations = await fetch('https://api-remede.camarm.fr').then(resp => resp.json()) as InformationsResponse

    const downloadResponse = await Filesystem.downloadFile({
        path: "remedeSQLite.db",
        url: 'https://api-remede.camarm.fr/download',
        directory: Directory.Data,
        progress: true
    })

    const offlineDictionary = {
        downloaded: true,
        path: downloadResponse.path,
        hash: datasetInformations.dataset
    }

    await Preferences.set({
        key: 'offlineDictionary',
        value: JSON.stringify(offlineDictionary)
    })
    return
}

async function deleteDictionary() {
    await Preferences.set({
        key: 'offlineDictionary',
        value: JSON.stringify({
            'downloaded': false,
            'path': '',
            'hash': ''
        })
    })
    await Filesystem.deleteFile({
        path: 'remedeSQLite.db',
        directory: Directory.Data
    })
}


async function getRawDictionary() {
    if (!Capacitor.isNativePlatform()) {
        const file = await Filesystem.readFile({
            path: 'remedeSQLite.db',
            directory: Directory.Data
        })

        return await file.data.arrayBuffer().then(buf => new Uint8Array(buf))
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
