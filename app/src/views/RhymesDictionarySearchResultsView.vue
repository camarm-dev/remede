<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button text="Retour" default-href="/rimes"></ion-back-button>
        </ion-buttons>
        <ion-title v-if="!failed && query != ''">Rimes "{{ query }}"</ion-title>
        <ion-title v-else>Rimes</ion-title>
        <ion-buttons slot="end" collapse>
          <ion-button @click="scrollToTop()">
            <ion-icon slot="icon-only" :icon="chevronUpOutline"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" ref="content">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-toolbar>
            <ion-searchbar :value="query" disabled placeholder="Entrez un mot"></ion-searchbar>
            <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
          </ion-toolbar>
          <ion-item class="item-carousel ion-text-wrap" lines="none">
            <ion-chip class="transparent">
              <ion-icon :icon="filterCircleOutline"></ion-icon>
              <ion-label>Filtres</ion-label>
            </ion-chip>
            <ion-chip v-if="quality != 0">
              <ion-label v-if="quality == 1">Rimes pauvres</ion-label>
              <ion-label v-if="quality == 2">Rimes suffisantes</ion-label>
              <ion-label v-if="quality == 3">Rimes riches</ion-label>
              <ion-icon :icon="closeOutline" @click="quality = 0; search()"/>
            </ion-chip>
            <ion-chip v-if="nature.length > 0">
              <ion-label><span :key="type" v-for="type in nature">{{ type.toLowerCase() }}. {{ nature.indexOf(type) + 1 < nature.length ? ',': '' }}</span></ion-label>
              <ion-icon :icon="closeOutline" @click="nature = []; search()"/>
            </ion-chip>
            <ion-chip v-if="elide">
              <ion-label>Avec élide</ion-label>
              <ion-icon :icon="closeOutline" @click="elide = false; search()"/>
            </ion-chip>
            <ion-chip v-if="feminine">
              <ion-label>Féminines seulement</ion-label>
              <ion-icon :icon="closeOutline" @click="feminine = false; search()"/>
            </ion-chip>
            <div v-if="minSyllabes != 0 || maxSyllabes != 0">
              <ion-chip id="open-syllabes-selector">
                <ion-label>de {{ minSyllabes }} {{ maxSyllabes > 0 ? ` à ${maxSyllabes}`: '' }} syllabe(s)</ion-label>
                <ion-icon :icon="closeOutline" @click="minSyllabes = 0; maxSyllabes = 0; search()"/>
              </ion-chip>
              <ion-picker trigger="open-syllabes-selector" :columns="syllabesPickerColumns" :buttons="syllabesPickerButtons"></ion-picker>
            </div>
            <div v-else>
              <ion-chip class="outline" id="open-syllabes-selector">
                <ion-label>Nb. syllabes</ion-label>
                <ion-icon :icon="chevronExpandOutline"/>
              </ion-chip>
              <ion-picker trigger="open-syllabes-selector" :columns="syllabesPickerColumns" :buttons="syllabesPickerButtons"></ion-picker>
            </div>
            <ion-chip class="outline" id="open-filters">
              <ion-label>Ajouter un filtre</ion-label>
              <ion-icon :icon="addOutline"/>
            </ion-chip>
            <ion-popover trigger="open-filters">
              <ion-item lines="none">
                <ion-label>Élides</ion-label>
                <ion-checkbox :checked="elide" @ionChange="elide = $event.detail.checked; search()"/>
              </ion-item>
              <ion-item lines="none">
                <ion-label>Féminines</ion-label>
                <ion-checkbox :checked="feminine" @ionChange="feminine = $event.detail.checked; search()"/>
              </ion-item>
              <ion-item lines="none">
                <ion-select @ionChange="nature = $event.detail.value; search()" multiple label="Nature des rimes">
                  <ion-select-option :value="wordsNature.nom">Nom</ion-select-option>
                  <ion-select-option :value="wordsNature.verbe">Verbe</ion-select-option>
                  <ion-select-option :value="wordsNature.adverbe">Adverbe</ion-select-option>
                  <ion-select-option :value="wordsNature.adjectif">Adjectif</ion-select-option>
                  <ion-select-option :value="wordsNature.pronom">Pronom</ion-select-option>
                  <ion-select-option :value="wordsNature.aux">Auxiliaire</ion-select-option>
                  <ion-select-option :value="wordsNature.onomatopee">Onomatopée</ion-select-option>
                </ion-select>
              </ion-item>
              <ion-item lines="none" id="open-quality-selector">
                <ion-label>Qualité des rimes</ion-label>
              </ion-item>
              <ion-picker trigger="open-quality-selector" :columns="rimeQualityPickerColumns" :buttons="rimeQualityPickerButtons"></ion-picker>
            </ion-popover>
          </ion-item>
        </ion-toolbar>
      </ion-header>
      <ion-list class="ion-margin-top">
        <ion-item-group>
          <ion-item-divider>
            <ion-label slot="start">
              Rime
            </ion-label>
            <ion-label slot="end">
              Féminine / Élidable
            </ion-label>
          </ion-item-divider>
          <div class="ion-padding" v-if="!failed && rhymes.length === 0">
            <ion-note>Aucune rimes trouvées dans notre base avec ce mot. Utilisez la barre de recherche ci-dessus.</ion-note>
          </div>

          <div class="ion-padding" v-if="failed">
            <ion-note>La recherche dans le dictionnaire des rimes a échouée.</ion-note>
          </div>
          <ion-item @click="goTo(`/dictionnaire/${word[0]}`)" v-for="word in rhymes" :key="word.toString()" button v-else>
            <ion-label>
              {{ word[0].replaceAll('\\', '') }}
              <p>\{{ word[1] }}\</p>
            </ion-label>

            <ion-icon :icon="radioButtonOnOutline" v-if="word[2] == 1" color="primary"/>
            <ion-icon :icon="radioButtonOffOutline" v-else color="medium"/>

            <ion-icon slot="end" :icon="radioButtonOnOutline" v-if="word[3] == 1" color="primary"/>
            <ion-icon slot="end" :icon="radioButtonOffOutline" v-else color="medium"/>
          </ion-item>
        </ion-item-group>
      </ion-list>
      <ion-infinite-scroll v-if="rhymes.length > 0" @ionInfinite="loadMore">
        <ion-infinite-scroll-content></ion-infinite-scroll-content>
      </ion-infinite-scroll>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {getWordRimes} from "@/functions/dictionnary"
import {
  IonButton,
  IonButtons,
  IonCheckbox,
  IonChip,
  IonContent,
  IonHeader,
  IonIcon,
  IonItem,
  IonItemDivider,
  IonItemGroup,
  IonLabel,
  IonList,
  IonNote,
  IonPicker,
  IonPopover,
  IonProgressBar,
  IonSearchbar,
  IonTitle,
  IonToolbar,
  IonPage,
  useIonRouter,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  InfiniteScrollCustomEvent,
  IonSelect,
  IonSelectOption, IonBackButton
} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"
import {
  addOutline,
  closeOutline,
  filterCircleOutline,
  radioButtonOffOutline,
  radioButtonOnOutline,
  chevronBackOutline,
  chevronExpandOutline,
  chevronUpOutline
} from "ionicons/icons"
import {defineComponent} from "vue"
import {wordsNature} from "@/functions/database"

export default defineComponent({
  computed: {
    wordsNature() {
      return wordsNature
    }
  },
  data() {
    const syllabesPickerColumns = [
      {
        name: "minSyllabes",
        options: [
          {
            text: "Syllabes min.",
            value: 0
          },
          {
            text: "1",
            value: 1
          },
          {
            text: "2",
            value: 2
          },
          {
            text: "3",
            value: 3
          },
          {
            text: "4",
            value: 4
          },
        ],
      },
      {
        name: "maxSyllabes",
        options: [
          {
            text: "Syllabes max.",
            value: 0
          },
          {
            text: "1",
            value: 1
          },
          {
            text: "2",
            value: 2
          },
          {
            text: "3",
            value: 3
          },
          {
            text: "4",
            value: 4
          },
          {
            text: "5",
            value: 5
          },
        ],
      },
    ]

    const syllabesPickerButtons = [
      {
        text: "Annuler",
        role: "cancel",
      },
      {
        text: "Appliquer",
        handler: (value: any) => {
          this.setMinMax(value.minSyllabes.value, value.maxSyllabes.value)
          this.search()
        },
      },
    ]

    const rimeQualityPickerColumns = [
      {
        name: "quality",
        options: [
          {
            text: "Toutes",
            value: 0
          },
          {
            text: "Rimes pauvres",
            value: 1
          },
          {
            text: "Rimes suffisantes",
            value: 2
          },
          {
            text: "Rimes riches",
            value: 3
          }
        ],
      },
    ]

    const rimeQualityPickerButtons = [
      {
        text: "Annuler",
        role: "cancel",
      },
      {
        text: "Appliquer",
        handler: (value: any) => {
          this.setQuality(value.quality.value)
          this.search()
        },
      },
    ]

    return {
      loading: false,
      failed: false,
      rhymes: [] as any[],
      query: "",
      maxSyllabes: 0,
      minSyllabes: 0,
      elide: false,
      feminine: false,
      page: 0,
      syllabesPickerColumns,
      syllabesPickerButtons,
      rimeQualityPickerColumns,
      rimeQualityPickerButtons,
      quality: 0,
      nature: [] as string[]
    }
  },
  setup() {
    const ionRouter = useIonRouter()
    const goTo = (path: string) => {
      ionRouter.push(path, iosTransitionAnimation)
    }

    return {
      goTo,
      addOutline,
      closeOutline,
      filterCircleOutline,
      radioButtonOffOutline,
      radioButtonOnOutline,
      chevronBackOutline,
      chevronExpandOutline,
      chevronUpOutline,
      ionRouter
    }
  },
  mounted() {
    if (this.$route.params.mot) {
      this.query = this.$route.params.mot as string
      this.searchRhymes()
    }
  },
  methods: {
    async searchRhymes() {
      this.loading = true
      try {
        const {rhymes, success} = await getWordRimes(this.query, this.maxSyllabes == 0 ? undefined: this.maxSyllabes, this.minSyllabes == 0 ? undefined: this.minSyllabes, this.elide, this.feminine, this.quality, this.nature, this.page)
        for (const element of rhymes) {
          this.rhymes.push(element)
        }
        this.failed = !success
      } catch (e) {
        this.failed = true
      }
      this.loading = false
    },
    search() {
      this.rhymes = []
      this.page = 0
      this.searchRhymes()
    },
    setMinMax(min: number, max: number) {
      this.minSyllabes = min
      this.maxSyllabes = max
    },
    setQuality(quality: number) {
      this.quality = quality
    },
    loadMore(event: InfiniteScrollCustomEvent) {
      this.page += 1
      this.searchRhymes().then(() => {
        event.target.complete()
      })
    },
    scrollToTop() {
      this.$refs.content.$el.scrollToTop(500)
    },
  },
  components: {
    IonButton,
    IonButtons,
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonProgressBar,
    IonSearchbar,
    IonItem,
    IonIcon,
    IonChip,
    IonLabel,
    IonNote,
    IonCheckbox,
    IonPopover,
    IonList,
    IonItemGroup,
    IonItemDivider,
    IonPicker,
    IonPage,
    IonInfiniteScroll,
    IonInfiniteScrollContent,
    IonSelect,
    IonSelectOption,
    IonBackButton
  }
})
</script>
<style>
ion-chip.outline {
  --background: var(--ion-item-background);
  border: rgba(var(--ion-text-color-rgb, 0, 0, 0), 0.12) .55px solid;
}

.transparent {
  background: var(--ion-item-background)
}

.item-carousel {
  max-width: 100%;
  overflow-x: scroll;
}

.item-carousel ion-chip, .item-carousel div {
  min-width: max-content;
}

</style>
