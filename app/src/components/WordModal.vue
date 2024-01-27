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
  IonSelect,
  IonSelectOption,
  IonNavLink,
  IonList,
  IonNote,
  IonLabel,
  IonItem,
  IonModal,
  IonAccordion,
  IonAccordionGroup,
  IonAlert,
  IonPopover,
  IonPage,
  IonSpinner
} from "@ionic/vue";
import {
  bookmark,
  bookmarkOutline,
  chevronBackOutline,
  chevronDownOutline,
  ellipsisVertical,
  link,
  play,
  shareOutline
} from "ionicons/icons";
import example from "@/assets/example.svg"
import copyright from "@/assets/copyright.svg"
</script>

<template>
  <ion-page>
    <ion-header v-if="header" :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-nav-link router-direction="back">
            <ion-button @click="navigateBack()">
              <ion-icon class="ion-no-margin" :icon="chevronBackOutline" slot="start"/>
              Retour
            </ion-button>
          </ion-nav-link>
        </ion-buttons>
        <ion-title>Définition "{{ mot }}"</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="starWord(mot); stared = isWordStarred(mot)">
            <ion-icon slot="icon-only" :icon="stared ? bookmark: bookmarkOutline"></ion-icon>
          </ion-button>
          <ion-button @click="shareDefinition()">
            <ion-icon slot="icon-only" :icon="shareOutline"></ion-icon>
          </ion-button>
          <ion-button :id="`open-modal-${mot}`">
            <ion-icon slot="icon-only" :icon="ellipsisVertical"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-header v-else>
      <button class="handle"></button>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-label>
            <ion-title class="remede-font" size="large">{{ mot }}</ion-title>
            <p class="ion-padding-start">{{ document.ipa }}</p>
          </ion-label>
          <ion-buttons slot="end">
            <ion-button @click="readWord()" :disabled="notFound">
              <ion-icon v-if="!audioLoading" slot="icon-only" :icon="play" color="medium"/>
              <ion-spinner v-else slot="icon-only" name="circles" color="medium"/>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
        <ion-toolbar>
          <ion-segment swipe-gesture :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value; refreshListeners()">
            <ion-segment-button value="def">Définition</ion-segment-button>
            <ion-segment-button value="syn">Synonymes</ion-segment-button>
            <ion-segment-button value="ant">Antonymes</ion-segment-button>
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
        <div class="definition" :key="`def-genre-${document.definitions.indexOf(def).toString()}`" v-for="def in document.definitions">
          <header>
            <h4 v-if="typeof def.genre !== 'string'">{{ def.genre[0] }}, {{ def.genre[1] }}</h4>
            <h4 v-else-if="def.genre != def.classe && def.classe != ''">{{ def.genre }}, {{ def.classe }}</h4>
            <h4 v-else>{{ def.genre }}</h4>
            <hr>
          </header>
          <ion-list inset class="border-radius" v-if="getModes().length > 0 && def.genre.includes('Verbe')">
            <ion-item lines="none" color="light" button @click="tab = 'conj'">
              Ouvrir la conjugaison
            </ion-item>
          </ion-list>
          <div class="content">
            <ul>
              <li :key="`def-${meaning}`" v-for="meaning in def.explications">
                <span v-html="parseMeaning(meaning)" v-if="typeof meaning === 'string'"></span>
                <ul v-else class="ion-padding-start">
                  <li :key="subMeaning" v-for="subMeaning in meaning" v-html="parseMeaning(subMeaning)"></li>
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
            <a @click="openPreviewModal(syn)">
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
            <a @click="openPreviewModal(ant)">
              {{ ant }}
            </a>
          </li>
        </ul>
        <ion-note v-if="document.antonymes.length == 0">Pas d'antonymes référencés</ion-note>
      </div>
      <div v-if="tab == 'conj'" class="tab-content">
        <div class="definition">
          <header>
            <h4>Conjugaison</h4>
            <hr>
          </header>
        </div>
        <br>
        <ion-list inset class="border-radius border">
          <ion-item color="light" lines="full">
            <ion-label slot="start">
              <p>Mode</p>
            </ion-label>
            <ion-label slot="end">
              <p>Temps</p>
            </ion-label>
          </ion-item>
          <ion-item color="light" lines="full">
            <ion-select @ionChange="changeMode($event.target.value)" slot="start" interface="action-sheet" placeholder="Mode" :value="currentMode">
              <ion-select-option :key="mode" v-for="mode in getModes()" :value="mode">{{ mode }}</ion-select-option>
            </ion-select>
            <ion-select @ionChange="changeTemps($event.target.value)" slot="end" interface="action-sheet" placeholder="Temps" :value="currentTemps">
              <ion-select-option :key="temps" v-for="temps in modeTemps" :value="temps">{{ temps }}</ion-select-option>
            </ion-select>
          </ion-item>
          <ion-item :key="sujet" v-for="sujet in currentSujets">
            <ion-label>
              <p>{{ sujet }}</p>
            </ion-label>
            <ion-label slot="end">
              {{ getFormeVerbale(currentMode, currentTemps, sujet) }}
            </ion-label>
          </ion-item>
        </ion-list>
        <br>
      </div>
      <br>
      <br>
      <ion-modal :trigger="`open-modal-${mot}`" :initial-breakpoint="0.5" :breakpoints="[0, 0.5, 0.75]">
        <ion-content class="ion-padding">
          <div class="list-title no-margin ion-padding-bottom">
            Dictionnaire
          </div>
          <ion-list class="border-radius">
            <ion-item button color="primary" lines="none" disabled>
              Ouvrir le dictionnaire des rimes
            </ion-item>
          </ion-list>
          <div class="list-title no-margin ion-padding-bottom">
            Crédits & sources
          </div>
          <ion-list class="border-radius">
            <ion-item :id="`open-copyrights-${mot}`" button color="light" lines="none" :detail-icon="copyright">
              Ouvrir les crédits
            </ion-item>
            <ion-accordion-group>
              <ion-accordion value="first">
                <ion-item button :detail-icon="chevronDownOutline" color="light" slot="header">
                  <ion-label>Sources</ion-label>
                </ion-item>
                <div slot="content" class="accordion-content">
                  <ion-item @click="open(document.credits.url)" button lines="inset" :detail-icon="link">
                    {{ document.credits.name }}
                  </ion-item>
                  <ion-item v-if="document.synonymes.length > 0" @click="open(`http://synonymo.fr/synonyme/${mot}`)" button lines="inset" :detail-icon="link">
                    Synonymes
                  </ion-item>
                  <ion-item v-if="document.antonymes.length > 0" @click="open(`http://www.antonyme.org/antonyme/${mot}`)" button lines="inset" :detail-icon="link">
                    Antonymes
                  </ion-item>
                  <ion-item v-if="Object.keys(document.conjugaisons).length > 0" @click="open(`http://conjuguons.fr/conjugaison/verbe/${mot}`)" button lines="none" :detail-icon="link">
                    Conjugaison
                  </ion-item>
                </div>
              </ion-accordion>
            </ion-accordion-group>
          </ion-list>
          <ion-alert
              :trigger="`open-copyrights-${mot}`"
              header="Crédits"
              :sub-header="`Source du mot '${mot}'`"
              :message="getHtmlCredits()"
          >
          </ion-alert>
        </ion-content>
      </ion-modal>

      <br>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">

import {getWordDocument, wordExists} from "@/functions/dictionnary";
import {isWordStarred, starWord} from "@/functions/favorites";
import {Share} from "@capacitor/share";
import {RemedeConjugateDocument, RemedeWordDocument} from "@/functions/types/remede";
import {defineComponent, ref} from "vue";
import {navigateBackFunction} from "@/functions/types/utils";
import {modalController, useBackButton, useIonRouter} from "@ionic/vue";
import { iosTransitionAnimation } from '@ionic/core';
import WordPreview from "@/components/WordPreview.vue";


export default defineComponent({
  props: ['motRemede', 'hasHeader'],
  setup() {
    const ionRouter = useIonRouter()

    useBackButton(110, () => {
      if (ionRouter.canGoBack()) {
        ionRouter.back(iosTransitionAnimation)
        return
      }
      ionRouter.navigate('/dictionnaire', 'back', 'replace', iosTransitionAnimation)
    });

    return {
      ionRouter
    }
  },
  data() {
    return {
      mot: '',
      currentMode: '',
      currentTemps: '',
      modeTemps: [] as string[],
      currentSujets: [] as string[],
      tab: localStorage.getItem('defaultTab') || 'def' as string,
      document: {
        synonymes: [] as string[],
        antonymes: [] as string[],
        definitions: [],
        references: [],
        ipa: '',
        credits: {
          name: '',
          url: ''
        },
        conjugaisons: {} as RemedeConjugateDocument,
        etymologies: [] as string[]
      } as RemedeWordDocument,
      notFound: false,
      stared: false,
      audioLoading: false,
      navigateBack: function () {
        return false
      } as navigateBackFunction,
      header: this.hasHeader !== undefined ? this.hasHeader: true,
      el: null as any
    }
  },
  mounted() {
    const ionRouter = useIonRouter()
    function navigateBackIfNoHistory() {
      if (!ionRouter.canGoBack()) {
        ionRouter.navigate('/dictionnaire', 'back', 'replace', iosTransitionAnimation)
        return true
      }
      return false
    }

    this.navigateBack = navigateBackIfNoHistory
    this.el = ref(this.$el)
  },
  created() {
    this.loadData(null).then(() => {
      this.listenSpecialTags()
    })
  },
  // unmounted() {
  //   window.dispatchEvent(new Event('reset'))
  // },
  methods: {
    async loadData(mot: null | string) {
      this.mot = mot || this.motRemede
      if (!this.motRemede) {
        this.mot = this.$router.params.mot
      }
      const document = await getWordDocument(this.mot)
      if (document) {
        this.document = document
      } else {
        this.notFound = true
      }

      this.stared = isWordStarred(this.mot)

      if (this.getModes().length > 0) {
        this.currentMode = this.getModes()[0]
        this.modeTemps = this.getTemps(this.currentMode)
        this.currentTemps = this.modeTemps[0]
        this.currentSujets = this.getSujets(this.currentMode, this.currentTemps)
      }
    },
    async shareDefinition() {
      try {
        await Share.share({
          title: `Définition "${this.mot}" sur Remède`,
          text: `La définition du mot "${this.mot}" est sur Remède !`,
          url: `https://remede-app.camarm.fr/dictionnaire/${this.mot}`,
          dialogTitle: 'Partager la définition',
        })
      } catch {
        alert('Fonctionnalité non supportée par votre navigateur')
      }
    },
    goTo(path: string) {
      this.$router.push(path)
    },
    getModes() {
      return Object.keys(this.document.conjugaisons) as string[]
    },
    getTemps(mode: string) {
      return Object.keys(this.document.conjugaisons[mode]) as string[]
    },
    getSujets(mode: string, temps: string) {
      return Object.keys(this.document.conjugaisons[mode][temps]) as string[]
    },
    getFormeVerbale(mode: string, temps: string, sujet: string) {
      return this.document.conjugaisons[mode][temps][sujet]
    },
    readWord() {
      this.audioLoading = true
      const url = 'https://iawll6of90.execute-api.us-east-1.amazonaws.com/production'
      const data = {
        text: this.document.ipa.replaceAll('/', ''),
        voice: 'Mathieu'
      }
      fetch(url, {
        method: 'POST',
        body: JSON.stringify(data)
      }).then(resp => resp.json()).then(audio => {
        const player = new window.Audio()
        player.src = `data:audio/mpeg;base64,${audio}`
        player.play()
        this.audioLoading = false
      })
    },
    changeMode(mode: string) {
      this.currentMode = mode
      this.modeTemps = this.getTemps(this.currentMode)
      this.changeTemps(this.modeTemps[0])
    },
    changeTemps(temps: string) {
      this.currentTemps = temps
      this.currentSujets = this.getSujets(this.currentMode, this.currentTemps)
    },
    getHtmlCredits() {
      return `Ce mot provient de la base Remède. Il suit les conditions et schémas <a href="https://remede.camarm.fr/FR#données-remède" target="_blank">de Remède</a>.`
    },
    open(url: string) {
      window.open(url)
    },
    refreshListeners() {
      window.dispatchEvent(new Event('reset'))
      this.listenSpecialTags()
    },
    async openPreviewModal(word: string) {
      const modal = await modalController.create({
        component: WordPreview,
        componentProps: {
          mot: word
        },
        presentingElement: this.el,
        handle: true
      })
      await modal.present()
    },
    async listenSpecialTags() {
      document.querySelectorAll('reference').forEach(el => {
        const listener = async () => {
          const href = el.getAttribute('href') || ''
          const word = href.replaceAll('https://fr.wiktionary.org/wiki/', '')
          if (await wordExists(word)) {
            // TODO works once, why ?
            await this.openPreviewModal(word)
          } else {
            window.open(href)
          }
        }
        el.addEventListener('click', listener)
        window.addEventListener('reset', () => {
          el.removeEventListener('click', listener)
        })
      })
    },
    parseMeaning(meaning: string) {
      try {
        return meaning.replaceAll('<a', '<reference').replaceAll('</a>', '</reference>')
      } catch (e) {
        return meaning
      }
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

.examples .sources {
  font-size: .8em;
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
</style>