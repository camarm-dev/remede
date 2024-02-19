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
                       @ionInput="handleSearchbarInput($event.detail.value)"
                       placeholder="Rechercher un mot"></ion-searchbar>
        <ion-progress-bar v-if="loading" type="indeterminate" color="medium"
                          style="width: 95%; margin: auto"></ion-progress-bar>
      </ion-toolbar>
      <ion-toolbar :class="`results-wrapper ${results.length > 0 ? '': 'empty'}`" ref="content">
        <ion-list class="search-results">
          <ion-nav-link :key="result" v-for="result in results" router-direction="forward" :component="WordModal"
                        :component-props="{ motRemede: result }">
            <ion-item class="ion-no-padding" button>
              <ion-label>
                {{ result }}
              </ion-label>
            </ion-item>
          </ion-nav-link>
        </ion-list>
      </ion-toolbar>
      <ion-toolbar v-if="results.length == 0 && query !== '' && !loading">
        <ion-item color="light" class="border-radius" lines="none" button @click="report()">
          <ion-label>
            <p>Demander à ajouter un mot</p>
            <h2>Reporter "{{ query }}"</h2>
          </ion-label>
        </ion-item>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Dictionnaire</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-list inset>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: todayWord }">
          <ion-item :disabled="todayWordDisabled" color="light" button>
            <ion-icon slot="start" :icon="calendarOutline"/>
            <ion-label>
              <h2>Mot du jour</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
        <ion-nav-link router-direction="forward" :component="WordModal" :component-props="{ motRemede: randomWord }">
          <ion-item :disabled="randomWordDisabled" color="light" button>
            <ion-icon :icon="shuffle" slot="start"/>
            <ion-label>
              <h2>Mot au hasard</h2>
            </ion-label>
          </ion-item>
        </ion-nav-link>
      </ion-list>

      <ion-list inset>
        <ion-item @click="goTo('/marques-page')" button color="primary">
          <ion-icon slot="start" :icon="bookmark"/>
          <ion-label>
            Mes marques page
          </ion-label>
        </ion-item>
      </ion-list>

    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import WordModal from "@/components/WordModal.vue";
import {bookmark, calendarOutline, shuffle} from "ionicons/icons";
import {getAutocomplete, getRandomWord, getTodayWord} from "@/functions/dictionnary";
import {useRouter} from "vue-router";
import {
  createAnimation,
  IonButtons,
  IonContent,
  IonHeader,
  IonMenuButton,
  IonPage,
  IonTitle,
  IonToolbar,
  IonNavLink,
  IonSearchbar,
  IonIcon,
  IonLabel,
  IonItem,
  IonList,
  IonProgressBar,
  loadingController,
  toastController, AnimationDirection
} from "@ionic/vue";
import {defineComponent, onMounted, ref} from "vue";
import type {Animation} from "@ionic/vue";


export default defineComponent({
  components: {
    IonButtons,
    IonContent,
    IonHeader,
    IonMenuButton,
    IonPage,
    IonTitle,
    IonToolbar,
    IonNavLink,
    IonSearchbar,
    IonIcon,
    IonLabel,
    IonItem,
    IonList,
    IonProgressBar,
  },
  data() {
    return {
      results: [] as string[],
      query: '',
      router: useRouter(),
      // Ignoring linter error about empty function (@typescript-eslint/no-empty-function)
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      autocompleteTimeout: window.setTimeout(() => {
      }, 500),
      randomWord: '',
      loading: false,
      randomWordDisabled: true,
      todayWord: '',
      todayWordDisabled: true
    }
  },
  mounted() {
    this.loadRandomWord()
    this.loadTodayWord()
  },
  setup() {
    const mainToolbar = ref(null)
    const searchToolbar = ref(null)
    const content = ref(null)

    let mainToolbarAnimation: Animation
    let searchToolbarAnimation: Animation
    let contentAnimation: Animation

    onMounted(() => {
      mainToolbarAnimation = createAnimation()
          .addElement(mainToolbar.value.$el)
          .duration(250)
          .fromTo('transform', 'translateY(0)', 'translateY(-100%)')
          .fromTo('opacity', '1', '0');
      searchToolbarAnimation = createAnimation()
          .addElement(searchToolbar.value.$el)
          .duration(250)
          .fromTo('transform', 'translateY(0)', 'translateY(-50%)')
          .fromTo('scale', '1', '1.01')
      contentAnimation = createAnimation()
          .addElement(content.value.$el)
          .duration(250)
          .fromTo('transform', 'translateY(0)', 'translateY(-10%)')

    })

    const animateMain = (direction: AnimationDirection = 'normal') => mainToolbarAnimation.direction(direction).play()
    const animateSearch = (direction: AnimationDirection = 'normal') => searchToolbarAnimation.direction(direction).play()
    const animateContent = (direction: AnimationDirection = 'normal') => contentAnimation.direction(direction).play()

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

    return {
      bookmark,
      calendarOutline,
      shuffle,
      WordModal,
      onFocus,
      onLeave,
      mainToolbar,
      searchToolbar,
      content
    }
  },
  methods: {
    async handleSearchbarInput(input: string) {
      this.query = input
      if (input != '') {
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
            header: 'Erreur',
            message: `La recherche dans le dictionnaire à échouée: ${e}`,
            duration: 5000,
            color: 'danger'
          })

          await message.present()
        }
        this.loading = false
      }, 500)
    },
    goTo(path: string) {
      this.router.push(path)
    },
    async loadRandomWord() {
      this.randomWord = await getRandomWord()
      this.randomWordDisabled = false
    },
    async loadTodayWord() {
      this.todayWord = await getTodayWord()
      this.todayWordDisabled = false
    },
    async report() {
      const loader = await loadingController.create({
        message: 'Chargement'
      })
      await loader.present()
      await fetch(`https://api-remede.camarm.fr/ask-new-word/${this.query}`)
      const toast = await toastController.create({
        header: 'Mot reporté',
        message: `Vous avez bien demander à ajouter le mot "${this.query}"`,
        duration: 3000
      })
      this.query = ''
      await loader.dismiss()
      await toast.present()
    },
  }
})
</script>
<style scoped>
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
