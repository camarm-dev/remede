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
          <ion-title size="large">Marques pages</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset>
        <ion-nav-link v-for="word in starredWords" :component="WordModal" router-direction="forward" :component-props="{ motRemede: word }">
          <ion-item color="light">
            <ion-icon color="primary" :icon="bookmark" @click="starWord(word); refresh()" slot="start"/>
            <ion-label>
              <h2 class="ion-text-capitalize">{{ word }}</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
      </ion-list>

      <ion-note v-if="starredWords.length === 0" class="ion-padding">Ajoutez des mots à vos marques pages</ion-note>

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
  IonNavLink,
  IonIcon
} from '@ionic/vue';
import WordModal from "@/components/WordModal.vue";
import {bookmark} from "ionicons/icons";
import {starWord} from "@/functions/favorites";
</script>

<script lang="ts">

import {getStarredWords} from "@/functions/favorites";

export default {
  data() {
    return {
      starredWords: []
    }
  },
  created() {
    this.refresh()
  },
  methods: {
    handleThemeChangement(theme: string) {
      localStorage.setItem('userTheme', theme)
      document.body.classList.remove('dark')
      document.body.classList.remove('light')
      document.body.classList.add(theme)
    },
    getCurrentTheme() {
      return localStorage.getItem('userTheme') || 'light'
    },
    refresh() {
      this.starredWords = getStarredWords()
    }
  }
}
</script>

