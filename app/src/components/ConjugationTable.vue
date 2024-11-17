<script setup lang="ts">

import {IonItem, IonLabel, IonList, IonSelect, IonSelectOption} from "@ionic/vue"
</script>

<template>
  <ion-list inset class="border-radius border">
    <ion-item color="light" lines="full">
      <ion-label slot="start">
        <p>{{ $t('definition.conjugationMode') }}</p>
      </ion-label>
      <ion-label slot="end">
        <p>{{ $t('definition.conjugationTense') }}</p>
      </ion-label>
    </ion-item>
    <ion-item color="light" lines="full">
      <ion-select @ionChange="changeMode($event.target.value)" slot="start" interface="action-sheet" placeholder="Mode" :value="currentMode">
        <ion-select-option :key="mode" v-for="mode in getModes()" :value="mode">{{ mode }}</ion-select-option>
      </ion-select>
      <ion-select @ionChange="changeTense($event.target.value)" slot="end" interface="action-sheet" placeholder="Temps" :value="currentTense">
        <ion-select-option :key="temps" v-for="temps in availableTenses" :value="temps">{{ temps }}</ion-select-option>
      </ion-select>
    </ion-item>
    <ion-item :key="sujet" v-for="sujet in currentSubjects">
      <ion-label>
        <p>{{ replaceSubjects.includes(sujet) ? $t('definition.noSubject'): sujet }}</p>
      </ion-label>
      <ion-label slot="end">
        {{ getVerbalForm(currentMode, currentTense, sujet) }}
      </ion-label>
    </ion-item>
  </ion-list>
</template>

<script lang="ts">
import {PropType} from "vue"

type conjugationData = {
  [key: string]: { // Mode
    [key: string]: { // Tense
      [key: string]: string // Subjects: verbal form
    }
  }
}

export default {
  props: {
    conjugations: {
      type: Object as PropType<conjugationData>,
      required: true
    }
  },
  data() {
    return {
      currentMode: "" as string,
      currentTense: "" as string,
      currentSubjects: [] as string[],
      availableTenses: [] as string[],
      replaceSubjects: ["1PS", "1PP", "2PP"]
    }
  },
  mounted() {
    if (this.getModes().length > 0) {
      this.currentMode = this.getModes()[0]
      this.availableTenses = this.getTemps(this.currentMode)
      this.currentTense = this.availableTenses[0]
      this.currentSubjects = this.getSubjects(this.currentMode, this.currentTense)
    }
  },
  methods: {
    changeMode(mode: string) {
      this.currentMode = mode
      this.availableTenses = this.getTemps(this.currentMode)
      this.changeTense(this.availableTenses[0])
    },
    changeTense(temps: string) {
      this.currentTense = temps
      this.currentSubjects = this.getSubjects(this.currentMode, this.currentTense)
    },
    getModes() {
      return Object.keys(this.conjugations) as string[]
    },
    getTemps(mode: string) {
      return Object.keys(this.conjugations[mode]) as string[]
    },
    getSubjects(mode: string, temps: string) {
      return Object.keys(this.conjugations[mode][temps]) as string[]
    },
    getVerbalForm(mode: string, temps: string, sujet: string) {
      return this.conjugations[mode][temps][sujet]
    }
  }
}
</script>
