<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-nav-link router-direction="back">
            <ion-button @click="navigateBack()">
              <ion-icon class="ion-no-margin" :icon="chevronBackOutline" slot="start"/>
              Retour
            </ion-button>
          </ion-nav-link>
        </ion-buttons>
        <ion-title v-if="!failed && query != ''">Rimes "{{ query }}"</ion-title>
        <ion-title v-else>Rimes</ion-title>
      </ion-toolbar>
      <ion-toolbar>
        <ion-searchbar :value="query" disabled placeholder="Entrez un mot"></ion-searchbar>
        <ion-progress-bar v-if="loading" type="indeterminate" color="medium" style="width: 95%; margin: auto"></ion-progress-bar>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-item class="item-carousel ion-text-wrap" lines="none">
            <ion-chip class="transparent">
              <ion-icon :icon="filterCircleOutline"></ion-icon>
              <ion-label>Filtres</ion-label>
            </ion-chip>
            <ion-chip v-if="minSyllabes != 0 || maxSyllabes != 0"  id="open-syllabes-selector">
              <ion-label>de {{ minSyllabes }} {{ maxSyllabes > 0 ? ` à ${maxSyllabes}`: '' }} syllabe(s)</ion-label>
              <ion-icon :icon="closeOutline" @click="minSyllabes = 0; maxSyllabes = 0; search()"/>
            </ion-chip>
            <ion-chip class="outline" id="open-syllabes-selector" v-else>
              <ion-label>Nb. syllabes</ion-label>
              <ion-icon :icon="chevronExpandOutline"/>
            </ion-chip>
            <ion-picker trigger="open-syllabes-selector" :columns="syllabesPickerColumns" :buttons="syllabesPickerButtons"></ion-picker>
            <ion-chip v-if="elide">
              <ion-label>Avec élide</ion-label>
              <ion-icon :icon="closeOutline" @click="elide = false; search()"/>
            </ion-chip>
            <ion-chip v-if="feminine">
              <ion-label>Féminines seulement</ion-label>
              <ion-icon :icon="closeOutline" @click="feminine = false; search()"/>
            </ion-chip>
            <ion-chip class="outline" id="open-filters">
              <ion-label>Ajouter un filtre</ion-label>
              <ion-icon :icon="addOutline"/>
            </ion-chip>
            <ion-popover trigger="open-filters">
              <ion-item lines="none">
                <ion-label>Élides</ion-label>
                <ion-checkbox :checked="elide" @ionChange="elide = $event.detail.checked"/>
              </ion-item>
              <ion-item lines="none">
                <ion-label>Féminines</ion-label>
                <ion-checkbox :checked="feminine" @ionChange="feminine = $event.detail.checked"/>
              </ion-item>
            </ion-popover>
          </ion-item>
        </ion-toolbar>
      </ion-header>
      <ion-list class="ion-margin-top ion-margin-bottom">
        <ion-item-group>
          <ion-item-divider>
            <ion-label slot="start">
              Mot
            </ion-label>
            <ion-label slot="end">
              Féminine
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
              {{ word[0] }}
              <p>\{{ word[1] }}\</p>
            </ion-label>

            <ion-icon slot="end" :icon="radioButtonOnOutline" v-if="word[3] == 1" color="success"/>
            <ion-icon slot="end" :icon="radioButtonOffOutline" v-else color="danger"/>
          </ion-item>
        </ion-item-group>
      </ion-list>
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
  IonInput,
  IonItem,
  IonItemDivider,
  IonItemGroup,
  IonLabel,
  IonList,
  IonNavLink,
  IonNote,
  IonPicker,
  IonPopover,
  IonProgressBar,
  IonSearchbar,
  IonTitle,
  IonToolbar,
  IonPage,
  useIonRouter
} from "@ionic/vue"
import {iosTransitionAnimation} from "@ionic/core"
import {
  addOutline,
  closeOutline,
  filterCircleOutline,
  radioButtonOffOutline,
  radioButtonOnOutline,
  chevronBackOutline,
  settingsOutline, chevronExpandOutline
} from "ionicons/icons"
import {defineComponent} from "vue"

export default defineComponent({
  data() {
    const syllabesPickerColumns = [
      {
        name: 'minSyllabes',
        options: [
          {
            text: 'Syllabes min.',
            value: 0
          },
          {
            text: '1',
            value: 1
          },
          {
            text: '2',
            value: 2
          },
          {
            text: '3',
            value: 3
          },
          {
            text: '4',
            value: 4
          },
        ],
      },
      {
        name: 'maxSyllabes',
        options: [
          {
            text: 'Syllabes max.',
            value: 0
          },
          {
            text: '1',
            value: 1
          },
          {
            text: '2',
            value: 2
          },
          {
            text: '3',
            value: 3
          },
          {
            text: '4',
            value: 4
          },
          {
            text: '5',
            value: 5
          },
        ],
      },
    ]

    const syllabesPickerButtons = [
      {
        text: 'Annuler',
        role: 'cancel',
      },
      {
        text: 'Appliquer',
        handler: (value: any) => {
          this.setMinMax(value.minSyllabes.value, value.maxSyllabes.value)
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
      syllabesPickerButtons
    }
  },
  setup() {
    const ionRouter = useIonRouter()
    const goTo = (path: string) => {
      ionRouter.push(path, iosTransitionAnimation)
    }

    function navigateBackIfNoHistory() {
      if (!ionRouter.canGoBack()) {
        ionRouter.navigate("/rimes", "back", "replace")
        return true
      }
      return false
    }

    const navigateBack = navigateBackIfNoHistory

    const filtersButtons = ['Appliquer'];
    const filtersInputs = [
      {
        label: 'Rimes féminines seulement',
        type: 'radio',
        value: 'feminine',
      },
      {
        label: 'Rimes élidables',
        type: 'radio',
        value: 'elide',
      },
      {
        label: 'Green',
        type: 'radio',
        value: 'green',
      },
    ];

    return {
      goTo,
      addOutline,
      closeOutline,
      filterCircleOutline,
      radioButtonOffOutline,
      radioButtonOnOutline,
      chevronBackOutline,
      chevronExpandOutline,
      ionRouter,
      navigateBack
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
        const {rhymes, success} = await getWordRimes(this.query, this.maxSyllabes == 0 ? undefined: this.maxSyllabes, this.minSyllabes == 0 ? undefined: this.minSyllabes, this.elide)
        for (const element of rhymes) {
          this.rhymes.push(element)
        }
        this.failed = !success
      } catch (e) {
        console.error(e)
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
    }
  },
  components: {
    IonButton,
    IonNavLink,
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
    IonInput,
    IonList,
    IonItemGroup,
    IonItemDivider,
    IonPicker,
    IonPage
  }
})
</script>
<style>
ion-chip.outline {
  --background: #fff;
  border: rgba(var(--ion-text-color-rgb, 0, 0, 0), 0.12) .55px solid;
}

.transparent {
  background: #fff
}

.item-carousel {
  max-width: 100%;
  overflow-x: scroll;
}

.item-carousel ion-chip, .item-carousel div {
  min-width: max-content;
}

</style>
