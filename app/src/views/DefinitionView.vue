<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonSegment,
  IonSegmentButton,
  IonTitle,
  IonToolbar,
  IonButton,
  IonList,
  IonNote,
  IonLabel,
  IonItem,
  IonModal,
  IonAccordion,
  IonAccordionGroup,
  IonPopover,
  IonPage,
  IonSpinner,
  IonBackButton,
  IonSkeletonText
} from "@ionic/vue"
import {
  bookmark,
  bookmarkOutline, chevronBackOutline,
  chevronDownOutline,
  documentAttachOutline,
  ellipsisVertical,
  fingerPrintOutline,
  link,
  play,
  shareOutline
} from "ionicons/icons"
import { Swiper, SwiperSlide } from "swiper/vue"
import { Pagination } from "swiper/modules"
import example from "@/assets/example.svg"
import quoteOpen from "@/assets/openQuote.svg"
import TabSection from "@/components/TabSection.vue"
import ConjugationTable from "@/components/ConjugationTable.vue"
import PluralsTable from "@/components/PluralsTable.vue";


const detailsModal = ref()

const closeModal = () => detailsModal.value.$el.dismiss(null, "cancel")
</script>

<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-button @click="quitApp()" v-if="closeApp" size="small">
            <ion-icon :icon="chevronBackOutline"/>
            {{ $t('definition.backToApp') }}
          </ion-button>
          <ion-back-button v-else :text="$t('back')" default-href="/dictionnaire"></ion-back-button>
        </ion-buttons>
        <ion-title class="remede-font">{{ mot }}</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="starWord(mot); stared = isWordStarred(mot)">
            <ion-icon slot="icon-only" :icon="stared ? bookmark: bookmarkOutline"></ion-icon>
          </ion-button>
          <ion-button @click="shareDefinition()">
            <ion-icon slot="icon-only" :icon="shareOutline"></ion-icon>
          </ion-button>
          <ion-button :id="id.modal">
            <ion-icon slot="icon-only" :icon="ellipsisVertical"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <ion-header collapse="condense">
        <ion-toolbar class="ion-margin-bottom">
          <ion-label>
            <ion-title class="remede-font" size="large">{{ mot }}</ion-title>
            <ion-skeleton-text class="ion-margin-start" style="width: 65px; border-radius: 2px" v-if="loading"/>
            <p class="ion-padding-start" v-else>{{ wordObject.phoneme }}</p>
          </ion-label>
          <ion-buttons slot="end">
            <ion-button @click="readWord()" :disabled="notFound">
              <ion-icon v-if="!audioLoading" slot="icon-only" :icon="play" color="medium"/>
              <ion-spinner v-else slot="icon-only" name="circles" color="medium"/>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
        <ion-toolbar>
          <ion-segment swipe-gesture :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value as string; refreshListeners()">
            <ion-segment-button value="def">{{ $t('definition.definition') }}</ion-segment-button>
            <ion-segment-button value="syn">{{ $t('definition.synonyms') }}</ion-segment-button>
            <ion-segment-button value="ant">{{ $t('definition.antonyms') }}</ion-segment-button>
          </ion-segment>
        </ion-toolbar>
      </ion-header>
      <br>
      <div v-if="loading" class="ion-padding ion-text-center">
        <ion-spinner name="crescent"></ion-spinner>
      </div>
      <div v-if="notFound" class="ion-padding">
        <ion-note>
          {{ $t('definition.wordNotFound') }}
        </ion-note>
      </div>
      <div v-if="isTab('def')" class="tab-content">
        <div class="definition" :key="`def-genre-${wordObject.definitions.indexOf(def).toString()}`" v-for="def in wordObject.definitions">
          <header>
            <div class="header-title">
              <h4 v-if="def.gender != ''">{{ def.nature }}, {{ def.gender }}</h4>
              <h4 v-else>{{ def.nature }}</h4>
              <ion-icon v-if="def.examples.length > 0" :id="id.examples[wordObject.definitions.indexOf(def)]" :icon="example" color="medium"/>
            </div>
            <ion-popover class="example" v-if="def.examples.length > 0" :trigger="id.examples[wordObject.definitions.indexOf(def)]">
              <div class="ion-padding examples">
                <h5>
                  {{ $t('definition.examples') }}
                  <span class="ion-color-medium">{{ mot }}</span>,
                  <span v-if="def.gender != ''">{{ def.nature }}, {{ def.gender }}</span>
                  <span v-else>{{ def.nature }}</span>
                </h5>
                <swiper
                    :pagination="{ clickable: true, enabled: true }"
                    :modules="[Pagination]"
                >
                  <swiper-slide v-for="example in def.examples" :key="example.content">
                    <div class="example-container">
                      <ion-icon class="opening-quote" :icon="quoteOpen"/>
                      <div>
                        <i class="example-content" v-html="example.content"/>
                      </div>
                      <span class="sources" v-html="example.sources"/>
                    </div>
                  </swiper-slide>
                </swiper>
              </div>
            </ion-popover>
            <hr>
          </header>
          <ion-list inset class="border-radius" v-if="hasConjugations() && isVerb(def)">
            <ion-item lines="none" color="light" button @click="tab = 'conj'">
              {{ $t('definition.openConjugation') }}
            </ion-item>
          </ion-list>
          <div class="content">
            <ul>
              <li :key="`def-${meaning}`" v-for="meaning in def.explanations">
                <span v-html="parseMeaning(meaning)" v-if="typeof meaning === 'string'"></span>
                <ul v-else class="ion-padding-start">
                  <li :key="`def-submeaning-${meaning.indexOf(subMeaning)}`" v-for="subMeaning in meaning" v-html="parseMeaning(subMeaning)"></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
        <div class="definition">
          <header v-if="wordObject.etymologies.length > 0">
            <h4>{{ $t('definition.etymologies') }}</h4>
            <hr>
          </header>
          <div class="content">
            <ul>
              <li v-for="content in wordObject.etymologies" :key="content" v-html="parseMeaning(content)"/>
            </ul>
          </div>
        </div>
        <div class="definition" v-if="wordObject.plurals.length > 0">
          <header>
            <h4>{{ $t('definition.plurals') }}</h4>
            <hr>
          </header>
          <div class="content">
            <PluralsTable :plurals="wordObject.plurals"/>
          </div>
        </div>
      </div>
      <TabSection v-if="isTab('syn')" :title="$t('definition.synonyms')">
        <ul>
          <li :key="syn" v-for="syn in wordObject.synonyms">
            <a @click="goTo(`/dictionnaire/${syn}`)">
              {{ syn }}
            </a>
          </li>
        </ul>
        <ion-note v-if="wordObject.synonyms.length == 0">{{ $t('definition.noSynonyms') }}</ion-note>
      </TabSection>
      <TabSection v-if="isTab('ant')" :title="$t('definition.antonyms')">
        <ul>
          <li :key="ant" v-for="ant in wordObject.antonyms">
            <a @click="goTo(`/dictionnaire/${ant}`)">
              {{ ant }}
            </a>
          </li>
        </ul>
        <ion-note v-if="wordObject.antonyms.length == 0">{{ $t('definition.noAntonyms') }}</ion-note>
      </TabSection>
      <TabSection v-if="isTab('conj')" :title="$t('definition.conjugation')">
        <ConjugationTable :conjugations="wordObject.conjugations"/>
      </TabSection>
      <br>
      <br>
      <ion-modal ref="detailsModal" :trigger="id.modal" :initial-breakpoint="0.75" :breakpoints="[0, 0.75, 0.9]">
        <ion-content class="ion-padding">
          <div class="list-title no-margin ion-padding-bottom">
            {{ $t('dictionary') }}
          </div>
          <ion-list class="border-radius">
            <ion-item button color="primary" lines="none" @click="goTo(`/rimes/${mot}`); closeModal()">
              {{ $t('definition.openRhymesDictionary') }}
            </ion-item>
          </ion-list>
          <div class="list-title no-margin ion-padding-bottom">
            {{ $t('credits') }}
          </div>
          <ion-list class="border-radius">
            <ion-item color="light" button href="https://github.com/camarm-dev/remede/blob/main/LICENSE" target="_blank">
              <ion-icon :icon="documentAttachOutline" slot="start" color="medium"/>
              <ion-label>
                {{ $t('license') }}
              </ion-label>
            </ion-item>
            <ion-item lines="none" color="light" button href="https://docs.remede.camarm.fr/docs/database/credits" target="_blank">
              <ion-icon :icon="fingerPrintOutline" slot="start" color="medium"/>
              <ion-label>
                {{ $t('remedeData') }}
              </ion-label>
            </ion-item>
          </ion-list>
          <div class="list-title no-margin ion-padding-bottom">
            {{ $t('sources') }}
          </div>
          <ion-list class="border-radius">
            <ion-accordion-group>
              <ion-accordion value="first">
                <ion-item button :detail-icon="chevronDownOutline" color="light" slot="header">
                  <ion-label>{{ $t('sources') }}</ion-label>
                </ion-item>
                <div slot="content" class="accordion-content">
                  <ion-item v-if="wordObject.pronunciation" @click="open(wordObject.pronunciation.credits)" :lines="wordObject.sources.length == 0 ? 'none': 'inset'" button :detail-icon="link">
                    {{ $t('definition.pronunciation') }}
                  </ion-item>
                  <ion-item v-for="source in wordObject.sources" :key="source.url" @click="open(source.url.replaceAll('{word}', mot))" :lines="wordObject.sources.indexOf(source) == wordObject.sources.length - 1 ? 'none': 'inset'" button :detail-icon="link">
                    {{ $t(source.label) }}
                  </ion-item>
                </div>
              </ion-accordion>
            </ion-accordion-group>
          </ion-list>
        </ion-content>
      </ion-modal>
      <br>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">

import {getWordDocument, wordExists} from "@/functions/dictionnary"
import {isWordStarred, starWord} from "@/functions/favorites"
import {Share} from "@capacitor/share"
import { FilledRemedeWordDocument } from "@/functions/types/remede"
import {defineComponent, ref} from "vue"
import {modalController, toastController, useIonRouter} from "@ionic/vue"
import "swiper/css"
import "swiper/css/pagination"
import "@ionic/vue/css/ionic-swiper.css"
import {generateId} from "@/functions/id"
import {App} from "@capacitor/app"
import PhonemeDetailsSheet from "@/components/PhonemeDetailsSheet.vue";


export default defineComponent({
  props: ["motRemede"],
  data() {
    return {
      mot: "",
      id: {
        modal: generateId(),
        examples: [] as string[]
      },
      tab: localStorage.getItem("defaultTab") || "def" as string,
      wordObject: {
        synonyms: [],
        antonyms: [],
        definitions: [],
        phoneme: "",
        plurals: [],
        sources: [],
        pronunciation: null,
        conjugations: {},
        etymologies: [] as string[]
      } as FilledRemedeWordDocument,
      notFound: false,
      stared: false,
      audioLoading: false,
      goTo: function(path: string) {
        console.log(path)
      } as (path: string) => void,
      el: null as any,
      loading: false,
      closeApp: false
    }
  },
  mounted() {
    const ionRouter = useIonRouter()

    function goTo(path: string) {
      ionRouter.push(path)
    }

    this.el = ref(this.$el)
    this.goTo = goTo as (path: string) => void

    const url = new URLSearchParams(location.search)
    const data = url.get("close")
    this.closeApp = data ? data == "true": false
  },
  created() {
    this.loading = true
    this.loadData(null).then(() => {
      this.listenSpecialTags()
      this.loading = false
    }).catch(() => {
      this.notFound = true
      this.loading = false
    })
  },
  methods: {
    quitApp() {
      App.exitApp()
    },
    async loadData(mot: null | string) {
      this.mot = mot || this.motRemede
      if (!this.mot) {
        this.mot = this.$route.params.mot as string
      }
      const document = await getWordDocument(this.mot)
      if (document) {
        this.wordObject = document
        this.wordObject.definitions.forEach(() => {
          this.id.examples.push(generateId())
        })
      } else {
        this.notFound = true
      }

      this.stared = isWordStarred(this.mot)
    },
    async shareDefinition() {
      try {
        await Share.share({
          title: this.$t("share.definitionTitle", { word: this.mot }),
          text: this.$t("share.definitionDescription", { word: this.mot }),
          url: `https://remede-app.camarm.fr/dictionnaire/${this.mot}`,
          dialogTitle: this.$t("share.definitionDialogTitle"),
        })
      } catch {
        console.error("Failed to share.")
      }
    },
    getAudioUrl() {
      if (this.wordObject.pronunciation) {
        return this.wordObject.pronunciation.audio
      }
      return `https://remede-tts.camarm.fr/api/tts?voice=nanotts%3Afr-FR&lang=fr&vocoder=high&denoiserStrength=0.005&text=${encodeURIComponent(this.mot)}&speakerId=&ssml=true&ssmlNumbers=false&ssmlDates=false&ssmlCurrency=false&cache=true`
    },
    readWord() {
      this.audioLoading = true
      const url = this.getAudioUrl()
      fetch(url, {
        method: "GET",
        cache: "no-cache"
      }).then(resp => resp.blob()).then(audio => {
        const player = new window.Audio()
        player.src = URL.createObjectURL(audio)
        player.play()
        this.audioLoading = false
      }).catch(async e => {
        const toast = await toastController.create({
          header: this.$t("error"),
          message: this.$t("errors.cannotReadWord", { error: e }),
          color: "danger",
          duration: 3000
        })
        this.audioLoading = false
        await toast.present()
      })
    },
    open(url: string) {
      window.open(url)
    },
    refreshListeners() {
      window.dispatchEvent(new Event("reset"))
      const safeListen = () => {
        if (document.querySelectorAll("reference, phoneme").length == 0) {
          setTimeout(safeListen, 500)
        } else {
          this.listenSpecialTags()
        }
      }
      setTimeout(safeListen, 500)
    },
    isTab(tab: string) {
      return this.tab == tab
    },
    async listenSpecialTags() {
      // Listen for <reference> tags
      document.querySelectorAll("reference").forEach(el => {
        const referenceListener = async () => {
          const href = el.getAttribute("href") || ""
          const word = href.replaceAll("https://fr.wiktionary.org/wiki/", "").replaceAll("/wiki/", "")
          if (await wordExists(word)) {
            this.goTo(`/dictionnaire/${word}`)
          } else {
            window.open(href)
          }
        }
        el.addEventListener("click", referenceListener)
        window.addEventListener("reset", () => {
          el.removeEventListener("click", referenceListener)
        })
      })
      // Listen for <phoneme> tags
      document.querySelectorAll("phoneme").forEach(el => {
        const phonemeListener = async () => {
          const phoneme = el.textContent
          const modal = await modalController.create({
            component: PhonemeDetailsSheet,
            breakpoints: [0, 1],
            initialBreakpoint: 1,
            componentProps: {
              phoneme
            },
            cssClass: 'phoneme-modal'
          })
          await modal.present()
        }
        el.addEventListener("click", phonemeListener)
        window.addEventListener("reset", () => {
          el.removeEventListener("click", phonemeListener)
        })
      })
    },
    parseMeaning(meaning: string) {
      try {
        return meaning.replaceAll("<a", "<reference").replaceAll("</a>", "</reference>")
      } catch (e) {
        return meaning
      }
    },
    hasConjugations() {
      return Object.keys(this.wordObject.conjugations).length > 0
    },
    isVerb(def: FilledRemedeWordDocument["definitions"][keyof FilledRemedeWordDocument["definitions"]]) {
      return def.nature.includes('Verbe') || def.nature.includes('Verb')
    },
    starWord
  }
})
</script>

<style>
.definition header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.definition header h4 {
  min-width: max-content;
  margin: 0 .3em 0 0;
}

.header-title {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 1em 0 0;
}

.header-title ion-icon {
  cursor: pointer;
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

.examples .sources {
  margin-top: 1em;
  font-size: .8em;
  margin-left: 1em;
  color: var(--ion-color-medium);
  text-align: end;
}

.credits {
  color: var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

.credits a {
  text-decoration: none;
}

details {
  margin-bottom: .5em;
}

summary {
  font-size: 1.25rem;
  font-weight: 400;
}

.border-radius {
  border-radius: 12px;
}

.border {
  margin: 0;
  border: .55px solid var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

ion-item:not(+ ion-item)::part(native) {
  border-radius: 12px;
}

ion-list.no-radius ion-item:last-child {
  --inner-border-width: 0;
}

ion-icon.loading#playIcon {
  animation: .5s infinite loading;
  transition: .5s ease-in-out;
}

@keyframes loading {
  from {
    color: transparent !important;
  }

  to {
    color: var(--ion-color-medium) !important;
  }
}

.ion-color-medium {
  color: var(--ion-color-medium)
}

div.accordion-content[slot='content'] ion-item {
  --background: rgba(var(--ion-color-light-rgb), 0.5);
}

.handle {
  width: 36px;
  height: 5px;
  border-radius: 8px;
  display: block;
  margin: 6px auto auto;
  background: var(--ion-color-step-350, #c0c0be) !important;
  cursor: pointer;
}

.swiper {
  --bullet-background: var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
  --bullet-background-active: var(--ion-color-medium);
}

.swiper-slide {
  text-align: left;
}

.dark ion-popover.example {
  --background: #0f0f0f;
}

ion-popover.example {
  --width: 90%;
}

.examples {
  padding: 1em 1.2em !important;
  border-radius: 12px;
  height: max-content;
}

.examples h5 {
  margin-top: .5em !important;
  margin-bottom: .7em !important;
}

.example-container {
  display: flex;
  flex-direction: column;
  padding-bottom: 2em;
}

.example-container .example-content {
  margin-bottom: .7em;
  margin-left: .4em;
  text-align: left;
}

.example-container .example-content * {
  text-align: left;
}

.example-container b, .example-container strong {
  display: inline-block;
  transition: .5s ease-in-out;
  font-weight: normal;
  margin-top: 0;
  padding: 0 5px;
  margin-bottom: 0;
  background: linear-gradient(to right, rgba(255, 235, 9, 0.5), rgba(255, 235, 9, 0.4), rgba(255, 235, 9, 0.5));
  border-radius: 3px;
}

.opening-quote {
  margin-bottom: .3em;
}

.closing-quote {
  position: relative;
  padding-left: 1em;
  top: .5em;
}

.phoneme-modal {
  --height: auto
}
</style>
