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
          <ion-title size="large">{{ $t('bookmarks') }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset>
        <ion-item :key="word" color="light" v-for="word in starredWords" @click="goTo(`/dictionary/${word}`)">
          <ion-icon color="primary" :icon="bookmark" @click="starWord(word); refresh()" slot="start"/>
          <ion-label>
            <h2 class="ion-text-capitalize">{{ word }}</h2>
          </ion-label>
        </ion-item>
      </ion-list>

      <ion-note v-if="starredWords.length === 0" class="ion-padding">{{ $t('bookmark.addWordsToBookmarks') }}</ion-note>

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
  IonList,
  IonNote,
  IonLabel,
  IonItem, useIonRouter
} from "@ionic/vue"
import {bookmark} from "ionicons/icons"
import {starWord} from "@/functions/favorites"

const router = useIonRouter()

const goTo = (path: string) => {
  router.push(path)
}
</script>

<script lang="ts">

import {getStarredWords} from "@/functions/favorites"

export default {
  data() {
    return {
      starredWords: [] as string[]
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    async refresh() {
      this.starredWords = await getStarredWords()
    }
  }
}
</script>

