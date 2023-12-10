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
  IonLabel,
} from "@ionic/vue";
import {chevronBackOutline, pushOutline, shareOutline} from "ionicons/icons";
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
      </ion-buttons>
    </ion-toolbar>
  </ion-header>
  <ion-content :fullscreen="true" class="ion-padding">
    <ion-header collapse="condense">
      <ion-toolbar>
        <ion-label>
          <ion-title class="remede-font ion-wrap" size="large">{{ nom }}</ion-title>
          <p class="ion-padding-start">{{ description }}</p>
        </ion-label>
        <ion-buttons slot="end">
          <ion-button @click="openCredits()">
            <ion-icon slot="icon-only" :icon="pushOutline" color="medium"/>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <br>
    <div class="ion-padding" v-html="contenu"/>
  </ion-content>
</template>

<script lang="ts">
import {useIonRouter} from "@ionic/vue";
import {defineComponent} from "vue";
import {Share} from "@capacitor/share";

export default defineComponent({
  props: ['nom', 'description', 'contenu', 'tags', 'credits', 'slug'],
  data() {
    return {
      navigateBack: () => "" as Function
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
          url: `https://remede.camam.fr/fiche/${this.slug}`,
          dialogTitle: 'Partager la fiche',
        })
      } catch {
        alert('Fonctionnalité non supportée par votre navigateur')
      }
    }
  }
})
</script>
