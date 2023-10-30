<script setup lang="ts">
import {
  IonBackButton,
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonSegment,
  IonSegmentButton,
  IonTitle,
  IonToolbar
} from "@ionic/vue";
import {bookmark, bookmarkOutline, play, shareOutline} from "ionicons/icons";
</script>

<template>
  <ion-header :translucent="true">
    <ion-toolbar>
      <ion-buttons slot="start">
        <ion-back-button defaultHref="/dictionnaire" text="Retour"></ion-back-button>
      </ion-buttons>
      <ion-title>Définition "{{ mot }}"</ion-title>
      <ion-buttons slot="end" @click="shareDefinition()">
        <ion-button @click="starWord(mot); stared = isWordStarred(mot)">
          <ion-icon slot="icon-only" :icon="stared ? bookmark: bookmarkOutline"></ion-icon>
        </ion-button>
        <ion-button>
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
            <ion-icon slot="icon-only" :icon="play" color="medium"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-segment :disabled="notFound" :value="tab" @ionChange="tab = $event.detail.value">
          <ion-segment-button value="def">Définition</ion-segment-button>
          <ion-segment-button value="syn">Synonymes</ion-segment-button>
          <ion-segment-button value="ant">Antonymes</ion-segment-button>
          <ion-segment-button v-if="getModes().length > 0" value="conj">Conjugaison</ion-segment-button>
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
              <span v-html="meaning.replaceAll('https://fr.wiktionary.org/wiki/', '/dictionnaire/')" v-if="typeof meaning === 'string'"></span>
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
      <div class="definition">
        <header>
          <h4>Conjugaison</h4>
          <hr>
        </header>
      </div>
      <br>
      <div v-for="mode in getModes()">
        <details>
          <summary>{{ mode }}</summary>
          <ion-list class="border-radius ion-margin-top">
            <ion-accordion-group>
              <ion-accordion :value="temps" v-for="temps in getTemps(mode)">
                <ion-item class="header" color="light" slot="header">
                  <ion-label>{{ temps }}</ion-label>
                </ion-item>
                <ion-list class="no-radius" slot="content">
                  <ion-item v-for="sujet in getSujets(mode, temps)">
                    <ion-label>
                      <p>{{ sujet }}</p>
                    </ion-label>
                    <ion-label slot="end">
                      {{ getFormeVerbale(mode, temps, sujet) }}
                    </ion-label>
                  </ion-item>
                </ion-list>
              </ion-accordion>
            </ion-accordion-group>
          </ion-list>
        </details>
      </div>
      <br>
      <ion-note>Via <a target="_blank" :href="`http://conjuguons.fr/conjugaison/verbe/${this.mot}`">conjuguons.fr</a></ion-note>
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
        },
        conjugaisons: {}
      },
      notFound: false,
      stared: false
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

    this.stared = isWordStarred(this.mot)
  },
  methods: {
    async shareDefinition() {
      try {
        await Share.share({
          title: `Définition "${this.mot}" sur Remède`,
          text: `La définition du mot "${this.mot}" est sur Remède !`,
          url: `https://remede.camam.fr/dictionnaire/${this.mot}`,
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
      })
    },
    starWord
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

details {
  margin-bottom: .5em;
}

summary {
  font-size: 1.25rem;
  font-weight: 400;
}

ion-item.header {
  transition: .2s ease-in-out;
}

ion-accordion:first-child ion-item.header {
  border-top-right-radius: 12px;
  border-top-left-radius: 12px;
  border-top: solid .55px var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)))
}

ion-accordion:last-child ion-item.header, ion-accordion.accordion-expanded:last-child ion-list.no-radius ion-item:last-child {
  border-bottom-right-radius: 12px;
  border-bottom-left-radius: 12px;
  border-bottom: solid .55px var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

ion-accordion.accordion-expanded:last-child ion-item.header {
  border-radius: 0;
  border-bottom: none;
}

ion-item {
  border-left: solid .55px var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
  border-right: solid .55px var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc)));
}

.border-radius {
  border-radius: 12px;
}

ion-item:not(+ ion-item)::part(native) {
  border-radius: 12px;
}

ion-list.no-radius ion-item:last-child {
  --inner-border-width: 0;
}
</style>