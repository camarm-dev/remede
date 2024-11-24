<script setup lang="ts">

import {
  IonSpinner, IonContent
} from "@ionic/vue";
</script>

<template>
  <ion-content class="ion-padding">
    <h5>
      {{ $t('definition.phoneme') }}
      <span class="contrast">{{ phoneme }}</span>
    </h5>
    <div v-if="loading" class="ion-padding ion-text-center">
      <ion-spinner name="crescent"></ion-spinner>
    </div>
    <ul>
      <li class="remede-font" v-for="wordObject in words">
        {{ wordObject[0] }}
      </li>
    </ul>
  </ion-content>
</template>

<script lang="ts">
// TODO: search words with phoneme, show them, and add possibility to here them

import { RemedeWordDocument } from "@/functions/types/remede";
import {getWordsWithPhoneme} from "@/functions/dictionnary";

export default {
  props: {
    phoneme: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      words: [] as [string, RemedeWordDocument[]][],
      loading: true
    }
  },
  mounted() {
    this.loadWords().then(() => {
      this.loading = false
    })
  },
  methods: {
    async loadWords() {
      this.words = await getWordsWithPhoneme(this.phoneme.replaceAll('\\', ''))
    },
    readWord(wordObject: RemedeWordDocument) {
      // todo
    }
  }
}
</script>

<style scoped>

</style>
