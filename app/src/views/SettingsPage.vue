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

      <ion-list inset>
        <ion-item color="light">
          <ion-label>
            <h3>Thème</h3>
          </ion-label>
          <ion-select :value="getCurrentTheme()" placeholder="Clair" @ionChange="handleThemeChangement($event.detail.value)" cancel-text="Annuler" ok-text="Confirmer" interface="action-sheet">
            <ion-select-option value="light">Clair</ion-select-option>
            <ion-select-option value="dark">Sombre</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>

      <br>

      <ion-list inset v-if="downloaded">
        <ion-item color="light">
          Dictionnaire "{{ dictionary.hash }}" téléchargé.
        </ion-item>
        <ion-item button color="danger" @click="deleteDictionary(); reloadDictionaryStatus()">
          <ion-icon :icon="trashBinOutline" slot="start"></ion-icon>
          <ion-label>Supprimer</ion-label>
        </ion-item>
        <ion-item v-if="hasUpdate" button color="primary" @click="loading = true; deleteDictionary(); reloadDictionaryStatus(); downloadDictionary()">
          <ion-icon :icon="refreshOutline" slot="start"></ion-icon>
          <ion-label>Mettre à jour vers "{{ latestDictionary }}"</ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset v-else-if="canDownload">
        <ion-item :disabled="loading" color="light" @click="download()">
          <ion-label>
            <h3>Télécharger le dictionnaire</h3>
          </ion-label>
          <ion-icon slot="end" :icon="cloudDownloadOutline"/>
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
        <ion-note class="ion-padding" v-if="!downloaded && canDownload && !loading">
          Télécharger le dictionnaire prendra environ 205Mb de stockage !
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
} from '@ionic/vue';
import {cloudDownloadOutline, refreshOutline, trashBinOutline} from "ionicons/icons";
import {deleteDictionary} from "@/functions/offline";
</script>

<script lang="ts">

import {downloadDictionary, getOfflineDictionaryStatus} from "@/functions/offline";
import {ProgressStatus} from "@capacitor/filesystem";
import {Capacitor} from "@capacitor/core";
import {toastController} from "@ionic/vue";
import {InformationsResponse} from "@/functions/types/api_responses";

export default {
  data() {
    return {
      canDownload: false,
      downloaded: false,
      loading: false,
      latestDictionary: '',
      hasUpdate: false,
      dictionary: {
        hash: ''
      }
    }
  },
  mounted() {
    this.reloadDictionaryStatus()
  },
  methods: {
    handleThemeChangement(theme: string) {
      localStorage.setItem('userTheme', theme)
      document.body.classList.remove('dark')
      document.body.classList.remove('light')
      document.body.classList.add(theme)
    },
    getCurrentTheme() {
      return localStorage.getItem('userTheme') || 'light'
    },
    async reloadDictionaryStatus() {
      const status = await getOfflineDictionaryStatus()
      this.dictionary = status
      this.downloaded = status.downloaded

      if (!this.isWeb()) {
        this.canDownload = true
      }
      if (this.downloaded) {
        this.canDownload = false
      }

      const specs = await fetch('https://api-remede.camarm.fr').then(resp => resp.json()) as InformationsResponse
      this.latestDictionary = specs.dataset
      this.hasUpdate = this.dictionary.hash != specs.dataset
    },
    isWeb() {
      return false
    },
    async download() {
      this.loading = true
      try {
        await downloadDictionary()
      } catch (e) {
        const message = await toastController.create({
          header: 'Échec de téléchargement',
          message: `Le dictionnaire hors-ligne n'a pas pu être téléchargé: ${e}`,
          duration: 5000,
          color: 'danger'
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
</style>

