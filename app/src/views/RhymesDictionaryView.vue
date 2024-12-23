<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar ref="mainToolbar">
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title v-if="!failed && query != ''">{{ $t('rhymes') }} "{{ query }}"</ion-title>
        <ion-title v-else>{{ $t('rhymes') }}</ion-title>
      </ion-toolbar>
      <ion-toolbar ref="searchToolbar">
        <ion-searchbar @keydown.enter="goTo(`/rimes/${query}`)" @focusin="onFocus()" @focusout="onLeave()" :value="query" @ionInput="handleSearchBarInput($event.detail.value as string)" :placeholder="$t('rhymesPage.placeholder')"></ion-searchbar>
        <ion-select v-if="availableDictionaries.length > 1" :selected-text="getSmallDictionaryName(selectedDictionary.name)" @ionChange="changeDictionary($event.target.value)" class="dictionarySelector" color="primary" interface="action-sheet" :toggle-icon="chevronDownOutline" slot="end">
          <ion-select-option :key="dictionary.slug" v-for="dictionary in availableDictionaries" :value="dictionary">{{ dictionary.name }}</ion-select-option>
        </ion-select>
        <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
      </ion-toolbar>
      <ion-toolbar :class="`results-wrapper ${results.length > 0 ? '': 'empty'}`" ref="content">
        <ion-list class="search-results">
          <ion-item v-if="!results.includes(query)" @click="goTo(`/rimes/${query}`)" class="ion-no-padding" button>
            <ion-label>
              {{ query }}
            </ion-label>
          </ion-item>
          <ion-item :key="result" v-for="result in results" @click="goTo(`/rimes/${result}`)" class="ion-no-padding" button>
            <ion-label>
              {{ result }}
            </ion-label>
          </ion-item>
        </ion-list>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">{{ $t('rhymes') }}</ion-title>
        </ion-toolbar>
      </ion-header>
      <div class="ion-padding">
        <ion-note>{{ $t('rhymesPage.searchRhymesAbove') }}</ion-note>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {
  getAvailableDictionaries,
  getFavoriteDictionary,
  getRimesAutocomplete,
  setDictionary
} from "@/functions/dictionnary"
import {
  type Animation, AnimationDirection,
  IonButtons,
  IonContent,
  IonHeader,
  IonItem,
  IonLabel,
  IonMenuButton,
  IonNote,
  IonPage,
  IonProgressBar,
  IonSearchbar,
  IonTitle,
  IonToolbar,
  toastController,
  IonList,
  useIonRouter, IonSelectOption, IonSelect
} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"
import {
  addOutline,
  closeOutline,
  filterCircleOutline,
  radioButtonOffOutline,
  radioButtonOnOutline
} from "ionicons/icons"
import {defineComponent, onMounted, Ref, ref} from "vue"
import {
  defaultRemedeContentAnimation,
  defaultRemedeMainToolbarAnimation,
  defaultRemedeSearchToolbarAnimation
} from "@/functions/animations"
import {RemedeDictionaryOption} from "@/functions/types/apiResponses"

export default defineComponent({
  data() {
    return {
      loading: false,
      failed: false,
      results: [] as string[],
      query: "",
      // Ignoring linter error about empty function (@typescript-eslint/no-empty-function)
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      autocompleteTimeout: window.setTimeout(() => {}, 500),
      availableDictionaries: [] as RemedeDictionaryOption[],
      selectedDictionary: {} as RemedeDictionaryOption
    }
  },
  mounted() {
    this.loadDictionaries()
  },
  setup() {
    const mainToolbar = ref(null) as any as Ref
    const searchToolbar = ref(null) as any as Ref
    const content = ref(null) as any as Ref

    let mainToolbarAnimation: Animation
    let searchToolbarAnimation: Animation
    let contentAnimation: Animation

    onMounted(() => {
      mainToolbarAnimation = defaultRemedeMainToolbarAnimation(mainToolbar.value?.$el)
      searchToolbarAnimation = defaultRemedeSearchToolbarAnimation(searchToolbar.value?.$el)
      contentAnimation = defaultRemedeContentAnimation(content.value?.$el)
    })

    const animateMain = (direction: AnimationDirection = "normal") => mainToolbarAnimation.direction(direction).play()
    const animateSearch = (direction: AnimationDirection = "normal") => searchToolbarAnimation.direction(direction).play()
    const animateContent = (direction: AnimationDirection = "normal") => contentAnimation.direction(direction).play()

    const onFocus = () => {
      animateMain()
      animateSearch()
      animateContent()
    }

    const onLeave = () => {
      animateMain("reverse")
      animateSearch("reverse")
      animateContent("reverse")
    }

    const ionRouter = useIonRouter()
    const goTo = (path: string) => {
      ionRouter.push(path, iosTransitionAnimation)
    }
    return {
      goTo,
      onFocus,
      onLeave,
      addOutline,
      closeOutline,
      filterCircleOutline,
      radioButtonOffOutline,
      radioButtonOnOutline
    }
  },
  methods: {
    async loadDictionaries() {
      this.availableDictionaries = (await getAvailableDictionaries()).filter(dictionary => !dictionary.slug.includes("legacy"))
      this.selectedDictionary = await getFavoriteDictionary(this.availableDictionaries)
    },
    getSmallDictionaryName(name: string) {
      return name.replaceAll("Remède", "").replaceAll("(", "").replaceAll(")", "")
    },
    changeDictionary(dictionary: RemedeDictionaryOption) {
      this.selectedDictionary = dictionary
      setDictionary(dictionary)
    },
    async startAutocompleteSearch(query: string) {
      window.clearTimeout(this.autocompleteTimeout)
      this.autocompleteTimeout = window.setTimeout(async () => {
        this.loading = true
        try {
          this.results = await getRimesAutocomplete(query)
        } catch (e) {
          const message = await toastController.create({
            header: this.$t("error"),
            message: this.$t("errors.rhymesSearchFailed", { error: e }),
            duration: 5000,
            color: "danger"
          })

          await message.present()
        }
        this.loading = false
      }, 500)
    },
    handleSearchBarInput(input: string) {
      this.query = input
      if (input != "") {
        this.startAutocompleteSearch(input)
      } else {
        window.clearTimeout(this.autocompleteTimeout)
        this.results = []
      }
    },
  },
  components: {
    IonSelect, IonSelectOption,
    IonButtons,
    IonContent,
    IonHeader,
    IonMenuButton,
    IonPage,
    IonTitle,
    IonToolbar,
    IonProgressBar,
    IonSearchbar,
    IonItem,
    IonLabel,
    IonNote,
    IonList
  }
})
</script>
