<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonTitle,
  IonToolbar,
  IonButton,
  IonNavLink,
  IonLabel, IonBadge,
} from "@ionic/vue";
import {
  chevronBackOutline,
  cloudDownloadOutline,
  informationCircleOutline,
  shareOutline
} from "ionicons/icons";
</script>

<template>
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
      <ion-title>{{ nom }}</ion-title>
      <ion-buttons slot="end">
        <ion-button @click="shareSheet()">
          <ion-icon slot="icon-only" :icon="shareOutline"></ion-icon>
        </ion-button>
        <ion-button :download="`${slug}.md`" :href="`https://api-remede.camarm.fr/sheets/download/${slug}`">
          <ion-icon slot="icon-only" :icon="cloudDownloadOutline"></ion-icon>
        </ion-button>
      </ion-buttons>
    </ion-toolbar>
  </ion-header>
  <ion-content :fullscreen="true" class="ion-padding">
    <ion-header collapse="condense">
      <ion-toolbar>
        <ion-label>
          <ion-title class="remede-font ion-wrap" size="large">{{ nom }}</ion-title>
        </ion-label>
        <ion-buttons slot="end">
          <ion-button @click="openCredits()">
            <ion-icon slot="icon-only" :icon="informationCircleOutline" color="medium"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-label>
      <p class="ion-padding-start">{{ description }}</p>
    </ion-label>
    <div class="ion-padding">
      <ion-badge class="ion-margin-end" :color="getTagColor(tag)" :key="tag" v-for="tag in tags">{{ tag }}</ion-badge>
    </div>
    <br>
    <div class="ion-padding" v-html="contenu"/>
  </ion-content>
</template>

<script lang="ts">
import {useIonRouter} from "@ionic/vue";
import {defineComponent} from "vue";
import {Share} from "@capacitor/share";
import {navigateBackFunction} from "@/functions/types/utils";

export default defineComponent({
  props: ['nom', 'description', 'contenu', 'tags', 'credits', 'slug'],
  data() {
    return {
      navigateBack: () => "" as navigateBackFunction
    }
  },
  mounted() {
    const ionRouter = useIonRouter()
    function navigateBackIfNoHistory() {
      if (!ionRouter.canGoBack()) {
        ionRouter.navigate('/fiches', 'back', 'replace')
      }
    }

    this.navigateBack = navigateBackIfNoHistory
  },
  methods: {
    goTo(path: string) {
      this.$router.push(path)
    },
    openCredits() {
      window.open(this.credits)
    },
    async shareSheet() {
      try {
        await Share.share({
          title: `"${this.nom}" sur Remède`,
          text: `La fiche de français "${this.nom}" est sur Remède !`,
          url: `https://remede-app.camarm.fr/fiches/${this.slug}`,
          dialogTitle: 'Partager la fiche',
        })
      } catch {
        alert('Fonctionnalité non supportée par votre navigateur')
      }
    },
    getTagColor(tag: string) {
      switch (tag) {
        case 'orthographe':
          return 'primary'
        case 'grammaire':
          return 'success'
        case 'lexique':
          return 'tertiary'
        case 'conjugaison':
          return 'secondary'
        case 'style':
          return 'warning'
        case 'typographie':
          return 'danger'
        default:
          return 'grey'
      }
    }
  }
})
</script>
