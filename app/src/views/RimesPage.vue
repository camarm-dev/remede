<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar ref="mainToolbar">
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title v-if="!failed && query != ''">Rimes "{{ query }}"</ion-title>
        <ion-title v-else>Rimes</ion-title>
      </ion-toolbar>
      <ion-toolbar ref="searchToolbar">
        <ion-searchbar @focusin="onFocus()" @focusout="onLeave()" :value="query" @ionInput="handleSearchBarInput($event.detail.value as string)" placeholder="Entrez un mot"></ion-searchbar>
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
          <ion-title size="large">Rimes</ion-title>
        </ion-toolbar>
      </ion-header>
      <div class="ion-padding">
        <ion-note>Recherchez des rimes ci-dessus !</ion-note>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {getRimesAutocomplete} from "@/functions/dictionnary"
import {
  type Animation, AnimationDirection, createAnimation,
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
  useIonRouter
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
    }
  },
  setup() {
    const mainToolbar = ref(null) as any as Ref
    const searchToolbar = ref(null) as any as Ref
    const content = ref(null) as any as Ref

    let mainToolbarAnimation: Animation
    let searchToolbarAnimation: Animation
    let contentAnimation: Animation

    onMounted(() => {
      mainToolbarAnimation = createAnimation()
          .addElement(mainToolbar.value?.$el)
          .duration(250)
          .fromTo("transform", "translateY(0)", "translateY(-100%)")
          .fromTo("opacity", "1", "0")
      searchToolbarAnimation = createAnimation()
          .addElement(searchToolbar.value?.$el)
          .duration(250)
          .fromTo("transform", "translateY(0)", "translateY(-50%)")
          .fromTo("scale", "1", "1.01")
      contentAnimation = createAnimation()
          .addElement(content.value?.$el)
          .duration(250)
          .fromTo("transform", "translateY(0)", "translateY(-10%)")

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
    async startAutocompleteSearch(query: string) {
      window.clearTimeout(this.autocompleteTimeout)
      this.autocompleteTimeout = window.setTimeout(async () => {
        this.loading = true
        try {
          this.results = await getRimesAutocomplete(query)
        } catch (e) {
          const message = await toastController.create({
            header: "Erreur",
            message: `La recherche dans le dictionnaire des rimes a échouée: ${e}`,
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
