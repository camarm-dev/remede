<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">{{ $t('settings') }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <div class="list-title">
        {{ $t('settingsPage.personalization') }}
      </div>
      <ion-list inset>
        <ion-item color="light">
          <ion-icon slot="start" :icon="contrastOutline"/>
          <ion-select :label="$t('settingsPage.theme')" :value="getCurrentTheme()" :placeholder="$t('settingsPage.lightTheme')" @ionChange="handleThemeChangement($event.detail.value)" :cancel-text="$t('cancel')" :ok-text="$t('confirm')" interface="action-sheet">
            <ion-select-option value="light">{{ $t('settingsPage.lightTheme') }}</ion-select-option>
            <ion-select-option value="dark">{{ $t('settingsPage.darkTheme') }}</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>
      <ion-list inset>
        <ion-item color="light">
          <ion-icon slot="start" :icon="languageOutline"/>
          <ion-select :label="$t('settingsPage.tongue')" :value="getCurrentLang()" placeholder="System" @ionChange="handleLangChangement($event.detail.value)" :cancel-text="$t('cancel')" :ok-text="$t('confirm')" interface="action-sheet">
            <ion-select-option v-for="locale in availableLocales" :value="locale" :key="locale">{{ getLocaleName(locale) }}</ion-select-option>
            <ion-select-option value="system">System</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>

      <br>

      <div class="list-title" v-if="canDownload">
        {{ $t('settingsPage.offlineDictionary') }}
      </div>

      <ion-list inset v-if="canDownload">
        <ion-item :disabled="loading" color="light" button @click="download(dictionaryToDownload)">
          <ion-label>
            {{ $t('settingsPage.download') }}
          </ion-label>
        </ion-item>
        <ion-item color="light">
          <ion-select :value="dictionaryToDownload" @ionChange="dictionaryToDownload = $event.target.value" interface="alert" :label="$t('dictionary')" :name="$t('dictionary')">
            <ion-select-option :key="key" v-for="key in availableDictionariesName" :value="availableDictionaries[key]">{{ availableDictionaries[key].name }} {{ availableDictionaries[key].size }}</ion-select-option>
          </ion-select>
        </ion-item>
        <ion-item color="light" v-if="loading">
          <ion-label>
            <p>{{ $t('settingsPage.downloading') }}</p>
            <ion-progress-bar type="indeterminate" color="primary"></ion-progress-bar>
          </ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset v-if="loading">
        <ion-note class="ion-padding">
          {{ $t('settingsPage.downloadingDisclaimer') }}
        </ion-note>
      </ion-list>

      <div class="list-title" v-if="downloaded">
        {{ $t('settingsPage.myDictionaries') }}
      </div>

      <div v-for="dictionary in downloadedDictionaries" :key="dictionary.slug">
        <ion-list inset class="mb-1">
          <ion-item color="light">
            {{ $t('dictionary') }} "{{ dictionary.name }}" {{ $t('settingsPage.downloaded') }}.
            <ion-icon @click="setFavoriteDictionary(dictionary).then(() => reloadDictionaryStatus())" :icon="dictionary.favorite ? heart : heartOutline" slot="end"></ion-icon>
          </ion-item>
          <ion-item button color="light" :id="`status-dict-${dictionary.slug}`" v-if="dictionariesWorking[dictionary.slug]">
            <ion-icon color="success" :icon="checkmarkCircle" slot="start"/>
            <ion-note v-if="dictionariesWorking[dictionary.slug]" color="success">
              {{ $t('settingsPage.working') }}
            </ion-note>
            <ion-alert :header="dictionariesWorking[dictionary.slug] ? $t('settingsPage.working') : $t('settingsPage.problem')" :message="dictionariesWorking[dictionary.slug] ? $t('settingsPage.workingNormally') : $t('settingsPage.problemDetected')" :trigger="`status-dict-${dictionary.slug}`"></ion-alert>
          </ion-item>
          <ion-item color="light" v-else-if="dictionariesWorking[dictionary.slug] === undefined">
            <ion-spinner slot="start" color="medium" name="crescent"></ion-spinner>
            <ion-note color="medium">
              {{ $t('settingsPage.loading') }}
            </ion-note>
          </ion-item>
          <ion-item button color="light" :id="`status-dict-${dictionary.slug}`" v-else>
            <ion-icon color="danger" :icon="closeCircle" slot="start"/>
            <ion-note color="danger">
              {{ $t('settingsPage.problem') }}
            </ion-note>
            <ion-alert :header="dictionariesWorking[dictionary.slug] ? $t('settingsPage.working') : $t('settingsPage.problem')" :message="dictionariesWorking[dictionary.slug] ? $t('settingsPage.workingNormally') : $t('settingsPage.problemDetected')" :trigger="`status-dict-${dictionary.slug}`"></ion-alert>
          </ion-item>
          <ion-item button color="danger" @click="deleteDictionary(dictionary).then(() => { reloadDictionaryStatus(); canDownload = true })">
            <ion-icon :icon="trashBinOutline" slot="start"></ion-icon>
            <ion-label>{{ $t('delete') }}</ion-label>
          </ion-item>
          <ion-item v-if="canBeUpdatedDictionaries.includes(dictionary.slug)" button color="primary" @click="loading = true; canDownload = true; deleteDictionary(dictionary).then(() => { reloadDictionaryStatus().then(() => { download(dictionary) }) })">
            <ion-icon :icon="refreshOutline" slot="start"></ion-icon>
            <ion-label>{{ $t('settingsPage.updateTo') }} "{{ latestDictionary }}"</ion-label>
          </ion-item>
        </ion-list>
<!--   Adding v-if to trigger refresh     -->
        <ion-list inset>
          <ion-item lines="none">
            <ion-note>
              {{ $t('settingsPage.dictionaryRevisionDownloaded', { name: dictionary.name, rev: dictionary.hash, size: dictionary.size, words: dictionary.total }) }}
            </ion-note>
          </ion-item>
        </ion-list>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonMenuButton,
  IonPage,
  IonProgressBar,
  IonSelect,
  IonSelectOption,
  IonTitle,
  IonToolbar,
  IonItem,
  IonLabel,
  IonNote,
  IonList,
  IonAlert,
  IonSpinner
} from "@ionic/vue"
import {
  checkmarkCircle,
  closeCircle, contrastOutline,
  languageOutline,
  refreshOutline,
  trashBinOutline,
  heartOutline,
  heart
} from "ionicons/icons"
import {deleteDictionary, setFavoriteDictionary} from "@/functions/offline"
</script>

<script lang="ts">

import {downloadDictionary, getDownloadedDictionaries, DownloadedDictionaryStatus} from "@/functions/offline"
import {alertController, toastController} from "@ionic/vue"
import {InformationsResponse, RemedeAvailableDictionaries, RemedeDictionaryOption} from "@/functions/types/apiResponses"
import {App} from "@capacitor/app"
import {Capacitor} from "@capacitor/core"
import {getAutocomplete, setDictionary} from "@/functions/dictionnary"
import {getDeviceLocale} from "@/functions/device"
import locales, {localeCode} from "@/functions/locales"

export default {
  data() {
    return {
      canDownload: true,
      downloaded: false,
      loading: false,
      latestDictionary: "",
      canBeUpdatedDictionaries: [] as string[],
      dictionaryToDownload: {} as RemedeDictionaryOption,
      downloadedDictionaries: [] as DownloadedDictionaryStatus[],
      availableDictionaries: {} as RemedeAvailableDictionaries,
      availableDictionariesName: [] as string[],
      dictionariesWorking: {} as { [key: string]: boolean },
      availableLocales: this.$i18n.availableLocales as any[] as localeCode[]
    }
  },
  mounted() {
    this.reloadDictionaryStatus().then(async () => {
      if (this.downloaded) {
        for (const downloadedDictionary of this.downloadedDictionaries) {
          try {
            await setDictionary(downloadedDictionary)
            const results = await getAutocomplete("a")
            if (results.length != 5) {
              throw "Database is wrong"
            }
            this.dictionariesWorking[downloadedDictionary.slug] = true
          } catch {
            this.dictionariesWorking[downloadedDictionary.slug] = false
          }
        }
      }
    })
  },
  methods: {
    handleThemeChangement(theme: string) {
      localStorage.setItem("userTheme", theme)
      document.body.classList.remove("dark")
      document.body.classList.remove("light")
      document.body.classList.add(theme)
    },
    getLocaleName(locale: localeCode) {
      return locales[locale] || locale
    },
    getCurrentTheme() {
      return localStorage.getItem("userTheme") || "light"
    },
    async handleLangChangement(lang: string) {
      if (lang == "system") {
        localStorage.removeItem("interfaceLanguage")
        this.$i18n.locale = await getDeviceLocale()
        return
      }
      localStorage.setItem("interfaceLanguage", lang)
      this.$i18n.locale = lang
    },
    getCurrentLang() {
      return localStorage.getItem("interfaceLanguage") || "system"
    },
    async reloadDictionaryStatus() {
      const downloadedDictionaries = await getDownloadedDictionaries()
      this.downloadedDictionaries = downloadedDictionaries
      this.downloaded = downloadedDictionaries.length > 0

      const specs = await fetch("https://api-remede.camarm.fr").then(resp => resp.json()) as InformationsResponse
      this.availableDictionaries = specs.dictionaries
      this.availableDictionariesName = Object.keys(this.availableDictionaries).filter(dictionary => !dictionary.includes("legacy"))
      if (this.availableDictionariesName.length > 0) {
        this.dictionaryToDownload = this.availableDictionaries[this.availableDictionariesName[0]]
      }

      if (this.downloadedDictionaries.length == this.availableDictionariesName.length) {
        this.canDownload = false
      }
      // Excluding downloaded dicts from downloadable dicts
      this.availableDictionariesName = this.availableDictionariesName.filter(dictionary => !downloadedDictionaries.some(downloadedDictionary => downloadedDictionary.slug == dictionary))

      this.latestDictionary = specs.dataset
      for (const downloadedDictionary of downloadedDictionaries) {
        if (downloadedDictionary.hash != specs.dictionaries[downloadedDictionary.slug].hash) {
          this.canBeUpdatedDictionaries.push(downloadedDictionary.slug)
        }
      }
    },
    async closeApp() {
      if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() === "electron") {
        location.reload()
        return
      }
      await App.exitApp()
    },
    async download(dictionary: RemedeDictionaryOption) {
      this.loading = true
      try {
        await downloadDictionary(dictionary)
        const successMessage = await alertController.create({
          header: this.$t("settingsPage.downloadSuccess"),
          subHeader: this.$t("settingsPage.downloadDescription"),
          message: this.$t("settingsPage.downloadLongDescription"),
          buttons: [
            {
              text: this.$t("settingsPage.understood"),
              role: "confirm",
              handler: async () => {
                await this.closeApp()
              },
            },
          ]
        })

        await successMessage.present()
      } catch (e) {
        const message = await toastController.create({
          header: this.$t("settingsPage.downloadFailed"),
          message: this.$t("settingsPage.downloadFailedDescription", { error: e }),
          duration: 5000,
          color: "danger"
        })

        await message.present()
      }

      this.loading = false
      await this.reloadDictionaryStatus()
    }
  }
}
</script>
<style scoped>
ion-label ion-progress-bar {
  margin-top: 8px;
}

ion-note.ion-padding {
  display: block;
}

.mb-1 {
  margin-bottom: 5x;
}
</style>

