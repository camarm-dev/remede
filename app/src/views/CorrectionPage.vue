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
          <ion-textarea v-if="!locked" auto-grow class="no-border ion-padding-bottom" :maxlength="500" counter :value="content"
                        @ionInput="content = $event.detail.value"
                        placeholder="Écrivez votre texte ici, nous le corrigerons."></ion-textarea>
          <div v-else-if="tab == 'correction'" class="content">
            {{ corrected }}
          </div>
          <div v-else class="content ion-padding-bottom">
            {{ content }}
            <span v-for="correction in corrections">
              <ion-text :id="`correction-${corrections.indexOf(correction)}`" :class="`error ${correction.type}`">{{ correction.mistakeText }}</ion-text>
              <ion-popover :trigger="`correction-${corrections.indexOf(correction)}`" trigger-action="click">
                <ion-content class="ion-padding">
                  <ion-label>
                    <h2>{{ correction.shortDescription }}</h2>
                    <p v-html="correction.longDescription.replaceAll('#!', `<a href=/dictionnaire/${correction.mistakeText}>`).replaceAll('#$', '</a>')"></p>
                  </ion-label>
                  <br>
                  <ion-label>
                    <ion-text color="medium">Remplacer par</ion-text>
                    <br>
                    <ion-text color="primary" v-for="suggested in correction.suggestions">{{ suggested.text }}<br></ion-text>
                  </ion-label>
                </ion-content>
              </ion-popover>
            </span>
          </div>
        </ion-item>
        <ion-item v-if="tab == 'correction'" class="no-border" color="light">
          <ion-buttons slot="end">
            <ion-button @click="copy(corrected)" color="primary">
              Copier&nbsp;<ion-icon :icon="copyOutline"/>
            </ion-button>
            <ion-button color="success" @click="content = corrected; locked = false">
              Utiliser&nbsp;<ion-icon :icon="chevronForwardOutline"/>
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
  IonSegmentButton
} from '@ionic/vue';
import {chevronForwardOutline, copyOutline, lockOpenOutline, pencilOutline, sparkles} from "ionicons/icons";
</script>

<script lang="ts">

export default {
  data() {
    return {
      content: "",
      corrections: [],
      corrected: "",
      locked: false,
      tab: "explain"
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
        console.log(response)
        this.corrections = response.corrections
        this.corrected = response.text
        const originalText = this.content
        for (const correction of this.corrections) {
          console.log(correction)

        }
        this.locked = true
      })
    },
    copy(text: string) {

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
</style>

