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
          <ion-title size="large">Dictionnaire des rimes</ion-title>
        </ion-toolbar>
        <ion-toolbar>
          <ion-searchbar :value="query" @ionInput="handleSearchBarInput($event.detail.value)" placeholder="Entrez un mot"></ion-searchbar>
          <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
        </ion-toolbar>
      </ion-header>


      <div class="ion-padding" v-if="!failed && rhymes.length === 0">
        <ion-note>Commencez à chercher un mot si-dessus !</ion-note>
      </div>

      <div class="ion-padding" v-if="failed">
        <ion-note>Fonctionne seulement avec une connexion internet !</ion-note>
      </div>
      <ion-content v-else>
        <ul>
          <li v-for="r in rhymes">{{r}}</li>
        </ul>
      </ion-content>
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
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonChip,
  IonBadge, IonNavLink, IonProgressBar, IonSearchbar
} from '@ionic/vue';
import FicheModal from "@/components/FicheModal.vue";
import {close, filterCircleOutline} from "ionicons/icons";
</script>

<script lang="ts">
import {RemedeRhymeRow} from "@/functions/types/remede";

export default {
  props: ['queryWord'],
  data() {
    return {
      loading: false,
      failed: false,
      rhymes: [] as RemedeRhymeRow[],
      query: '',
      // Ignoring linter error about empty function (@typescript-eslint/no-empty-function)
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      searchTimeout: window.setTimeout(() => {}, 500),
    }
  },
  mounted() {
    if (this.queryWord) {
      this.query = this.queryWord
      this.searchRhymes()
    }
  },
  methods: {
    async searchRhymes() {
      this.loading = true
      try {
        this.rhymes = await fetch(`https://rimes-remede.camarm.fr/${this.query}`).then(resp => resp.json())
        this.failed = false
      } catch {
        this.failed = true
      }
      this.loading = false
    },
    handleSearchBarInput(query: string) {
      this.query = query
      clearTimeout(this.searchTimeout)
      this.searchTimeout = window.setTimeout(() => {
        this.searchRhymes()
      }, 500)
    },
  }
}
</script>
<style>
</style>