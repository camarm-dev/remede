<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button :text="$t('back')" default-href="/rimes"></ion-back-button>
        </ion-buttons>
        <ion-title v-if="!failed && query != ''">{{ $t('rhymes') }} "{{ query }}"</ion-title>
        <ion-title v-else>{{ $t('rhymes') }}</ion-title>
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
            <ion-searchbar :value="query" disabled :placeholder="$t('rhymesPage.placeholder')"></ion-searchbar>
            <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
          </ion-toolbar>
          <ion-item class="item-carousel ion-text-wrap" lines="none">
            <ion-chip class="transparent">
              <ion-icon :icon="filterCircleOutline"></ion-icon>
              <ion-label>{{ $t('filters') }}</ion-label>
            </ion-chip>
            <ion-chip v-if="quality != 0">
              <ion-label v-if="quality == 1">{{ $t('rhymesPage.qualityPoor') }}</ion-label>
              <ion-label v-if="quality == 2">{{ $t('rhymesPage.qualitySufficient') }}</ion-label>
              <ion-label v-if="quality == 3">{{ $t('rhymesPage.qualityRich') }}</ion-label>
              <ion-icon :icon="closeOutline" @click="quality = 0; search()"/>
            </ion-chip>
            <ion-chip v-if="nature.length > 0">
              <ion-label><span :key="type" v-for="type in nature">{{ type.toLowerCase() }}. {{ nature.indexOf(type) + 1 < nature.length ? ',': '' }}</span></ion-label>
              <ion-icon :icon="closeOutline" @click="nature = []; search()"/>
            </ion-chip>
            <ion-chip v-if="elide">
              <ion-label>{{ $t('rhymesPage.withElide') }}</ion-label>
              <ion-icon :icon="closeOutline" @click="elide = false; search()"/>
            </ion-chip>
            <ion-chip v-if="feminine">
              <ion-label>{{ $t('rhymesPage.femininesOnly') }}</ion-label>
              <ion-icon :icon="closeOutline" @click="feminine = false; search()"/>
            </ion-chip>
            <div v-if="minSyllabes != 0 || maxSyllabes != 0">
              <ion-chip id="open-syllabes-selector">
                <ion-label>{{ $t('rhymesPage.fromSyllables') }} {{ minSyllabes }} {{ maxSyllabes > 0 ? ` ${$t('rhymesPage.toSyllables')} ${maxSyllabes}`: '' }} {{ $t('rhymesPage.syllables') }}</ion-label>
                <ion-icon :icon="closeOutline" @click="minSyllabes = 0; maxSyllabes = 0; search()"/>
              </ion-chip>
              <ion-picker trigger="open-syllabes-selector" :columns="syllabesPickerColumns" :buttons="syllabesPickerButtons"></ion-picker>
            </div>
            <div v-else>
              <ion-chip class="outline" id="open-syllabes-selector">
                <ion-label>{{ $t('rhymesPage.syllablesNumber') }}</ion-label>
                <ion-icon :icon="chevronExpandOutline"/>
              </ion-chip>
              <ion-picker trigger="open-syllabes-selector" :columns="syllabesPickerColumns" :buttons="syllabesPickerButtons"></ion-picker>
            </div>
            <ion-chip class="outline" id="open-filters">
              <ion-label>{{ $t('rhymesPage.addFilter') }}</ion-label>
              <ion-icon :icon="addOutline"/>
            </ion-chip>
            <ion-popover trigger="open-filters">
              <ion-item lines="none">
                <ion-label>{{ $t('rhymesPage.elides') }}</ion-label>
                <ion-checkbox :checked="elide" @ionChange="elide = $event.detail.checked; search()"/>
              </ion-item>
              <ion-item lines="none">
                <ion-label>{{ $t('rhymesPage.feminines') }}</ion-label>
                <ion-checkbox :checked="feminine" @ionChange="feminine = $event.detail.checked; search()"/>
              </ion-item>
              <ion-item lines="none">
                <ion-select @ionChange="nature = $event.detail.value; search()" multiple :label="$t('rhymesPage.rhymeNature')">
                  <ion-select-option :value="wordsNature.nom">{{ $t('nature.name') }}</ion-select-option>
                  <ion-select-option :value="wordsNature.verbe">{{ $t('nature.verb') }}</ion-select-option>
                  <ion-select-option :value="wordsNature.adverbe">{{ $t('nature.adverb') }}</ion-select-option>
                  <ion-select-option :value="wordsNature.adjectif">{{ $t('nature.adjective') }}</ion-select-option>
                  <ion-select-option :value="wordsNature.pronom">{{ $t('nature.pronoun') }}</ion-select-option>
                  <ion-select-option :value="wordsNature.aux">{{ $t('nature.auxiliary') }}</ion-select-option>
                  <ion-select-option :value="wordsNature.onomatopee">{{ $t('nature.onomatopoeia') }}</ion-select-option>
                </ion-select>
              </ion-item>
              <ion-item lines="none" id="open-quality-selector">
                <ion-label>{{ $t('rhymesPage.quality') }}</ion-label>
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
              {{ $t('rhymesPage.rhyme') }}
            </ion-label>
            <ion-label slot="end">
              {{ $t('rhymesPage.femininesElidableLabel') }}
            </ion-label>
          </ion-item-divider>
          <div class="ion-padding" v-if="!failed && rhymes.length === 0">
            <ion-note>{{ $t('rhymesPage.noRhymeFound') }}</ion-note>
          </div>

          <div class="ion-padding" v-if="failed">
            <ion-note>{{ $t('rhymesPage.searchErrored') }}</ion-note>
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
            text: this.$t("rhymesPage.syllablesMinimumAbbr"),
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
            text: this.$t("rhymesPage.syllablesMaximumAbbr"),
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
        text: this.$t("cancel"),
        role: "cancel",
      },
      {
        text: this.$t("apply"),
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
            text: this.$t("feminineAll"),
            value: 0
          },
          {
            text: this.$t("rhymesPage.qualityPoor"),
            value: 1
          },
          {
            text: this.$t("rhymesPage.qualitySufficient"),
            value: 2
          },
          {
            text: this.$t("rhymesPage.qualityRich"),
            value: 3
          }
        ],
      },
    ]

    const rimeQualityPickerButtons = [
      {
        text: this.$t("cancel"),
        role: "cancel",
      },
      {
        text: this.$t("apply"),
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
      ((this.$refs.content as any).$el as HTMLIonContentElement).scrollToTop(500)
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
