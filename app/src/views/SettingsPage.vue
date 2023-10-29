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

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar, IonSelect, IonSelectOption} from '@ionic/vue';
</script>

<script lang="ts">

export default {
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

