<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar ref="mainToolbar">
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar ref="searchToolbar">
        <ion-searchbar @focusin="onFocus()" @focusout="onLeave()" :value="query"
                       @ionInput="handleSearchbarInput($event.detail.value as string)"
                       placeholder="Rechercher un mot"></ion-searchbar>
        <ion-progress-bar v-if="loading" type="indeterminate" color="medium"
                          style="width: 95%; margin: auto"></ion-progress-bar>
      </ion-toolbar>
      <ion-toolbar :class="`results-wrapper ${results.length > 0 ? '': 'empty'}`" ref="content">
        <ion-list class="search-results">
          <ion-item :key="result" v-for="result in results" @click="goTo(`/dictionnaire/${result}`)" class="ion-no-padding" button>
            <ion-label>
              {{ result }}
            </ion-label>
          </ion-item>
          <ion-item v-if="!loading && query != ''" @click="goTo(`/search/${query}`)" :detail-icon="arrowForward" class="ion-no-padding" button>
            <ion-label>
              Tout voir
            </ion-label>
          </ion-item>
        </ion-list>
      </ion-toolbar>
      <ion-toolbar v-if="results.length == 0 && query !== '' && !loading">
        <ion-list inset>
          <ion-item color="light" class="border-radius" lines="none" button @click="report()">
            <ion-label>
              <p>Demander à ajouter un mot</p>
              <h2>Reporter "{{ query }}"</h2>
            </ion-label>
          </ion-item>
        </ion-list>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Dictionnaire</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset>
        <ion-item @click="goTo(`/dictionnaire/${todayWord}`)" :disabled="todayWordDisabled" color="light" button>
          <ion-icon slot="start" :icon="calendarOutline"/>
          <ion-label>
            <h2>Mot du jour</h2>
          </ion-label>
        </ion-item>
        <ion-item @click="goTo(`/dictionnaire/${randomWord}`)" :disabled="randomWordDisabled" color="light" button>
          <ion-icon :icon="shuffle" slot="start"/>
          <ion-label>
            <h2>Mot au hasard</h2>
          </ion-label>
        </ion-item>
      </ion-list>

      <ion-list inset>
        <ion-item @click="goTo('/marques-page')" button color="primary">
          <ion-icon slot="start" :icon="bookmark"/>
          <ion-label>
            Mes marques page
          </ion-label>
        </ion-item>
      </ion-list>

      <div class="list-title">
        Pour vous
      </div>
      <ion-list inset>
        <swiper :modules="[Pagination]" :pagination="{ enabled: true, clickable: true }">
          <swiper-slide v-if="hasDictionaryUpdate" @click="goTo('/parametres')">
            <img :src="newBaseIllustration" alt="Mettez à jour votre dictionnaire !"/>
          </swiper-slide>
          <swiper-slide v-if="hasAppUpdate" @click="open('https://remede.camarm.fr/download')">
            <img :src="newVersionIllustration" alt="Mettez à jour votre app !"/>
          </swiper-slide>
          <swiper-slide id="open-changelog">
            <img :src="changelogIllustration" alt="Illustration changelog"/>
          </swiper-slide>
        </swiper>
      </ion-list>
      <ion-modal trigger="open-changelog" :initial-breakpoint="0.5" :breakpoints="[0, 0.5, 0.75]">
        <ion-content class="ion-padding">
          <h1 class="remede-font">Notes de changement</h1>
          <p>
            La version sur laquelle vous naviguez est la version <code>1.2.0-beta</code>, nom de code <i>Brown Sheep, beta</i>.<br><br>
            Elle apporte les nouveautés et patch suivants:
            <ul>
              <li>Dictionnaire de rimes.</li>
              <li>Nouvelle base de données, et suppression des anciennes versions.</li>
              <li>Création d'un site web à <a href="https://remede.camarm.fr" target="_blank">remede.camarm.fr</a>.</li>
            </ul>
          </p>
        </ion-content>
      </ion-modal>

    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import WordModal from "@/components/WordModal.vue"
import {bookmark, calendarOutline, shuffle, arrowForward} from "ionicons/icons"
import {getAutocomplete, getRandomWord, getTodayWord} from "@/functions/dictionnary"
import {useRouter} from "vue-router"
import {
  createAnimation,
  IonButtons,
  IonContent,
  IonHeader,
  IonMenuButton,
  IonPage,
  IonTitle,
  IonToolbar,
  IonSearchbar,
  IonIcon,
  IonLabel,
  IonItem,
  IonList,
  IonProgressBar,
  loadingController,
  toastController,
  AnimationDirection,
  useIonRouter,
  useBackButton,
  modalController,
  IonModal,
} from "@ionic/vue"
import {defineComponent, onMounted, Ref, ref} from "vue"
import type {Animation} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"
import LandingScreen from "@/components/LandingScreen.vue"
import {Swiper, SwiperSlide} from "swiper/vue"
import {Navigation, Pagination} from "swiper/modules"
import changelogIllustration from  "@/assets/changelog.png"
import newBaseIllustration from  "@/assets/newBase.png"
import newVersionIllustration from  "@/assets/newVersion.png"
import "swiper/css"
import "swiper/css/navigation"
import "swiper/css/pagination"
import "@ionic/vue/css/ionic-swiper.css"
import {getOfflineDictionaryStatus} from "@/functions/offline"
import {InformationsResponse} from "@/functions/types/api_responses"
import {App} from "@capacitor/app"

export default defineComponent({
  components: {
    IonModal,
    IonButtons,
    IonContent,
    IonHeader,
    IonMenuButton,
    IonPage,
    IonTitle,
    IonToolbar,
    IonSearchbar,
    IonIcon,
    IonLabel,
    IonItem,
    IonList,
    IonProgressBar,
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      results: [] as string[],
      query: "",
      router: useRouter(),
      // Ignoring linter error about empty function (@typescript-eslint/no-empty-function)
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      autocompleteTimeout: window.setTimeout(() => {
      }, 500),
      randomWord: "",
      loading: false,
      randomWordDisabled: true,
      todayWord: "",
      todayWordDisabled: true,
      el: null as any,
      hasDictionaryUpdate: false,
      hasAppUpdate: false,
    }
  },
  mounted() {
    this.loadRandomWord()
    this.loadTodayWord()
    this.el = ref(this.$el)
    this.openLandingScreen()
    this.reloadUpdateStatuses()
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

    useBackButton(110, () => {
      if (ionRouter.canGoBack()) {
        ionRouter.back(iosTransitionAnimation)
        return
      }
      ionRouter.navigate("/dictionnaire", "back", "replace", iosTransitionAnimation)
    })

    const goTo = (path: string) => {
      ionRouter.push(path, iosTransitionAnimation)
    }

    return {
      bookmark,
      calendarOutline,
      shuffle,
      WordModal,
      onFocus,
      onLeave,
      mainToolbar,
      searchToolbar,
      content,
      ionRouter,
      goTo,
      Navigation,
      Pagination,
      arrowForward,
      changelogIllustration,
      newBaseIllustration,
      newVersionIllustration
    }
  },
  methods: {
    async handleSearchbarInput(input: string) {
      this.query = input
      if (input != "") {
        this.startAutocompleteSearch(input)
      } else {
        window.clearTimeout(this.autocompleteTimeout)
        this.results = []
      }
    },
    startAutocompleteSearch(input: string) {
      window.clearTimeout(this.autocompleteTimeout)
      this.autocompleteTimeout = window.setTimeout(async () => {
        this.loading = true
        try {
          this.results = await getAutocomplete(input)
        } catch (e) {
          const message = await toastController.create({
            header: "Erreur",
            message: `La recherche dans le dictionnaire a échouée: ${e}`,
            duration: 5000,
            color: "danger"
          })

          await message.present()
        }
        this.loading = false
      }, 500)
    },
    async loadRandomWord() {
      this.randomWord = await getRandomWord()
      this.randomWordDisabled = false
    },
    async loadTodayWord() {
      this.todayWord = await getTodayWord()
      this.todayWordDisabled = false
    },
    open(url: string) {
      window.open(url)
    },
    async reloadUpdateStatuses() {
      const status = await getOfflineDictionaryStatus()
      const downloaded = status.downloaded
      const specs = await fetch("https://api-remede.camarm.fr").then(resp => resp.json()) as InformationsResponse
      if (downloaded) {
        this.hasDictionaryUpdate = status.hash != specs.dictionnaires[status.slug].hash
      }

      const tag = await fetch("https://api.github.com/repos/camarm-dev/remede/tags").then(resp => resp.json()).then((resp: any) => resp[0].name)
      const version = (await App.getInfo()).version
      if (!version.startsWith(tag)) {
        this.hasAppUpdate = true
      }
    },
    async report() {
      const loader = await loadingController.create({
        message: "Chargement"
      })
      await loader.present()
      await fetch(`https://api-remede.camarm.fr/ask-new-word/${this.query}`)
      const toast = await toastController.create({
        header: "Mot reporté",
        message: `Vous avez bien demander à ajouter le mot "${this.query}"`,
        duration: 3000
      })
      this.query = ""
      await loader.dismiss()
      await toast.present()
    },
    async openLandingScreen() {
      const hasOpenedLandingScreen = localStorage.getItem("landingScreen") || "false"
      if (hasOpenedLandingScreen === "false") {
        const modal = await modalController.create({
          component: LandingScreen,
          presentingElement: this.el,
          handle: true
        })
        await modal.present()
        window.addEventListener("landingScreenClosed", () => {
          modal.dismiss()
        })
        localStorage.setItem("landingScreen", "true")
      }
    }
  }
})
</script>
<style>
.results-wrapper {
  transition: .5s ease-in-out;
  height: 270px;
}

.results-wrapper.empty {
  height: 0;
}

.search-results {
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  padding-inline-start: 10px;
  padding-inline-end: 10px;
}

.search-results ion-item {
  --border-width: 0;
  padding-bottom: .55px !important;
  background: linear-gradient(to right, var(--ion-item-border-color, var(--ion-border-color, var(--ion-color-step-250, #c8c7cc))) 70%, rgba(64, 64, 64, 0));
}

.search-results ion-item .item-bottom {
  --border-color: transparent;
}

.search-results ion-item::part(native) {
  --border-width: 0;
  --inner-border-width: 0;
  position: relative;
}
</style>
