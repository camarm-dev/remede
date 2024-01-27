<script setup lang="ts">
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonIcon,
  IonPopover,
  IonNote,
  IonContent,
  IonLabel,
  IonSegmentButton,
  IonSegment,
  IonTitle
} from '@ionic/vue'
import example from "@/assets/example.svg";
</script>

<template>
  <ion-page>
    <ion-header>
      <button class="handle"></button>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-label>
            <ion-title class="remede-font" size="large">{{ mot }}</ion-title>
            <p class="ion-padding-start">{{ document.ipa }}</p>
          </ion-label>
        </ion-toolbar>
        <ion-toolbar>
          <ion-segment swipe-gesture :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value;">
            <ion-segment-button value="def">Définition</ion-segment-button>
            <ion-segment-button value="syn">Synonymes</ion-segment-button>
            <ion-segment-button value="ant">Antonymes</ion-segment-button>
          </ion-segment>
        </ion-toolbar>
      </ion-header>
      <div v-if="notFound" class="ion-padding">
        <ion-note>
          Ce mot n'a pas été trouvé dans le dictionnaire Remède...
        </ion-note>
      </div>
      <div class="tab-content" v-if="tab == 'def'">
        <div class="definition" :key="`def-genre-${document.definitions.indexOf(def).toString()}`" v-for="def in document.definitions">
          <header>
            <h4 v-if="typeof def.genre !== 'string'">{{ def.genre[0] }}, {{ def.genre[1] }}</h4>
            <h4 v-else-if="def.genre != def.classe && def.classe != ''">{{ def.genre }}, {{ def.classe }}</h4>
            <h4 v-else>{{ def.genre }}</h4>
            <hr>
          </header>
          <div class="content">
            <ul>
              <li :key="`def-${meaning}`" v-for="meaning in def.explications">
                <span v-html="meaning" v-if="typeof meaning === 'string'"></span>
                <ul v-else class="ion-padding-start">
                  <li :key="subMeaning" v-for="subMeaning in meaning" v-html="subMeaning"></li>
                </ul>
                <ion-icon v-if="def.exemples.length > 0" :id="meaning" :icon="example" color="medium"/>
                <ion-popover v-if="def.exemples.length > 0" :trigger="meaning">
                  <div class="ion-padding examples">
                    <h5>
                      Exemples
                      <span class="ion-color-medium">{{ mot }}</span>,
                      <span v-if="typeof def.genre !== 'string'">{{ def.genre[0] }}, {{ def.genre[1] }}</span>
                      <span v-else-if="def.genre != def.classe && def.classe != ''">{{ def.genre }}, {{ def.classe }}</span>
                      <span v-else>{{ def.genre }}</span>
                    </h5>
                    <p v-for="exemple in def.exemples" :key="exemple.contenu"><i>{{ exemple.contenu }}</i> <span class="sources" v-html="exemple.sources"/><br></p>
                  </div>
                </ion-popover>
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
          <li :key="syn" v-for="syn in document.synonymes">
            <a>
              {{ syn }}
            </a>
          </li>
        </ul>
        <ion-note v-if="document.synonymes.length == 0">Pas de synonymes référencés</ion-note>
      </div>
      <div v-if="tab == 'ant'" class="tab-content">
        <div class="definition">
          <header>
            <h4>Antonymes</h4>
            <hr>
          </header>
        </div>
        <ul>
          <li :key="ant" v-for="ant in document.antonymes">
            <a>
              {{ ant }}
            </a>
          </li>
        </ul>
        <ion-note v-if="document.antonymes.length == 0">Pas d'antonymes référencés</ion-note>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {getWordDocument} from "@/functions/dictionnary";
import {RemedeWordDocument} from "@/functions/types/remede";

export default {
  props: [
      'mot'
  ],
  data() {
    return {
      document: {} as RemedeWordDocument,
      notFound: false,
      tab: 'def' as string
    }
  },
  mounted() {
    this.loadDocument()
  },
  methods: {
    async loadDocument() {
      let document

      try {
        document = await getWordDocument(this.mot)
      } catch {
        document = null
      }

      if (document) {
        this.document = document
      } else {
        this.notFound = true
      }
    }
  }
}
</script>

<style scoped>
.handle {
  width: 36px;
  height: 5px;
  border-radius: 8px;
  display: block;
  margin: 6px auto auto;
  background: var(--ion-color-step-350, #c0c0be) !important;
  cursor: pointer;
}
</style>