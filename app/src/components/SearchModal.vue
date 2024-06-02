<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonItem,
  IonPage,
  IonSearchbar,
  IonToolbar,
  IonLabel,
  IonBackButton
} from "@ionic/vue"
</script>

<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button text="Retour" default-href="/dictionnaire"></ion-back-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-searchbar disabled :value="mot"/>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-list class="search-results">
        <ion-item button :key="result" v-for="result in results" @click="goTo(`/dictionnaire/${result}`)">
          <ion-label>
            {{ result }}
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {getSearchResults} from "@/functions/dictionnary"
import {defineComponent} from "vue"
import {useIonRouter} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"
import {navigateBackFunction} from "@/functions/types/utils"


export default defineComponent({
  data() {
    return {
      mot: "" as string,
      results: [] as string[],
      goTo: function (path: string): void {
        console.log(path)
        return
      }
    }
  },
  mounted() {
    this.mot = this.$route.params.mot as string
    this.loadData()

    const ionRouter = useIonRouter()

    function goTo(path: string) {
      ionRouter.push(path, iosTransitionAnimation)
    }

    this.goTo = goTo
  },
  methods: {
    async loadData() {
      this.results = await getSearchResults(this.mot)
    }
  }
})
</script>
