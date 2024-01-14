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
  IonItem
} from "@ionic/vue";
import {
  bookmark,
  bookmarkOutline,
  chevronBackOutline,
  play,
  shareOutline
} from "ionicons/icons";
import WordModal from "@/components/WordModal.vue";
import example from "@/assets/example.svg"
</script>

<template>
  <ion-header :translucent="true">
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
          <ion-button @click="readWord()" :disabled="notFound">
            <ion-icon v-if="!audioLoading" slot="icon-only" :icon="play" color="medium"/>
            <ion-spinner v-else slot="icon-only" name="circles" color="medium"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-segment swipe-gesture :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value">
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
      <div class="definition" :key="def" v-for="def in document.definitions">
        <header>
          <h4 v-if="typeof def.genre !== 'string'">{{ def.genre[0] }}, {{ def.genre[1] }}</h4>
          <h4 v-else-if="def.genre != def.classe && def.classe != ''">{{ def.genre }}, {{ def.classe }}</h4>
          <h4 v-else>{{ def.genre }}</h4>
          <hr>
        </header>
        <ion-list inset class="border-radius" v-if="getModes().length > 0 && def.genre == 'Verbe'">
          <ion-item lines="none" color="light" button @click="tab = 'conj'">
            Ouvrir la conjugaison
          </ion-item>
        </ion-list>
        <div class="content">
          <ul>
            <li :key="meaning" v-for="meaning in def.explications">
              <span v-html="meaning.replaceAll('https://fr.wiktionary.org/wiki/', '/dictionnaire/')" v-if="typeof meaning === 'string'"></span>
              <ul v-else class="ion-padding-start">
                <li :key="subMeaning" v-for="subMeaning in meaning" v-html="subMeaning"></li>
              </ul>
              <sup>
                <ion-icon :id="meaning" :icon="example" color="medium"/>
                <ion-popover :trigger="meaning">
                  <div class="ion-padding">
                    <h3>Exemples</h3>
                    - omzehfouehfzuef
                  </div>
                </ion-popover>
              </sup>
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
          <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: syn }">
            <a>{{ syn }}</a>
          </ion-nav-link>
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
        <li :key="ant" v-for="ant in document.antonymes">
          <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: ant }">
            <a>{{ ant }}</a>
          </ion-nav-link>
        </li>
      </ul>
      <ion-note v-if="document.antonymes.length == 0">Pas d'antonymes référencés</ion-note>
      <ion-note v-else>Via <a target="_blank" :href="`http://www.antonyme.org/antonyme/${mot}`">antonyme.org</a></ion-note>
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
      <ion-note>Via <a target="_blank" :href="`http://conjuguons.fr/conjugaison/verbe/${mot}`">conjuguons.fr</a></ion-note>
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
import {isWordStarred, starWord} from "@/functions/favorites";
import {Share} from "@capacitor/share";
import {RemedeConjugateDocument, RemedeWordDocument} from "@/functions/types/remede";
import {useIonRouter} from "@ionic/vue";
import {defineComponent} from "vue";

export default defineComponent({
  props: ['motRemede'],
  data() {
    return {
      mot: '',
      currentMode: '',
      currentTemps: '',
      modeTemps: [],
      currentSujets: [],
      tab: localStorage.getItem('defaultTab') || 'def',
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
        conjugaisons: {} as RemedeConjugateDocument
      } as RemedeWordDocument,
      notFound: false,
      stared: false,
      audioLoading: false,
      navigateBack() { return }
    }
  },
  mounted() {
    const ionRouter = useIonRouter()
    function navigateBackIfNoHistory() {
      if (!ionRouter.canGoBack()) {
        ionRouter.navigate('/dictionnaire', 'back', 'replace')
      }
    }

    this.navigateBack = navigateBackIfNoHistory
  },
  created() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.mot = this.motRemede
      if (!this.motRemede) {
        this.mot = this.$router.params.mot
      }
      const document = await getWordDocument(this.mot)
      if (document) {
        this.document = await getWordDocument(this.mot)
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
      return Object.keys(this.document.conjugaisons)
    },
    getTemps(mode: string) {
      return Object.keys(this.document.conjugaisons[mode])
    },
    getSujets(mode: string, temps: string) {
      return Object.keys(this.document.conjugaisons[mode][temps])
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
    starWord
  }
})
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

</style>