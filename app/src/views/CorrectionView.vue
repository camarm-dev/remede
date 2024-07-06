<template>
  <ion-page ref="page">
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-buttons slot="end">
          <ion-button id="open-exceptions-modal">
            <ion-icon slot="icon-only" :icon="languageOutline"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">{{ $t('corrector') }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset class="ion-bg-light corrector">
        <ion-item color="light" class="no-border border-bottom">
          <ion-label slot="start">
            <p v-if="locked">{{ $t('correctionPage.corrected')}}</p>
            <p v-else>{{ $t('correctionPage.text')}}</p>
          </ion-label>
          <ion-buttons slot="end">
            <ion-item color="light" lines="none" v-if="hasDialect($i18n.locale)">
              <ion-select label="" :value="selectedDialect" @ionChange="selectedDialect = $event.target.value" interface="popover">
                <ion-select-option v-for="dialect in availableDialects">{{ dialect }}</ion-select-option>
              </ion-select>
            </ion-item>
            <ion-button v-if="locked" @click="locked = false" color="primary">
              {{ $t('correctionPage.edit') }}&nbsp;<ion-icon :icon="pencilOutline"/>
            </ion-button>
            <ion-button v-else-if="!locked && !loading" @click="correct()" color="success">
              {{ $t('correctionPage.correct') }}&nbsp;<ion-icon :icon="sparkles"/>
            </ion-button>
            <ion-button v-else color="success">
              <ion-spinner name="dots" color="success"></ion-spinner>
            </ion-button>
          </ion-buttons>
        </ion-item>
        <ion-item color="light" class="no-border pd-t">
          <ion-textarea v-if="!locked" auto-grow class="no-border ion-padding-bottom" :maxlength="5000" counter :value="content"
                        @ionInput="content = $event.detail.value as string"
                        :placeholder="$t('correctionPage.placeholder')"></ion-textarea>
          <div v-else class="content correction-content ion-padding-bottom pd-t">
            <span :key="`segment-${explainSegments.indexOf(segment)}`" v-for="segment in explainSegments" :class="segment.correction ? 'correction': 'sentencePart'">
              <span v-if="segment.correction">
                <ion-text :id="`correction-${corrections.indexOf(segment.correction)}`" :class="`error ${segment.correction.rule.category.id} ${segment.ignored ? 'ignored': ''}`">{{ segment.text }}</ion-text>
                <ion-popover :ref="(el) => { modalsOpenStates[`correction-${corrections.indexOf(segment.correction)}`] = el }" :trigger="`correction-${corrections.indexOf(segment.correction)}`" trigger-action="click">
                  <ion-content class="ion-padding" v-if="!segment.ignored">
                    <ion-label v-if="segment.correction.shortMessage != ''">
                      <p class="ion-text-uppercase">{{ segment.correction.rule.category.name }}</p>
                      <h2>{{ segment.correction.shortMessage }}</h2>
                      <p>{{ segment.correction.message }}</p>
                    </ion-label>
                    <ion-label v-else>
                      <p class="ion-text-uppercase">{{ segment.correction.rule.category.name }}</p>
                      <h3>{{ segment.correction.message }}</h3>
                    </ion-label>
                    <br>
                    <ion-label>
                      <ion-text color="medium">{{ $t('correctionPage.replaceBy') }}</ion-text>
                    </ion-label>
                    <br>
                    <ion-button :title="suggested.value" size="small" :color="suggested.value == '' ? 'danger': 'primary'" @click="setSegmentAsText(segment, suggested.value); closeModal(`correction-${corrections.indexOf(segment.correction)}`)" :key="`suggestion-${corrections.indexOf(segment.correction)}-${suggested}`" v-for="suggested in segment.correction.replacements">{{ suggested.value == '' ? 'Supprimer': suggested.value }}<br></ion-button>
                    <ion-button size="small" @click="ignoreError(segment.text, segment.correction); setSegmentAsText(segment, segment.text); closeModal(`correction-${corrections.indexOf(segment.correction)}`)" color="light">{{ $t('ignore') }} <ion-icon :icon="closeOutline"/></ion-button>
                  </ion-content>
                  <ion-content class="ion-padding" v-else>
                    <ion-label>
                      <p>{{ $t('correctionPage.ignoredError') }}</p>
                    </ion-label>
                    <br>
                    <ion-button @click="removeException(segment.text, segment.correction); setSegmentAsText(segment, segment.text); closeModal(`correction-${corrections.indexOf(segment.correction)}`)" color="danger" class="ion-no-margin" size="small">{{ $t('correctionPage.deleteException') }} <ion-icon :icon="closeOutline"/></ion-button>
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
              {{ $t('correctionPage.copy') }}&nbsp;<ion-icon :icon="copyOutline"/>
            </ion-button>
            <ion-button color="success" @click="content = getPartiallyCorrectedContent(); locked = false">
              {{ $t('correctionPage.recorrect') }}&nbsp;<ion-icon :icon="chevronForwardOutline"/>
            </ion-button>
          </ion-buttons>
        </ion-item>
      </ion-list>

      <div v-if="openedFromSelection && !loading && explainSegments.length > 0">
        <div class="ion-padding">
          <ion-button expand="block" @click="getBackToSelection()" color="primary">
            <ion-icon :icon="returnUpBackOutline" class="ion-margin-end"/>
            <span v-if="textSelectionReadOnly">{{ $t('correctionPage.copyAndBackToApp') }}</span>
            <span v-else>{{ $t('correctionPage.backToApp') }}</span>
          </ion-button>
        </div>
        <div class="ion-padding">
          <ion-note v-if="textSelectionReadOnly">
            <ion-icon :icon="informationCircleOutline"/>
            {{ $t('correctionPage.copyAndBackToAppDisclaimer') }}
          </ion-note>
          <ion-note v-else>
            <ion-icon :icon="informationCircleOutline"/>
            {{ $t('correctionPage.backToAppDisclaimer') }}
          </ion-note>
        </div>
      </div>

      <div class="ion-padding">
        <ion-note>
          {{ $t('correctionPage.correctionPoweredBy') }} <a href="https://languagetool.org" target="_blank">Languagetool</a>, <i>{{ $t('correctionPage.hostedByRemede') }}</i>.
        </ion-note>
      </div>

      <ion-modal :ref="(el) => { modalsOpenStates['exceptionsModal'] = el }" trigger="open-exceptions-modal" :presenting-element="pageElement">
        <ion-header>
          <ion-toolbar>
            <ion-title>{{ $t('correctionPage.exceptions') }}</ion-title>
            <ion-buttons slot="end">
              <ion-button @click="closeModal('exceptionsModal')">{{ $t('close') }}</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content>
          <ion-note v-if="ignoredErrors.length == 0">
            {{ $t('correctionPage.noExceptions') }}
          </ion-note>
          <ion-list class="fullwidth" inset>
            <ion-item v-for="error in ignoredErrors" color="light" :key="error.text">
              <ion-label>
                <h2>"{{ error.text }}"</h2>
                <p class="ion-color-base">{{ error.summary }}</p>
              </ion-label>
              <ion-icon @click="removeException(error.text, { rule: { id: error.error } })" slot="end" color="danger" :icon="trashOutline"/>
            </ion-item>
          </ion-list>
        </ion-content>
      </ion-modal>
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
  IonSpinner,
  IonModal,
  IonSelect,
  IonSelectOption
} from "@ionic/vue"
import {
  chevronForwardOutline,
  copyOutline,
  pencilOutline,
  sparkles,
  closeOutline,
  trashOutline,
  languageOutline,
  informationCircleOutline,
  returnUpBackOutline
} from "ionicons/icons"
import { hasDialect } from "@/functions/locales";
</script>

<script lang="ts">
import { Clipboard } from "@capacitor/clipboard"
import {ExplainSegment, LanguageToolCorrection} from "@/functions/types/languagetool"
import SetResult from "@/functions/plugins/setResult"
import locales from "@/functions/locales";

export default {
  data() {
    const locale = this.$i18n.locale
    const availableDialects = locales.dialects[locale] || [] as string[]
    return {
      content: "",
      corrections: [] as LanguageToolCorrection[],
      locked: false,
      loading: false,
      explainSegments: [] as ExplainSegment[],
      modalsOpenStates: {} as { [key: string]: any },
      ignoredErrors: [] as any[],
      pageElement: null as any,
      openedFromSelection: false,
      textSelectionReadOnly: false,
      availableDialects: availableDialects as string[],
      selectedDialect: availableDialects.at(0) || this.$i18n.locale
    }
  },
  mounted() {
    this.loadExceptions()
    this.pageElement = this.$refs.page.$el
    const url = new URLSearchParams(location.search)
    const data = url.get("data")
    const readonly = url.get("readonly")
    if (data) {
      const content = data
      this.content = content.replaceAll("<newline>", "\n")
      if (content != "") {
        this.openedFromSelection = true
        this.textSelectionReadOnly = readonly ? readonly == "true": false
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
        error: correction.rule.id,
        summary: correction.rule.description
      })
      this.saveExceptions()
    },
    isErrorIgnored(text: string, correction: LanguageToolCorrection) {
      return this.ignoredErrors.some(element => {
        return element.text == text && element.error == correction.rule.id
      })
    },
    removeException(text: string, correction: LanguageToolCorrection) {
      this.ignoredErrors = this.ignoredErrors.filter(element => {
          return !(element.text == text && element.error == correction.rule.id)
      })
      this.saveExceptions()
    },
    loadExceptions() {
      this.ignoredErrors = JSON.parse(localStorage.getItem("correctionExceptions") || "[]")
    },
    saveExceptions() {
      localStorage.setItem("correctionExceptions", JSON.stringify(this.ignoredErrors))
    },
    getBackToSelection() {
      const result = this.getPartiallyCorrectedContent()
      if (this.textSelectionReadOnly) {
        this.copy(result)
      }
      SetResult.sendActiveRemedeResult({ value: result })
    },
    correct() {
      this.loading = true
      this.modalsOpenStates = {}

      const url = "https://remede-corrector.camarm.fr/v2/check"
      const body = new FormData()
      body.set("text", this.content)
      body.set("language", this.selectedDialect)
      body.set("motherTongue", this.$i18n.locale)
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
    closeModal(refName: string) {
      this.modalsOpenStates[refName].$el.dismiss()
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
  text-decoration: underline;
  text-decoration-color: var(--ion-color-danger);
  text-decoration-style: wavy;
  cursor: pointer;
}

.error.CAT_GRAMMAIRE, .error.TYPOS {
  text-decoration-color: var(--ion-color-warning);
}

.error.CAT_PONCTUATION {
  text-decoration-color: var(--ion-color-success-shade);
}

.error.ignored {
  text-decoration-color: var(--ion-color-medium-shade) !important;
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

