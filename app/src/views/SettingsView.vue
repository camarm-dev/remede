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
          <ion-title size="large">Paramètres</ion-title>
        </ion-toolbar>
      </ion-header>

      <div class="list-title">
        Personnalisation
      </div>
      <ion-list inset>
        <ion-item color="light">
          <ion-label>
            <h3>Thème</h3>
          </ion-label>
          <ion-select label="Thème" :value="getCurrentTheme()" placeholder="Clair" @ionChange="handleThemeChangement($event.detail.value)" cancel-text="Annuler" ok-text="Confirmer" interface="action-sheet">
            <ion-select-option value="light">Clair</ion-select-option>
            <ion-select-option value="dark">Sombre</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>
      <ion-list inset>
        <ion-item color="light">
          <ion-label>
            <h3>Langue</h3>
          </ion-label>
          <ion-select label="Langue" :value="getCurrentLang()" placeholder="System" @ionChange="handleLangChangement($event.detail.value)" cancel-text="Annuler" ok-text="Confirmer" interface="action-sheet">
            <ion-select-option v-for="locale in availableLocales" :value="locale" :key="locale">{{ locale }}</ion-select-option>
            <ion-select-option value="system">System</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>

      <br>

      <div class="list-title">
        Dictionnaire hors ligne
      </div>

      <ion-list inset v-if="downloaded">
        <ion-item color="light">
          Dictionnaire "{{ dictionary.hash }}" téléchargé.
        </ion-item>
        <ion-item button color="danger" @click="deleteDictionary().then(() => { reloadDictionaryStatus(); canDownload = true })">
          <ion-icon :icon="trashBinOutline" slot="start"></ion-icon>
          <ion-label>Supprimer</ion-label>
        </ion-item>
        <ion-item v-if="hasUpdate" button color="primary" @click="loading = true; canDownload = true; deleteDictionary().then(() => { reloadDictionaryStatus().then(() => { download() }) })">
          <ion-icon :icon="refreshOutline" slot="start"></ion-icon>
          <ion-label>Mettre à jour vers "{{ latestDictionary }}"</ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset v-else-if="canDownload">
        <ion-item :disabled="loading" color="light" button @click="download()">
          <ion-label>
            Télécharger
          </ion-label>
        </ion-item>
        <ion-item color="light">
          <ion-select @ionChange="dictionaryToDownload = $event.target.value" interface="popover" label="Dictionnaire" value="remede" name="Dictionnaire">
            <ion-select-option :key="key" v-for="key in availableDictionariesName" :value="availableDictionaries[key].slug">{{ availableDictionaries[key].nom }}</ion-select-option>
          </ion-select>
        </ion-item>
        <ion-item color="light" v-if="loading">
          <ion-label>
            <p>Téléchargement en cours...</p>
            <ion-progress-bar type="indeterminate" color="primary"></ion-progress-bar>
          </ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset v-else>
        <ion-item>
          Vous ne pouvez pas télécharger le dictionnaire...
        </ion-item>
      </ion-list>

      <ion-list inset>
        <ion-note class="ion-padding" v-if="loading">
          Veuillez ne pas quitter cette page pendant le téléchargement.

          Il est conseillé de redémarrer l'application après le téléchargement.
        </ion-note>
      </ion-list>

      <ion-list inset v-if="downloaded">
        <ion-note v-if="working" class="ion-padding" color="success">
          <ion-icon :icon="checkmarkCircle"/>
          Tout semble fonctionner parfaitement. Vous pouvez commencer à chercher des mots hors-ligne !
        </ion-note>
        <ion-note v-else class="ion-padding" color="danger">
          <ion-icon :icon="closeCircle"/>
          Un problème a été détecté, veuillez réinstaller le dictionnaire ou contacter le support.
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
import {checkmarkCircle, closeCircle, refreshOutline, trashBinOutline} from "ionicons/icons"
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
import {Device} from "@capacitor/device";

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
        slug: ""
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
    getCurrentTheme() {
      return localStorage.getItem("userTheme") || "light"
    },
    async handleLangChangement(lang: string) {
      if (lang == "system") {
        localStorage.deleteItem("interfaceLanguage")
        this.$i18n.locale = await this.getDeviceLocale()
        return
      }
      localStorage.setItem("interfaceLanguage", lang)
      this.$i18n.locale = lang
    },
    async getDeviceLocale() {
      const locale = await Device.getLanguageCode()
      return locale.value.includes('-') ? locale.value.split('-')[0]: locale.value
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
      this.availableDictionaries = specs.dictionnaires
      this.availableDictionariesName = Object.keys(specs.dictionnaires)

      this.latestDictionary = specs.dataset
      if (this.downloaded) {
        this.hasUpdate = this.dictionary.hash != specs.dictionnaires[this.dictionary.slug].hash
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
          header: "Téléchargement réussi",
          subHeader: "Le dictionnaire hors-ligne a été téléchargé",
          message: "Pour finaliser son installation, veuillez relancer l'application !",
          buttons: [
            {
              text: "C'est compris !",
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
          header: "Échec de téléchargement",
          message: `Le dictionnaire hors-ligne n'a pas pu être téléchargé: ${e}`,
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

