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
  IonList,
  IonInfiniteScroll,
  IonInfiniteScrollContent
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
        <ion-searchbar disabled :value="mot"/>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-list class="search-results">
        <ion-item button :key="result" v-for="result in results" @click="goTo(`/dictionary/${result}`)">
          <ion-label>
            {{ result }}
          </ion-label>
        </ion-item>
      </ion-list>
      <ion-infinite-scroll v-if="results.length > 0" @ionInfinite="loadMore">
        <ion-infinite-scroll-content></ion-infinite-scroll-content>
      </ion-infinite-scroll>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {getSearchResults} from "@/functions/dictionnary"
import {defineComponent} from "vue"
import {InfiniteScrollCustomEvent, useIonRouter} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"

export default defineComponent({
  data() {
    return {
      mot: "" as string,
      results: [] as string[],
      page: 0,
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
      const results = await getSearchResults(this.mot, this.page)
      for (const element of results) {
        this.results.push(element)
      }
    },
    async loadMore(event: InfiniteScrollCustomEvent) {
      this.page += 1
      this.loadData().then(() => {
        event.target.complete()
      })
    }
  }
})
</script>
