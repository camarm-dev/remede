<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-searchbar :value="query" @ionInput="handleSearchBarInput($event.detail.value)" placeholder="Rechercher un mot"></ion-searchbar>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Dictionnaire</ion-title>
        </ion-toolbar>
      </ion-header>

      <div class="ion-padding">
        <ion-note>Rien ici pour le moment</ion-note>
        <ion-note v-for="result in results">{{ result }}</ion-note>
      </div>

      <ion-list inset>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ mot: 'à' }">
          <ion-item color="light" button>
            <ion-label slot="start">
              <h2>Mot du jour</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ mot: 'bienvenue' }">
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
import { IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar, IonNavLink } from '@ionic/vue';
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
      this.results = getAutocomplete(input)
    }
  }
}
</script>
