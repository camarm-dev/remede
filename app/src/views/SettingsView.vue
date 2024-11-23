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

      <div class="list-title">
        {{ $t('settingsPage.offlineDictionary') }}
      </div>

      <ion-list inset v-if="downloaded">
        <ion-item color="light">
          {{ $t('dictionary') }} "{{ dictionary.name }}" {{ $t('settingsPage.downloaded') }}.
        </ion-item>
        <ion-item button color="danger" @click="deleteDictionary().then(() => { reloadDictionaryStatus(); canDownload = true })">
          <ion-icon :icon="trashBinOutline" slot="start"></ion-icon>
          <ion-label>{{ $t('delete') }}</ion-label>
        </ion-item>
        <ion-item v-if="hasUpdate" button color="primary" @click="loading = true; canDownload = true; deleteDictionary().then(() => { reloadDictionaryStatus().then(() => { download() }) })">
          <ion-icon :icon="refreshOutline" slot="start"></ion-icon>
          <ion-label>{{ $t('settingsPage.updateTo') }} "{{ latestDictionary }}"</ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset v-if="downloaded">
        <ion-item>
          <ion-note>
            {{ $t('settingsPage.dictionaryRevisionDownloaded', { name: dictionary.name, rev: dictionary.hash, size: dictionary.size, words: dictionary.words }) }}
          </ion-note>
        </ion-item>
      </ion-list>

      <ion-list inset v-else-if="canDownload">
        <ion-item :disabled="loading" color="light" button @click="download()">
          <ion-label>
            {{ $t('settingsPage.download') }}
          </ion-label>
        </ion-item>
        <ion-item color="light">
          <ion-select @ionChange="dictionaryToDownload = $event.target.value" interface="alert" :label="$t('dictionary')" value="remede" :name="$t('dictionary')">
            <ion-select-option :key="key" v-for="key in availableDictionariesName" :value="availableDictionaries[key].slug">{{ availableDictionaries[key].name }} {{ availableDictionaries[key].size }}</ion-select-option>
          </ion-select>
        </ion-item>
        <ion-item color="light" v-if="loading">
          <ion-label>
            <p>{{ $t('settingsPage.downloading') }}</p>
            <ion-progress-bar type="indeterminate" color="primary"></ion-progress-bar>
          </ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset v-else>
        <ion-item>
          {{ $t('settingsPage.cannotDownload') }}
        </ion-item>
      </ion-list>

      <ion-list inset>
        <ion-note class="ion-padding" v-if="loading">
          {{ $t('settingsPage.downloadingDisclaimer') }}
        </ion-note>
      </ion-list>

      <ion-list inset v-if="downloaded">
        <ion-note v-if="working" class="ion-padding" color="success">
          <ion-icon :icon="checkmarkCircle"/>
          {{ $t('settingsPage.workingNormally') }}
        </ion-note>
        <ion-note v-else class="ion-padding" color="danger">
          <ion-icon :icon="closeCircle"/>
          {{ $t('settingsPage.problemDetected') }}
        </ion-note>
      </ion-list>

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
  IonList
} from "@ionic/vue"
import {
  checkmarkCircle,
  closeCircle, contrastOutline,
  languageOutline,
  refreshOutline,
  trashBinOutline
} from "ionicons/icons"
import {deleteDictionary} from "@/functions/offline"
</script>

<script lang="ts">

import {downloadDictionary, getOfflineDictionaryStatus} from "@/functions/offline"
import {alertController, toastController} from "@ionic/vue"
import {InformationsResponse, RemedeAvailableDictionaries} from "@/functions/types/apiResponses"
import {App} from "@capacitor/app"
import {Capacitor} from "@capacitor/core"
import {getWordDocument} from "@/functions/dictionnary"
import {RemedeWordDocument} from "@/functions/types/remede"
import {getDeviceLocale} from "@/functions/device"
import locales from "@/functions/locales"

export default {
  data() {
    return {
      canDownload: true,
      downloaded: false,
      loading: false,
      latestDictionary: "",
      hasUpdate: false,
      dictionaryToDownload: "remede",
      dictionary: {
        hash: "",
        slug: "",
        name: "",
        words: ""
      },
      availableDictionaries: {} as RemedeAvailableDictionaries,
      availableDictionariesName: [] as string[],
      working: true,
      availableLocales: this.$i18n.availableLocales
    }
  },
  mounted() {
    this.reloadDictionaryStatus().then(async () => {
      if (this.downloaded) {
        try {
          const word = await getWordDocument("remède") as RemedeWordDocument
          if (word.ipa != "/ʁəmɛd/") {
            throw "Database is wrong"
          }
          this.working = true
        } catch {
          this.working = false
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
    getLocaleName(locale: string) {
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
      const status = await getOfflineDictionaryStatus()
      this.dictionary = status
      this.downloaded = status.downloaded

      if (this.downloaded) {
        this.canDownload = false
      }

      const specs = await fetch("https://api-remede.camarm.fr").then(resp => resp.json()) as InformationsResponse
      this.availableDictionaries = specs.dictionaries
      this.availableDictionariesName = Object.keys(specs.dictionaries)

      this.latestDictionary = specs.dataset
      if (this.downloaded) {
        this.hasUpdate = this.dictionary.hash != specs.dictionaries[this.dictionary.slug].hash
      } else {
        this.hasUpdate = false
      }
    },
    async closeApp() {
      if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() === "electron") {
        location.reload()
        return
      }
      await App.exitApp()
    },
    async download() {
      this.loading = true
      try {
        await downloadDictionary(this.availableDictionaries[this.dictionaryToDownload])
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
</style>

