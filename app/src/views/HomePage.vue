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
            <ion-icon slot="start" :icon="calendarOutline"/>
            <ion-label>
              <h2>Mot du jour</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: randomWord }">
          <ion-item color="light" button>
            <ion-icon :icon="shuffle" slot="start"/>
            <ion-label>
              <h2>Mot au hasard</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
      </ion-list>

      <ion-list inset>
        <ion-item @click="goTo('/marques-page')" button color="primary">
          <ion-icon slot="start" :icon="bookmark"/>
          <ion-label>
            Mes marques page
          </ion-label>
        </ion-item>
      </ion-list>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar, IonNavLink, IonSearchbar, IonIcon, IonLabel, IonItem, IonList } from '@ionic/vue';
import WordModal from "@/components/WordModal.vue";
import {bookmark, calendarOutline, shuffle} from "ionicons/icons";
</script>

<script lang="ts">
import {getAutocomplete, getRandomWord} from "@/functions/dictionnary";
import {useRouter} from "vue-router";

export default {
  data() {
    return {
      results: [] as string[],
      query: '',
      router: useRouter(),
      autocompleteTimeout: window.setTimeout(() => {}, 500),
      randomWord: ''
    }
  },
  mounted() {
    this.loadRandomWord()
  },
  methods: {
    async handleSearchbarInput(input: string) {
      this.query = input
      if (input != '') {
        this.startAutocompleteSearch(input)
      } else {
        window.clearTimeout(this.autocompleteTimeout)
        this.results = []
      }
    },
    startAutocompleteSearch(input: string) {
      window.clearTimeout(this.autocompleteTimeout)
      this.autocompleteTimeout = window.setTimeout(async () => {
        this.results = await getAutocomplete(input)
      }, 500)
    },
    goTo(path: string) {
      this.router.push(path)
    },
    async loadRandomWord() {
      this.randomWord = await getRandomWord()
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
