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
          <ion-searchbar :value="query" @ionInput="handleSearchBarInput($event.detail.value)" placeholder="Rechercher une fiche"></ion-searchbar>
          <ion-item class="item-carousel ion-text-wrap" lines="none">
            <ion-chip id="open-filters">
              <ion-icon :icon="filterCircleOutline"></ion-icon>
              <ion-label>Filtres</ion-label>
            </ion-chip>
            <ion-popover alignment="center" trigger="open-filters" trigger-action="click">
              <ion-chip class="filter" @click="addFilter(filter)" :color="getTagColor(filter)" v-for="filter in availableFilters">
                {{ filter }}
              </ion-chip>
            </ion-popover>

            <ion-chip v-for="filter in filters" :color="getTagColor(filter)">
              <ion-label>{{ filter }}</ion-label>
              <ion-icon :icon="close" @click="deleteFilter(filter)"></ion-icon>
            </ion-chip>
          </ion-item>
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
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonChip,
  IonBadge, IonNavLink, IonProgressBar, IonSearchbar
} from '@ionic/vue';
import FicheModal from "@/components/FicheModal.vue";
import {add, close, filterCircleOutline} from "ionicons/icons";
</script>

<script lang="ts">
export default {
  data() {
    return {
      loading: true,
      failed: false,
      sheets: [],
      all_sheets: [],
      filters: [],
      availableFilters: ['orthographe', 'conjugaison', 'grammaire', 'lexique', 'style', 'typographie'],
      query: ''
    }
  },
  mounted() {
    this.loadSheets()
  },
  methods: {
    async loadSheets() {
      this.loading = true
      try {
        this.all_sheets = await fetch('https://api-remede.camarm.fr/sheets').then(resp => resp.json())
        this.sheets = this.all_sheets
        this.filters = []
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
    },
    searchInSheets() {
      if (this.query.length == 0) this.loadFilteredSheets()
      else {
        if (this.sheets.length == 0) this.loadFilteredSheets()
        this.sheets = this.sheets.filter((value) => {
          return value.nom.toLowerCase().includes(this.query.toLowerCase())
        })
      }
    },
    handleSearchBarInput(query: string) {
      this.query = query
      this.searchInSheets()
    },
    loadFilteredSheets() {
      if (this.filters.length == 0) this.sheets = this.all_sheets
      else {
        this.sheets = this.all_sheets.filter((value) => {
          for (const tag of this.filters) {
            if (value.tags.includes(tag)) return true
          }
        })
      }
    },
    addFilter(tag: string) {
      this.filters.push(tag)
      this.availableFilters.splice(this.availableFilters.indexOf(tag), 1)
      this.loadFilteredSheets()
    },
    deleteFilter(tag: string) {
      this.filters.splice(this.filters.indexOf(tag), 1)
      this.availableFilters.push(tag)
      this.loadFilteredSheets()
    }
  }
}
</script>
<style>
.item-carousel {
  min-width: max-content;
  overflow-x: scroll;
}

.filter {
  min-width: max-content;
  justify-content: center;
}

ion-popover {
  --background: #e0e0e0;
  --border: 0;
  --width: max-content;
}

ion-popover .popover-content, ion-popover ion-content {
  --background: #e0e0e0;
  width: max-content !important;
}

ion-popover .popover-viewport {
  --background: #e0e0e0;
  display: flex;
  flex-direction: column;
  width: max-content;
}
</style>