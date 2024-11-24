<script setup lang="ts">

import {
  IonSpinner, IonContent, IonIcon, IonButton
} from "@ionic/vue";
import {play} from "ionicons/icons";
</script>

<template>
  <ion-content class="ion-padding">
    <h3>
      {{ $t('definition.phoneme') }}
      <span class="contrast">{{ phoneme }}</span>
    </h3>
    <p class="contrast">{{ $t('definition.wordWithThisPhoneme') }}</p>
    <div v-if="loading" class="ion-padding ion-text-center">
      <ion-spinner name="crescent"></ion-spinner>
    </div>
    <div class="definition" :key="`phoneme-${wordObject[0]}`" v-for="wordObject in words">
      <header>
        <div class="header-title">
          <h4 class="ion-text-capitalize">{{ wordObject[0] }}</h4>
        </div>
        <hr>
        <ion-button size="small" fill="clear" @click="readWord(wordObject)">
          <ion-icon v-if="!audioLoading[wordObject[0]]" slot="icon-only" :icon="play" color="medium"/>
          <ion-spinner v-else slot="icon-only" name="circles" color="medium"/>
        </ion-button>
      </header>
    </div>
  </ion-content>
</template>

<script lang="ts">
import { RemedeWordDocument } from "@/functions/types/remede";
import {getWordsWithPhoneme} from "@/functions/dictionnary";
import {toastController} from "@ionic/vue";

export default {
  props: {
    phoneme: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      words: [] as [string, RemedeWordDocument][],
      audioLoading: {} as { [key: string]: boolean },
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
    getAudioUrl(wordObject: [string, RemedeWordDocument]) {
      if (wordObject[1].pronunciation) {
        return wordObject[1].pronunciation.audio
      }
      return `https://remede-tts.camarm.fr/api/tts?voice=nanotts%3Afr-FR&lang=fr&vocoder=high&denoiserStrength=0.005&text=${encodeURIComponent(wordObject[0])}&speakerId=&ssml=true&ssmlNumbers=false&ssmlDates=false&ssmlCurrency=false&cache=true`
    },
    readWord(wordObject: [string, RemedeWordDocument]) {
      this.audioLoading[wordObject[0]] = true
      const url = this.getAudioUrl(wordObject)
      fetch(url, {
        method: "GET",
        cache: "no-cache"
      }).then(resp => resp.blob()).then(audio => {
        const player = new window.Audio()
        player.src = URL.createObjectURL(audio)
        player.play()
        this.audioLoading[wordObject[0]] = false
      }).catch(async e => {
        const toast = await toastController.create({
          header: this.$t("error"),
          message: this.$t("errors.cannotReadWord", { error: e }),
          color: "danger",
          duration: 3000
        })
        this.audioLoading[wordObject[0]] = false
        await toast.present()
      })
    }
  }
}
</script>

<style scoped>
ion-content {
  min-height: 300px;
  height: max-content;
  padding-top: 3em !important;
}

.contrast {
  color: var(--ion-color-medium);
}

.definition header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.definition header h4 {
  min-width: max-content;
  margin: 0 .3em 0 0;
}

.definition header hr {
  margin: 0;
  width: 80%;
  background: none;
  border-bottom: 0.55px solid;
  border-color: var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

header ion-button {
  margin: 0 0 0 .5em;
}

.header-title {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 1em 0 0;
}
</style>
