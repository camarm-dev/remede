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
      </ion-header>

      <ion-note v-if="failed">Fonctionne seulement avec une connexion internet !</ion-note>
      <ion-item v-if="loading">
        <ion-spinner name="crescent"></ion-spinner>
        <ion-note>Chargement en cour...</ion-note>
      </ion-item>

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
  IonBadge, IonNavLink
} from '@ionic/vue';
import WordModal from "@/components/WordModal.vue";
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
      try {
        this.sheets = await fetch('http://127.0.0.1:8000/sheets').then(resp => resp.json())
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
        default:
          return 'grey'
      }
    }
  }
}
</script>
