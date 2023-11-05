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
        <ion-item>
          Dictionnaire <pre>01ffea</pre> téléchargé: 240 562 entrées.
        </ion-item>
      </ion-list>

      <ion-list inset v-else>
        <ion-item :disabled="loading" color="light" @click="loading = true">
          <ion-label>
            <h3>Télécharger le dictionnaire</h3>
          </ion-label>
          <ion-icon slot="end" :icon="cloudDownloadOutline"/>
        </ion-item>
        <ion-item color="light" v-if="loading">
          <ion-label slot="start">
            <p>Téléchargement en cour...</p>
          </ion-label>
          <ion-progress-bar type="indeterminate" color="primary"></ion-progress-bar>
        </ion-item>
      </ion-list>

      <ion-note class="ion-padding" v-if="loading">
        Veuillez ne pas quitter cette page pendant le téléchargement.
      </ion-note>

      <ion-note v-if="!downloaded">
        Télécharger le dictionnaire prendra environ 200Mb de stockage !
      </ion-note>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar, IonSelect, IonSelectOption, IonIcon, IonProgressBar} from '@ionic/vue';
import {cloudDownloadOutline} from "ionicons/icons";
</script>

<script lang="ts">

export default {
  data() {
    return {
      downloaded: false,
      loading: false
    }
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
    }
  }
}
</script>

