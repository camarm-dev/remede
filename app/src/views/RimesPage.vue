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
        </ion-toolbar>
        <ion-toolbar>
          <ion-item class="item-carousel ion-text-wrap" lines="none">
            <ion-chip class="transparent">
              <ion-icon :icon="filterCircleOutline"></ion-icon>
              <ion-label>Filtres</ion-label>
            </ion-chip>
            <ion-chip v-if="minSyllabes != 0 || maxSyllabes != 0">
              <ion-label>de {{ minSyllabes }} {{ maxSyllabes > 0 ? ` à ${maxSyllabes}`: '' }} syllabe(s)</ion-label>
              <ion-icon :icon="closeOutline" @click="minSyllabes = 0; maxSyllabes = 0; handleSearchBarInput(query)"/>
            </ion-chip>
            <ion-chip v-if="elide">
              <ion-label>Elidables</ion-label>
              <ion-icon :icon="closeOutline" @click="elide = false; handleSearchBarInput(query)"/>
            </ion-chip>
            <ion-chip class="outline" id="open-filters">
              <ion-label>Ajouter un filtre</ion-label>
              <ion-icon :icon="addOutline"/>
            </ion-chip>
            <ion-popover trigger="open-filters">
              <ion-item lines="none">
                <ion-label>Nombre de syllabes</ion-label>
              </ion-item>
              <ion-item>
                <ion-input :value="minSyllabes" @input="minSyllabes = $event.target.value; handleSearchBarInput(query)" label-placement="stacked" placeholder="0" type="number" label="Minimum"></ion-input>
                <ion-input :value="maxSyllabes" @input="maxSyllabes = $event.target.value; handleSearchBarInput(query)" label-placement="stacked" placeholder="0" type="number" label="Maximum"></ion-input>
              </ion-item>
              <ion-item lines="none">
                <ion-label>Rimes elidables</ion-label>
                <ion-checkbox :checked="elide" @ionChange="elide = $event.detail.checked"/>
              </ion-item>
            </ion-popover>
          </ion-item>
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
        <ion-list>
          <ion-item-group>
            <ion-item-divider>
              <ion-label>
                Mot
              </ion-label>
              <ion-label>
                Phonème
              </ion-label>
              <ion-label slot="end">
                <ion-icon :icon="chevronBackOutline"/>
                <ion-note>Page {{ page + 1 }}</ion-note>
                <ion-icon :icon="chevronForwardOutline"/>
              </ion-label>
            </ion-item-divider>
            <ion-item v-for="word in rhymes" :key="word.toString()">
              <ion-label>{{ word }}</ion-label>
            </ion-item>
          </ion-item-group>
        </ion-list>
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
  IonSearchbar, IonItem, IonIcon, IonChip, IonLabel, IonNote, IonCheckbox, IonPopover, IonInput, IonList, IonItemGroup, IonItemDivider
} from "@ionic/vue"
import {addOutline, chevronBackOutline, chevronForwardOutline, closeOutline, filterCircleOutline} from "ionicons/icons";
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
      elide: false,
      page: 0
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
        for (const element of rhymes) {
          this.rhymes.push(element)
        }
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
        this.rhymes = []
        this.page = 0
        this.searchRhymes()
      }, 500)
    },
  }
}
</script>
<style>
ion-chip.outline {
  --background: #fff;
  border: rgba(var(--ion-text-color-rgb, 0, 0, 0), 0.12) .55px solid;
}

.transparent {
  background: #fff
}

</style>
