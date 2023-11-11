<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Correcteur</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset>
        <ion-item color="light" class="no-border">
          <ion-label slot="start">
            <p>Texte <span v-if="locked">Corrigé</span></p>
          </ion-label>
          <ion-buttons slot="end">
            <ion-button v-if="locked" @click="locked = false" color="primary">
              Éditer&nbsp;<ion-icon :icon="pencilOutline"/>
            </ion-button>
            <ion-button v-else @click="correct()" color="success">
              Corriger&nbsp;<ion-icon :icon="sparkles"/>
            </ion-button>
          </ion-buttons>
        </ion-item>
        <ion-item color="light" class="no-border" v-if="locked">
          <ion-segment @ionChange="tab = $event.detail.value" :value="tab">
            <ion-segment-button value="explain">Explications</ion-segment-button>
            <ion-segment-button value="correction">Corrigé</ion-segment-button>
          </ion-segment>
        </ion-item>
        <ion-item color="light" class="no-border">
          <ion-textarea v-if="!locked" auto-grow class="no-border ion-padding-bottom" :maxlength="360" counter :value="content"
                        @ionInput="content = $event.detail.value"
                        placeholder="Écrivez votre texte ici, nous le corrigerons."></ion-textarea>
          <div v-else-if="tab == 'correction'" class="content">
            {{ corrected }}
          </div>
          <div v-else class="content ion-padding-bottom">
            <span v-for="segment in explainSegments" :class="segment.correction ? 'correction': 'sentencePart'">
              <span v-if="segment.correction">
                <ion-text :id="`correction-${corrections.indexOf(segment.correction)}`" :class="`error ${segment.correction.type}`">{{ segment.correction.mistakeText }}</ion-text>
                <ion-popover :trigger="`correction-${corrections.indexOf(segment.correction)}`" trigger-action="click">
                  <ion-content class="ion-padding">
                    <ion-label>
                      <h2>{{ segment.correction.shortDescription }}</h2>
                      <p v-html="segment.correction.longDescription.replaceAll('#!', `<a href=/dictionnaire/${segment.correction.mistakeText}>`).replaceAll('#$', '</a>')"></p>
                    </ion-label>
                    <br>
                    <ion-label>
                      <ion-text color="medium">Remplacer par</ion-text>
                      <br>
                      <ion-text @click="explainSegments[explainSegments.indexOf(segment)] = { correction: false, text: suggested.text }" color="primary" v-for="suggested in segment.correction.suggestions">{{ suggested.text }}<br></ion-text>
                    </ion-label>
                  </ion-content>
                </ion-popover>
              </span>
              {{ segment.text }}
            </span>
          </div>
        </ion-item>
        <ion-item v-if="locked" class="no-border" color="light">
          <ion-buttons slot="end">
            <ion-button @click="copy(tab == 'correction' ? corrected: getPartiallyCorrectedContent())" color="primary">
              Copier&nbsp;<ion-icon :icon="copyOutline"/>
            </ion-button>
            <ion-button color="success" @click="content = tab == 'correction' ? corrected: getPartiallyCorrectedContent(); locked = false">
              Réutiliser&nbsp;<ion-icon :icon="chevronForwardOutline"/>
            </ion-button>
          </ion-buttons>
        </ion-item>
      </ion-list>
      <ion-note class="ion-padding">
        Correction grâce à <a href="https://reverso.net" target="_blank">Reverso</a>.
      </ion-note>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader, IonIcon,
  IonMenuButton,
  IonPage,
  IonTitle,
  IonToolbar,
  IonTextarea,
  IonText,
  IonSegment,
  IonSegmentButton,
  IonButton,
  IonItem,
  IonLabel,
  IonPopover,
  IonList,
  IonNote
} from '@ionic/vue';
import {chevronForwardOutline, copyOutline, pencilOutline, sparkles} from "ionicons/icons";
</script>

<script lang="ts">
import { Clipboard } from '@capacitor/clipboard';
import {ExplainSegment, ReversoCorrection} from "@/functions/types/reverso";

export default {
  data() {
    return {
      content: "",
      corrections: [] as ReversoCorrection[],
      corrected: "",
      locked: false,
      tab: "explain",
      explainSegments: [] as ExplainSegment[]
    }
  },
  methods: {
    correct() {
      const url = 'https://orthographe.reverso.net/api/v1/Spelling/'
      const data = {
        "englishDialect": "indifferent",
        "autoReplace": true,
        "getCorrectionDetails": true,
        "interfaceLanguage": "fr",
        "locale": "",
        "language": "fra",
        "text": this.content,
        "originalText": "",
        "spellingFeedbackOptions": {"insertFeedback": true, "userLoggedOn": false},
        "origin": "interactive",
        "isHtml": false,
        "IsUserPremium": false
      }

      fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/*+json'
        }
      }).then(resp => resp.json()).then(response => {
        this.corrections = response.corrections
        this.corrected = response.text
        let originalText = this.content
        let lastIndex = 0
        let segmentedText = [] as ExplainSegment[]
        for (const correction of this.corrections) {
          const startIndex = correction.startIndex
          const endIndex = correction.endIndex
          segmentedText.push({
            correction: false,
            text: originalText.slice(lastIndex, lastIndex == 0 ? startIndex: startIndex - 1)
          })
          segmentedText.push({
            correction: correction,
            text: ''
          })
          lastIndex = endIndex
        }

        this.explainSegments = segmentedText
        this.locked = true
      })
    },
    copy(text: string) {
      Clipboard.write({
        string: text
      });
    },
    getPartiallyCorrectedContent() {
      return this.explainSegments.map(obj => {
        return obj.correction ? obj.correction.mistakeText: obj.text
      }).join('')
    }
  }
}
</script>

<style>
.no-border {
  --inner-border-width: 0;
  --border-width: 0;
}

.error {
  text-decoration: underline wavy var(--ion-color-danger);
}

.error.Grammar {
  text-decoration: underline wavy var(--ion-color-warning);
}

.error.Punctuation {
  text-decoration: underline wavy var(--ion-color-success-shade);
}

.correction + .correction {
  margin-left: .2em;
}
</style>

