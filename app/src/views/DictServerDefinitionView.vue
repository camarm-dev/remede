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
  IonPage,
  IonSpinner,
  IonBackButton,
  IonSkeletonText
} from "@ionic/vue"
import {
  ellipsisVertical, radioOutline, serverOutline,
} from "ionicons/icons"
import TabSection from "@/components/TabSection.vue"
import DictLogs from "@/components/DictLogs.vue"
</script>

<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button :text="$t('back')" default-href="/dictionary"></ion-back-button>
        </ion-buttons>
        <ion-title class="remede-font">{{ word }}</ion-title>
        <ion-buttons slot="end">
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
            <ion-title class="remede-font" size="large">{{ word }}</ion-title>
            <ion-skeleton-text class="ion-margin-start" style="width: 65px; border-radius: 2px" v-if="loading"/>
            <p class="ion-padding-start" v-else>{{ $t('from') }} {{ server }}</p>
          </ion-label>
        </ion-toolbar>
        <ion-toolbar>
          <ion-segment swipe-gesture :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value as string; listenSpecialTags()">
            <ion-segment-button value="def">{{ $t('definition.definition') }}</ion-segment-button>
            <ion-segment-button value="logs">{{ $t('dictClient.logs') }}</ion-segment-button>
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
        <div class="definition" v-for="def in definitions" :key="def.definition">
          <header>
            <div class="header-title">
              <h4>{{ def.word }}</h4>
            </div>
            <hr>
          </header>
          <div class="content">
            <pre v-html="parseMeaning(def.definition)"></pre>
          </div>
          <br>
        </div>
      </div>
      <TabSection v-if="isTab('logs')" :title="$t('dictClient.logs')">
        <DictLogs :logs="logs"/>
      </TabSection>
      <br>
      <br>
      <ion-modal :trigger="id.modal" :initial-breakpoint="0.75" :breakpoints="[0, 0.75, 0.9]">
        <ion-content class="ion-padding">
          <div class="list-title no-margin ion-padding-bottom">
            {{ $t('sources') }}
          </div>
          <ion-list class="border-radius">
            <ion-item color="light">
              <ion-icon slot="start" :icon="radioOutline"/>
              <ion-label>{{ server }}</ion-label>
            </ion-item>
            <ion-item color="light">
              <ion-icon slot="start" :icon="serverOutline"/>
              <ion-label>{{ database }} ({{ databaseId }})</ion-label>
            </ion-item>
            <ion-item v-if="header" color="light" lines="none">
              <ion-label>{{ $t('dictClient.serverHeader') }}</ion-label>
            </ion-item>
            <ion-item v-if="header" color="light">
              <ion-note class="ion-padding-bottom">{{ header?.raw }}</ion-note>
            </ion-item>
          </ion-list>
        </ion-content>
      </ion-modal>
      <br>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">

import {wordExists} from "@/functions/dictionnary"
import {defineComponent} from "vue"
import {useIonRouter} from "@ionic/vue"
import "swiper/css"
import "swiper/css/pagination"
import "@ionic/vue/css/ionic-swiper.css"
import {generateId} from "@/functions/id"
import {DictDefinition, DictResponseLine, getDictServerDefinition} from "@/functions/dictProtocol"
import { Browser } from "@capacitor/browser"

export default defineComponent({
  data() {
    return {
      word: "",
      server: "",
      port: 2628,
      database: "",
      databaseId: "",
      definitions: [] as DictDefinition[],
      logs: [] as DictResponseLine[],
      header: {} as DictResponseLine | undefined,
      goTo: function(path: string) {
        console.log(path)
      } as (path: string) => void,
      id: {
        modal: generateId()
      },
      notFound: false,
      loading: true,
      tab: "def"
    }
  },
  mounted() {
    const definitionRequest = JSON.parse(this.$route.params.definition as string) as DictDefinition
    this.word = definitionRequest.word
    this.server = definitionRequest.server || "Unknown server"
    this.port = definitionRequest.port || 2628
    this.database = definitionRequest.database
    this.databaseId = definitionRequest.databaseId

    this.fetchDefinition().then(this.listenSpecialTags)

    const ionRouter = useIonRouter()
    function goTo(path: string) {
      ionRouter.push(path)
    }
    this.goTo = goTo as (path: string) => void
  },
  methods: {
    async fetchDefinition() {
      const { definitions, rawDecoded } = await getDictServerDefinition({
        name: "",
        description: "",
        host: this.server,
        port: this.port
      }, this.word, this.database)
      this.definitions = definitions
      this.database = definitions[0].database // Load full db name
      this.logs = rawDecoded
      this.header = rawDecoded.find(line => line.type === "HEADER")
      this.loading = false
    },
    isTab(tab: string) {
      return this.tab == tab
    },
    async listenSpecialTags() {
      // Listen for <reference> tags
      document.querySelectorAll("reference").forEach(el => {
        const referenceListener = async () => {
          const href = el.getAttribute("href") || ""
          if (await wordExists(href)) { // TODO check if words exists in dict server !
            this.goTo(`/dictionary/${href}`) // TODO
          } else if (href.includes("://")) {
            await Browser.open({ url: href })
          } else {
            this.$router.push(`/search/${href}`)
          }
        }
        el.addEventListener("click", referenceListener)
        window.addEventListener("reset", () => {
          el.removeEventListener("click", referenceListener)
        })
      })
    },
    parseMeaning(meaning: string) {
      const lines = meaning.split("\n")
      if (lines[0].trim() == this.word) { // Remove first line if it just contains the word
        meaning = lines.slice(1).join("\n")
      }
      try {
        // TODO {link(http://url)} should become <reference href="url"></...>
        const parsingEl = document.createElement("div")
        parsingEl.innerHTML = meaning
            .replaceAll("{", "<reference>")
            .replaceAll("}", "</reference>")
            .replaceAll("\t", "")
            .trim()
        for (const referenceTag of Array.from(parsingEl.querySelectorAll("reference"))) {
          const innerText = referenceTag.innerHTML
          const href = (/\(([^)]+)\)/.exec(innerText) || [innerText])[0]
          referenceTag.setAttribute("href", href)
          referenceTag.innerHTML = innerText.replaceAll("\n", "").replaceAll("  ", "").trim()
        }
        return parsingEl.innerHTML
      } catch (e) {
        return meaning
      }
    }
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
  width: max-content;
  margin: 0;
}

.header-title {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 1em 0 0;
  max-width: 90%;
}

.header-title ion-icon {
  cursor: pointer;
  margin-left: .3em;
}

.definition header hr {
  margin: 0;
  width: 80%;
  background: none;
  border-bottom: 0.55px solid;
  border-color: var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

.definition .content {
  margin-bottom: 1em;
}

.border-radius {
  border-radius: 12px;
}

pre {
  font-family: var(--ion-font-family);
  max-width: 100%;
  overflow: hidden;
  text-wrap: stable;
  word-break: break-word;
}
</style>
