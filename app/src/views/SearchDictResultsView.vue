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
  IonBackButton,
  IonList
} from "@ionic/vue"
</script>

<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button :text="$t('back')" default-href="/dictionary"></ion-back-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-searchbar disabled :value="word"/>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-list class="search-results">
        <ion-item
            :key="getResultId(result)"
            v-for="result in results"
            @click="$router.push({
                name: 'dictServersDefinition',
                params: {
                  definition: JSON.stringify(result)
                }
              })"
            button
        >
          <ion-label>
            <h2>{{ result.word }}</h2>
            <span class="small">dict://{{ result.server }}, {{ result.database }}</span>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {defineComponent} from "vue"
import {useIonRouter} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"
import {DictDefinition} from "@/functions/dictProtocol"

export default defineComponent({
  data() {
    return {
      results: [] as DictDefinition[],
      word: "",
      goTo: function (path: string): void {
        console.log(path)
        return
      }
    }
  },
  mounted() {
    this.results = JSON.parse(this.$route.params.results as string) as DictDefinition[]
    this.word = this.$route.params.word as string

    const ionRouter = useIonRouter()

    function goTo(path: string) {
      ionRouter.push(path, iosTransitionAnimation)
    }

    this.goTo = goTo
  },
  methods: {
    getResultId(result: DictDefinition) {
      return result.word + "-" + result.databaseId + "-" + result.server
    }
  }
})
</script>
