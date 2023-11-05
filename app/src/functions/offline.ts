import {InformationsResponse} from "@/functions/types/api_responses";
import {Filesystem} from '@capacitor/filesystem'
import {Preferences} from '@capacitor/preferences'

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


async function downloadDictionary(progressListener: Function) {
    const datasetInformations = await fetch('https://api-remede.camarm.fr').then(resp => resp.json()) as InformationsResponse

    addEventListener('progress', (progress) => { progressListener(progress) })

    const downloadResponse = await Filesystem.downloadFile({
        path: "remedeSQLite.db",
        url: 'https://api-remede.camarm.fr/download',
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

export {
    downloadDictionary,
    getOfflineDictionaryStatus
}
