<script setup lang="ts">
import {
  IonIcon,
  IonHeader,
  IonContent, IonTitle, IonToolbar, IonBackButton, IonButtons, IonSegment, IonSegmentButton
} from "@ionic/vue";
import {play, shareOutline} from "ionicons/icons";
import "@/components/WordModal.vue";
</script>

<template>
  <ion-header :translucent="true">
    <ion-toolbar>
      <ion-buttons slot="start">
        <ion-back-button defaultHref="/dictionnaire" text="Retour"></ion-back-button>
      </ion-buttons>
      <ion-title>Définition "{{ mot }}"</ion-title>
      <ion-buttons slot="end" @click="shareDefinition()">
        <ion-icon slot="icon-only" :icon="shareOutline"></ion-icon>
      </ion-buttons>
    </ion-toolbar>
  </ion-header>
  <ion-content :fullscreen="true" class="ion-padding">
    <ion-header collapse="condense">
      <ion-toolbar>
        <ion-label>
          <ion-title class="remede-font" size="large">{{ mot }}</ion-title>
          <p class="ion-padding-start">{{ document.ipa }}</p>
        </ion-label>
        <ion-buttons slot="end">
          <ion-button :disabled="notFound">
            <ion-icon slot="icon-only" :icon="play" color="medium"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-segment :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value">
          <ion-segment-button value="def">Définition</ion-segment-button>
          <ion-segment-button value="syn">Synonymes</ion-segment-button>
          <ion-segment-button value="ant">Antonymes</ion-segment-button>
          <ion-segment-button v-if="false" value="con">Conjugaison</ion-segment-button>
        </ion-segment>
      </ion-toolbar>
    </ion-header>
    <br>
    <div v-if="notFound" class="ion-padding">
      <ion-note>
        Ce mot n'a pas été trouvé dans le dictionnaire Remède...
      </ion-note>
    </div>
    <div v-if="tab == 'def'" class="tab-content">
      <div class="image" v-if="document.image.url !== ''">
        <figure>
          <img :alt="`Image de ${mot}`" :src="document.image.url"/>
          <figcaption>{{ document.image.credits }}</figcaption>
        </figure>
      </div>
      <div class="definition" v-for="def in document.definitions">
        <header>
          <h4 v-if="typeof def.genre !== 'string'">{{ def.genre[0] }}, {{ def.genre[1] }}</h4>
          <h4 v-else-if="def.genre != def.classe && def.classe != ''">{{ def.genre }}, {{ def.classe }}</h4>
          <h4 v-else>{{ def.genre }}</h4>
          <hr>
        </header>
        <div class="content">
          <ul>
            <li v-for="meaning in def.explications">
              <span v-html="meaning.replaceAll('https://fr.wiktionary.org/wiki/', '/definition/')" v-if="typeof meaning === 'string'"></span>
              <ul v-else class="ion-padding-start">
                <li v-for="subMeaning in meaning" v-html="subMeaning"></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-if="tab == 'syn'" class="tab-content">
      <div class="definition">
        <header>
          <h4>Synonymes</h4>
          <hr>
        </header>
      </div>
      <ul>
        <li v-for="syn in document.synonymes">
          <a href="" @click="goTo(`/dictionnaire/${syn}`)">{{ syn }}</a>
        </li>
      </ul>
      <ion-note v-if="document.synonymes.length == 0">Pas de synonymes référencés</ion-note>
      <ion-note v-else>Via <a target="_blank" :href="`http://synonymo.fr/synonyme/${mot}`">synonymo.fr</a></ion-note>
    </div>
    <div v-if="tab == 'ant'" class="tab-content">
      <div class="definition">
        <header>
          <h4>Antonymes</h4>
          <hr>
        </header>
      </div>
      <ul>
        <li v-for="ant in document.antonymes">
          <a href="" @click="goTo(`/dictionnaire/${ant}`)">{{ ant }}</a>
        </li>
      </ul>
      <ion-note v-if="document.antonymes.length == 0">Pas d'antonymes référencés</ion-note>
      <ion-note v-else>Via <a target="_blank" :href="`http://www.antonyme.org/antonyme/${mot}`">antonyme.org</a></ion-note>
    </div>
    <div v-if="tab == 'conj'" class="tab-content">

    </div>
    <br>
    <br>
    <div class="credits ion-padding-start" v-if="document.credits.name != ''">
      Voir <a target="_blank" :href="document.credits.url">{{ document.credits.name }}</a>
    </div>
  </ion-content>
</template>

<script lang="ts">

import {getWordDocument} from "@/functions/dictionnary";

export default {
  props: ['motRemede'],
  data() {
    return {
      mot: '',
      tab: localStorage.getItem('defaultTab') || 'def',
      document: {
        synonymes: [] as string[],
        antonymes: [] as string[],
        definitions: [],
        image: {
          url: '',
          credits: ''
        },
        references: [],
        ipa: '',
        credits: {
          name: '',
          url: ''
        }
      },
      notFound: false
    }
  },
  created() {
    this.mot = this.motRemede
    if (!this.motRemede) {
      this.mot = this.$router.params.mot
    }
    const document = getWordDocument(this.mot)
    if (document) {
      this.document = getWordDocument(this.mot)
    } else {
      this.notFound = true
    }
  },
  methods: {
    shareDefinition() {

    },
    goTo(path: string) {
      this.$router.push(path)
    }
  }
}
</script>

<style scoped>
.definition header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.definition header h4 {
  min-width: max-content;
  margin: 0 1em 0 0;
}

.definition header hr {
  margin: 0;
  width: 80%;
  background: none;
  border-bottom: 0.55px solid;
  border-color: var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

.definition .content ul {
  list-style: decimal;
}

.definition .content ul ul {
  list-style: disc;
}

.definition .content li {
  margin-bottom: .5em;
}

.credits {
  color: var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

.credits a {
  text-decoration: none;
}

summary {
  font-size: 2em;
}
</style>