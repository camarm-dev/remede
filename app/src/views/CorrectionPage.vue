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

      <ion-list inset class="ion-bg-light">
        <ion-item color="light" class="no-border border-bottom">
          <ion-label slot="start">
            <p>Texte <span v-if="locked">Corrigé</span></p>
          </ion-label>
          <ion-buttons slot="end">
            <ion-button v-if="locked" @click="locked = false" color="primary">
              Éditer&nbsp;<ion-icon :icon="pencilOutline"/>
            </ion-button>
            <ion-button v-else-if="!locked && !loading" @click="correct()" color="success">
              Corriger&nbsp;<ion-icon :icon="sparkles"/>
            </ion-button>
            <ion-button v-else color="success">
              <ion-spinner name="dots" color="success"></ion-spinner>
            </ion-button>
          </ion-buttons>
        </ion-item>
        <ion-item color="light" class="no-border pd-t">
          <ion-textarea v-if="!locked" auto-grow class="no-border ion-padding-bottom" :maxlength="1000" counter :value="content"
                        @ionInput="content = $event.detail.value as string"
                        placeholder="Écrivez votre texte ici, nous le corrigerons."></ion-textarea>
          <div v-else class="content ion-padding-bottom pd-t">
            <span :key="`segment-${explainSegments.indexOf(segment)}`" v-for="segment in explainSegments" :class="segment.correction ? 'correction': 'sentencePart'">
              <span v-if="segment.correction">
                <ion-text :id="`correction-${corrections.indexOf(segment.correction)}`" :class="`error ${segment.correction.rule.category.id} ${segment.ignored ? 'ignored': ''}`">{{ segment.text }}</ion-text>
                <ion-popover :ref="(el) => { popoversOpenStates[`correction-${corrections.indexOf(segment.correction)}`] = el }" :trigger="`correction-${corrections.indexOf(segment.correction)}`" trigger-action="click">
                  <ion-content class="ion-padding" v-if="!segment.ignored">
                    <ion-label v-if="segment.correction.shortMessage != ''">
                      <p class="ion-text-uppercase">{{ segment.correction.rule.category.id }}</p>
                      <h2>{{ segment.correction.shortMessage }}</h2>
                      <p>{{ segment.correction.message }}</p>
                    </ion-label>
                    <ion-label v-else>
                      <h3>{{ segment.correction.message }}</h3>
                    </ion-label>
                    <br>
                    <ion-label>
                      <ion-text color="medium">Remplacer par</ion-text>
                    </ion-label>
                    <br>
                    <ion-button size="small" color="primary" @click="setSegmentAsText(segment, suggested.value); closePopover(`correction-${corrections.indexOf(segment.correction)}`)" :key="`suggestion-${corrections.indexOf(segment.correction)}-${suggested}`" v-for="suggested in segment.correction.replacements">{{ suggested.value }}<br></ion-button>
                    <ion-button size="small" @click="ignoreError(segment.text, segment.correction); setSegmentAsText(segment, segment.text); closePopover(`correction-${corrections.indexOf(segment.correction)}`)" color="light">Ignorer <ion-icon :icon="closeOutline"/></ion-button>
                  </ion-content>
                  <ion-content class="ion-padding" v-else>
                    <ion-label>
                      <p>Erreur ignorée.</p>
                    </ion-label>
                    <br>
                    <ion-button @click="removeException(segment.text, segment.correction); setSegmentAsText(segment, segment.text); closePopover(`correction-${corrections.indexOf(segment.correction)}`)" color="danger" class="ion-no-margin" size="small">Enlever l'exception <ion-icon :icon="closeOutline"/></ion-button>
                  </ion-content>
                </ion-popover>
              </span>
              <span v-else v-html="segment.text.replaceAll('\n', '<br>')"/>
            </span>
          </div>
        </ion-item>
        <ion-item v-if="locked" class="no-border" color="light">
          <ion-buttons slot="end">
            <ion-button @click="copy(getPartiallyCorrectedContent())" color="primary">
              Copier&nbsp;<ion-icon :icon="copyOutline"/>
            </ion-button>
            <ion-button color="success" @click="content = getPartiallyCorrectedContent(); locked = false">
              Réutiliser&nbsp;<ion-icon :icon="chevronForwardOutline"/>
            </ion-button>
          </ion-buttons>
        </ion-item>
      </ion-list>
      <div class="ion-padding">
        <ion-note>
          Correction grâce à <a href="https://languagetool.org" target="_blank">Languagetool</a>, <i>hébergé par Remède</i>.
        </ion-note>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonMenuButton,
  IonPage,
  IonTitle,
  IonToolbar,
  IonTextarea,
  IonText,
  IonButton,
  IonItem,
  IonLabel,
  IonPopover,
  IonList,
  IonNote,
  IonSpinner
} from "@ionic/vue"
import {chevronForwardOutline, copyOutline, pencilOutline, sparkles, closeOutline} from "ionicons/icons"
</script>

<script lang="ts">
import { Clipboard } from "@capacitor/clipboard"
import {ExplainSegment, LanguageToolCorrection} from "@/functions/types/languagetool"

export default {
  data() {
    return {
      content: "",
      corrections: [] as LanguageToolCorrection[],
      locked: false,
      loading: false,
      explainSegments: [] as ExplainSegment[],
      popoversOpenStates: {} as { [key: string]: any },
      ignoredErrors: [] as any[]
    }
  },
  mounted() {
    this.loadExceptions()
    const url = new URLSearchParams(location.search)
    const data = url.get("data")
    if (data) {
      const content = data.replaceAll("?data=", "")
      this.content = content
      if (content != "") {
        this.correct()
      }
    }
  },
  methods: {
    saveWordToDictionary() {
      // TODO, dict remede
    },
    deleteWordFromDictionary() {
      // TODO, dict remede
    },
    getWordDictionary() {
      // TODO, dict remede
    },
    ignoreError(text: string, correction: LanguageToolCorrection) {
      this.ignoredErrors.push({
        text: text,
        error: correction.rule.id
      })
      this.saveExceptions()
    },
    isErrorIgnored(text: string, correction: LanguageToolCorrection) {
      return this.ignoredErrors.some(element => {
        return element.text == text && element.error == correction.rule.id
      })
    },
    removeException(text: string, correction: LanguageToolCorrection) {
      this.ignoredErrors = this.ignoredErrors.map(element => {
          if (element.text == text && element.error == correction.rule.id) {
            return false
          }
          return true
      })
      this.saveExceptions()
    },
    loadExceptions() {
      this.ignoredErrors = JSON.parse(localStorage.getItem('correctionExceptions') || "[]")
    },
    saveExceptions() {
      localStorage.setItem("correctionExceptions", JSON.stringify(this.ignoredErrors))
    },
    correct() {
      this.loading = true
      this.popoversOpenStates = {}

      const url = "https://remede-corrector.camarm.fr/v2/check"
      const body = new FormData()
      body.set("text", this.content)
      body.set("language", "fr")
      body.set("motherTongue", "fr")
      body.set("allowIncompleteResults", "false")
      body.set("mode", "allButTextLevelOnly")

      fetch(url, {
        method: "POST",
        body: new URLSearchParams(body as any),
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }).then(resp => resp.json()).then(response => {
        this.corrections = response.matches
        const originalText = this.content
        let lastIndex = 0
        const segmentedText = [] as ExplainSegment[]
        for (const correction of this.corrections) {
          const startIndex = correction.offset
          const endIndex = correction.offset + correction.length
          correction.replacements = correction.replacements.slice(0, 4)
          segmentedText.push({
            correction: false as any as LanguageToolCorrection,
            text: originalText.slice(lastIndex, startIndex),
            ignored: false
          })
          const text = correction.context.text.slice(correction.context.offset, correction.context.offset + correction.context.length)
          segmentedText.push({
            correction: correction,
            text: text,
            ignored: this.isErrorIgnored(text, correction)
          })
          lastIndex = endIndex
        }

        segmentedText.push({
          correction: false as any as LanguageToolCorrection,
          text: originalText.slice(lastIndex, originalText.length),
          ignored: false
        })

        this.explainSegments = segmentedText
        this.locked = true
        this.loading = false
      })
    },
    copy(text: string) {
      Clipboard.write({
        string: text
      })
    },
    getPartiallyCorrectedContent() {
      return this.explainSegments.map(obj => {
        return obj.correction ? obj.correction.context.text.slice(obj.correction.context.offset, obj.correction.context.offset + obj.correction.context.length): obj.text
      }).join("")
    },
    setSegmentAsText(segment: ExplainSegment, text: string) {
      this.explainSegments[this.explainSegments.indexOf(segment)] = { correction: false as any as LanguageToolCorrection, text: text, ignored: false }
    },
    closePopover(refName: string) {
      this.popoversOpenStates[refName].$el.dismiss()
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

.error.CAT_GRAMMAIRE, .error.TYPOS {
  text-decoration: underline wavy var(--ion-color-warning);
}

.error.CAT_PONCTUATION {
  text-decoration: underline wavy var(--ion-color-success-shade);
}

.error.ignored {
  text-decoration: underline wavy var(--ion-color-medium-shade) !important;
}

.correction + .correction {
  margin-left: .2em;
}

.border-bottom {
  border-bottom: var(--color-medium-light) .55px solid;
  box-sizing: content-box;
}

.pd-t {
  box-sizing: border-box;
  padding-top: .5em
}

.ion-bg-light {
  background: var(--ion-color-light);
}
</style>

