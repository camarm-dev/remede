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
          <ion-title size="large">Rimes</ion-title>
        </ion-toolbar>
        <ion-toolbar>
          <ion-searchbar :value="query" @ionInput="handleSearchBarInput($event.detail.value as string)" placeholder="Entrez un mot"></ion-searchbar>
          <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
        </ion-toolbar>
      </ion-header>


      <div class="ion-padding" v-if="!failed && rhymes.length === 0">
        <ion-note>Aucune rimes trouvées dans notre base avec ce mot. Utilisez la barre de recherche ci-dessus.</ion-note>
      </div>

      <div class="ion-padding" v-if="failed">
        <ion-note>La recherche dans le dictionnaire des rimes a échouée.</ion-note>
      </div>
      <ion-content v-else>
        <ul>
          <li :key="r[0].toString()" v-for="r in rhymes">{{r}}</li>
        </ul>
      </ion-content>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonMenuButton,
  IonPage,
  IonTitle,
  IonToolbar,
  IonProgressBar,
  IonSearchbar
} from "@ionic/vue"
</script>

<script lang="ts">
import {getWordRimes} from "@/functions/dictionnary"

export default {
  props: ["queryWord"],
  data() {
    return {
      loading: false,
      failed: false,
      rhymes: [] as any[],
      query: "",
      // Ignoring linter error about empty function (@typescript-eslint/no-empty-function)
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      searchTimeout: window.setTimeout(() => {}, 500),
      maxSyllabes: 0,
      minSyllabes: 0,
      elide: false
    }
  },
  mounted() {
    if (this.queryWord) {
      this.query = this.queryWord
      this.searchRhymes()
    }
  },
  methods: {
    async searchRhymes() {
      this.loading = true
      try {
        const {rhymes, success} = await getWordRimes(this.query, this.maxSyllabes == 0 ? undefined: this.maxSyllabes, this.minSyllabes == 0 ? undefined: this.minSyllabes, this.elide)
        this.rhymes = rhymes
        console.log(rhymes)
        this.failed = !success
      } catch (e) {
        console.error(e)
        this.failed = true
      }
      this.loading = false
    },
    handleSearchBarInput(query: string) {
      this.query = query
      clearTimeout(this.searchTimeout)
      this.searchTimeout = window.setTimeout(() => {
        this.searchRhymes()
      }, 500)
    },
  }
}
</script>
<style>
</style>
