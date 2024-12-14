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
          <ion-title size="large">{{ $t('about') }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-content class="ion-padding">
        <p>
          {{ $t('aboutPage.description') }}
          <a href="https://github.com/camarm-dev/remede" target="_blank">{{ $t('repository') }}</a>.
        </p>
        <p>
          {{ $t('aboutPage.moreInformationCredits') }}
          <a href="https://docs.remede.camarm.fr" target="_blank">docs.remede.camarm.fr</a>.
        </p>
        <ion-list class="border-radius">
          <ion-item color="light" button href="https://github.com/camarm-dev/remede" target="_blank">
            <ion-icon color="medium" slot="start" :icon="logoGithub"/>
            <ion-label>
              Github
            </ion-label>
          </ion-item>
          <ion-item color="light" button id="open-contributors-screen">
            <ion-icon color="medium" slot="start" :icon="heartOutline"/>
            <ion-label>
              {{ $t('aboutPage.contributorsAndDonors') }}
            </ion-label>
          </ion-item>
          <ion-item lines="none" button href="https://ko-fi.com/camarm" target="_blank" :detail="false" class="buy-me-a-coffee">
            <ion-label>
              Donate on Ko-Fi
            </ion-label>
            <ion-avatar>
              <img alt="Ko-Fi logo" src="@/assets/kofi.webp"/>
            </ion-avatar>
          </ion-item>
        </ion-list>
        <ion-modal trigger="open-contributors-screen" :initial-breakpoint="0.6" :breakpoints="[0, 0.6, 0.75, 0.99]">
          <ion-content class="ion-padding">
            <div class="list-title no-margin ion-padding-bottom">
              {{ $t('aboutPage.contributors') }}
            </div>
            <ion-list class="border-radius">
              <ion-item button :detail-icon="atOutline" href="https://github.com/camarm-dev" target="_blank" color="light">
                <ion-avatar aria-hidden="true" slot="start">
                  <img alt="Photo de profil de camarm" src="https://avatars.githubusercontent.com/u/77529508?s=88&v=4" />
                </ion-avatar>
                <ion-label>
                  <h2>camarm</h2>
                  <p>{{ $t('aboutPage.maintainer') }}</p>
                </ion-label>
              </ion-item>
              <ion-item lines="none" button :detail-icon="atOutline" href="https://github.com/labsesoftware" target="_blank" color="light">
                <ion-avatar aria-hidden="true" slot="start">
                  <img alt="Photo de profil de Labse Software" src="@/assets/labse.png" />
                </ion-avatar>
                <ion-label>
                  <h2>Labse Software</h2>
                  <p>{{ $t('aboutPage.contributors') }}</p>
                </ion-label>
              </ion-item>
            </ion-list>
<!--            <div class="list-title no-margin ion-padding-bottom">-->
<!--              Donateurs-->
<!--            </div>-->
<!--            <ion-note>Pas encore de donateurs, soyez le premier !</ion-note>-->
            <div class="list-title no-margin ion-padding-bottom">
              {{ $t('credits') }}
            </div>
            <ion-list class="border-radius">
              <ion-item color="light" button href="https://github.com/camarm-dev/remede/blob/main/LICENSE" target="_blank">
                <ion-icon :icon="documentAttachOutline" slot="start" color="medium"/>
                <ion-label>
                  {{ $t('license') }}
                </ion-label>
              </ion-item>
              <ion-item lines="none" color="light" button href="https://docs.remede.camarm.fr/docs/database/credits" target="_blank">
                <ion-icon :icon="fingerPrintOutline" slot="start" color="medium"/>
                <ion-label>
                  {{ $t('remedeData') }}
                </ion-label>
              </ion-item>
            </ion-list>
          </ion-content>
        </ion-modal>
        <br>
        <ion-note>Version {{ version }}, build {{ build }} • <a href="https://github.com/camarm-dev/remede/releases" target="_blank">All releases</a></ion-note>
      </ion-content>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar, IonModal, IonItem, IonList, IonLabel, IonIcon, IonAvatar, IonNote} from "@ionic/vue"
import {atOutline, documentAttachOutline, fingerPrintOutline, heartOutline, logoGithub} from "ionicons/icons"
</script>

<script lang="ts">
import { App } from "@capacitor/app"

export default {
  data() {
    return {
      version: "1.4.0-beta",
      build: "tauri-2"
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
<style>
.border-radius {
  border-radius: 12px;
}

.buy-me-a-coffee::part(native) {
  background: #ff5f5f;
  color: var(--ion-color-light);
}
</style>
