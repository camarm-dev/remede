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
          <ion-title size="large">Fiches</ion-title>
        </ion-toolbar>
        <ion-toolbar>
          <ion-searchbar disabled placeholder="Rechercher une fiche"></ion-searchbar>
          <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
        </ion-toolbar>
      </ion-header>

      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content></ion-refresher-content>
      </ion-refresher>

      <ion-note class="ion-padding ion-float-end" v-if="failed">Fonctionne seulement avec une connexion internet !</ion-note>
      <ion-nav-link router-direction="forward" :component="FicheModal" :component-props="sheet" v-for="sheet in sheets">
        <ion-list inset>
          <ion-item button color="light" lines="none">
            <ion-label>
              <h1>{{ sheet.nom }}</h1>
              <p>{{ sheet.description }}</p>
              <ion-badge class="ion-margin-end" :color="getTagColor(tag)" v-for="tag in sheet.tags">{{ tag }}</ion-badge>
            </ion-label>
          </ion-item>
        </ion-list>
      </ion-nav-link>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonMenuButton,
  IonPage,
  IonTitle,
  IonToolbar,
  IonSpinner,
  IonItem,
  IonLabel,
  IonList,
  IonBadge, IonNavLink, IonProgressBar, IonSearchbar
} from '@ionic/vue';
import FicheModal from "@/components/FicheModal.vue";
</script>

<script lang="ts">
export default {
  data() {
    return {
      loading: true,
      failed: false,
      sheets: []
    }
  },
  mounted() {
    this.loadSheets()
  },
  methods: {
    async loadSheets() {
      this.loading = true
      try {
        this.sheets = await fetch('https://api-remede.camarm.fr/sheets').then(resp => resp.json())
        this.failed = false
      } catch {
        this.failed = true
      }
      this.loading = false
    },
    getTagColor(tag: string) {
      switch (tag) {
        case 'orthographe':
          return 'primary'
        case 'grammaire':
          return 'success'
        case 'lexique':
          return 'tertiary'
        case 'conjugaison':
          return 'secondary'
        case 'style':
          return 'warning'
        case 'typographie':
          return 'danger'
        default:
          return 'grey'
      }
    },
    handleRefresh(event: CustomEvent) {
      this.loadSheets().then(() => {
        event.target.complete()
      })
    }
  }
}
</script>
