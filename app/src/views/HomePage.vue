<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-searchbar :value="query" @ionInput="handleSearchbarInput($event.detail.value)" placeholder="Rechercher un mot"></ion-searchbar>
      </ion-toolbar>
      <ion-toolbar :class="`results-wrapper ${results.length > 0 ? '': 'empty'}`">
        <ion-list class="search-results">
          <ion-nav-link v-for="result in results" router-direction="forward" :component="WordModal" :component-props="{ motRemede: result }">
            <ion-item class="ion-no-padding" button>
              <ion-label>
                {{ result }}
              </ion-label>
            </ion-item>
          </ion-nav-link>
        </ion-list>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Dictionnaire</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: 'à' }">
          <ion-item color="light" button>
            <ion-label slot="start">
              <h2>Mot du jour</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: 'bienvenue' }">
          <ion-item color="light" button>
            <ion-label slot="start">
              <h2>Mot au hasard</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
      </ion-list>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar, IonNavLink, IonSearchbar } from '@ionic/vue';
import WordModal from "@/components/WordModal.vue";
</script>

<script lang="ts">
import {getAutocomplete} from "@/functions/dictionnary";

export default {
  data() {
    return {
      results: [],
      query: ''
    }
  },
  methods: {
    handleSearchbarInput(input: string) {
      this.query = input
      if (input != '') {
        this.results = getAutocomplete(input)
      } else {
        this.results = []
      }
    }
  }
}
</script>
<style scoped>
.results-wrapper {
  transition: .5s ease-in-out;
  height: 270px;
}

.results-wrapper.empty {
  height: 0;
}

.search-results {
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  padding-inline-start: 10px;
  padding-inline-end: 10px;
}

.search-results ion-item {
  --border-width: 0;
  padding-bottom: .55px !important;
  background: linear-gradient(to right, var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc))) 70%, rgba(64, 64, 64, 0));
}

.search-results ion-item .item-bottom {
  --border-color: transparent;
}

.search-results ion-item::part(native) {
  --border-width: 0;
  --inner-border-width: 0;
  position: relative;
}
</style>
