import {Device} from "@capacitor/device";

export async function getDeviceLocale() {
    const locale = await Device.getLanguageCode()
    return locale.value.includes('-') ? locale.value.split('-')[0]: locale.value
}
