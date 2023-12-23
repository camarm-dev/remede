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
      <img src="/og.png" alt="Remède"/>
      <br>
      <br>
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">À propos</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-content class="ion-padding">
        <p>
          Remède est un dictionnaire français libre, construit sur plusieurs services tiers.
        </p>
        <h2>Crédits / Sources</h2>
        <a href="https://labse.camarm.fr" target="_blank">
          <img width="150" alt="Powered by Labse Softwares" src="/labse_powered_by.png" />
        </a>
        <p>
          <a href="https://github.com/camarm-dev/remede#données-remède" target="_blank">Données Remède</a>
          •
          <a href="https://github.com/camarm-dev/remede" target="_blank">Github</a>
          •
          <a href="https://github.com/camarm-dev/remede/blob/main/LICENSE" target="_blank">Licence Remède</a>
        </p>
        <ion-note>Version {{ version }}, build {{ build }} • <a href="https://github.com/camarm-dev/remede/releases" target="_blank">All releases</a></ion-note>
      </ion-content>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar} from '@ionic/vue';
</script>

<script lang="ts">
import { App } from '@capacitor/app';

export default {
  data() {
    return {
      version: ':unavailable:',
      build: ':unavailable:'
    }
  },
  mounted() {
    this.fetchAppInformations()
  },
  methods: {
    async fetchAppInformations() {
      const app = await App.getInfo()
      this.version = app.version
      this.build = app.build
    }
  }
}
</script>
