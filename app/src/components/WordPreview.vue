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
} from "@ionic/vue"
import example from "@/assets/example.svg"
import {Swiper, SwiperSlide} from "swiper/vue"
import {Pagination} from "swiper/modules"
import quoteOpen from "@/assets/openQuote.svg"
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
            <ion-icon v-if="def.exemples.length > 0" :id="id.examples[document.definitions.indexOf(def)]" :icon="example" color="medium"/>
            <hr>
          </header>
          <ion-popover class="example" v-if="def.exemples.length > 0" :trigger="id.examples[document.definitions.indexOf(def)]">
            <div class="ion-padding examples">
              <h5>
                Exemples
                <span class="ion-color-medium">{{ mot }}</span>,
                <span v-if="typeof def.genre !== 'string'">{{ def.genre[0] }}, {{ def.genre[1] }}</span>
                <span v-else-if="def.genre != def.classe && def.classe != ''">{{ def.genre }}, {{ def.classe }}</span>
                <span v-else>{{ def.genre }}</span>
              </h5>
              <swiper
                  :pagination="{ clickable: true, enabled: true }"
                  :modules="[Pagination]"
              >
                <swiper-slide v-for="exemple in def.exemples" :key="exemple.contenu">
                  <div class="example-container">
                    <ion-icon class="opening-quote" :icon="quoteOpen"/>
                    <div>
                      <i class="example-content" v-html="exemple.contenu"/>
                    </div>
                    <span class="sources" v-html="exemple.sources"/>
                  </div>
                </swiper-slide>
              </swiper>
            </div>
          </ion-popover>
          <div class="content">
            <ul>
              <li :key="`def-${meaning}`" v-for="meaning in def.explications">
                <span v-html="meaning" v-if="typeof meaning === 'string'"></span>
                <ul v-else class="ion-padding-start">
                  <li :key="subMeaning" v-for="subMeaning in meaning" v-html="subMeaning"></li>
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
import {getWordDocument} from "@/functions/dictionnary"
import {RemedeWordDocument} from "@/functions/types/remede"
import {generateId} from "@/functions/id"

export default {
  props: [
      "mot"
  ],
  data() {
    return {
      document: {} as RemedeWordDocument,
      notFound: false,
      tab: "def" as string,
      id: {
        examples: []
      }
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
        this.document.definitions.forEach(() => {
          this.id.examples.push(generateId())
        })
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
