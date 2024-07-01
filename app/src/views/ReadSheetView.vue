<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button text="Retour" default-href="/fiches"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ fiche.nom }}</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="shareSheet()">
            <ion-icon slot="icon-only" :icon="shareOutline"></ion-icon>
          </ion-button>
          <ion-button :download="`${fiche.slug}.md`" :href="`https://api-remede.camarm.fr/sheets/download/${fiche.slug}`">
            <ion-icon slot="icon-only" :icon="cloudDownloadOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-label>
            <ion-title class="remede-font ion-wrap" size="large">{{ fiche.nom }}</ion-title>
          </ion-label>
          <ion-buttons slot="end">
            <ion-button id="present-credits">
              <ion-icon slot="icon-only" :icon="informationCircleOutline" color="medium"/>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
      <ion-alert
          class="alert"
          trigger="present-credits"
          header="Crédits"
          :sub-header="`Attributions à ${fiche.credits.attributions}`"
          :message="fiche.credits.text">

      </ion-alert>
      <ion-label>
        <p class="ion-padding-start">{{ fiche.description }}</p>
      </ion-label>
      <div class="ion-padding">
        <ion-badge class="ion-margin-end" :color="getTagColor(tag)" :key="tag" v-for="tag in fiche.tags">{{ tag }}</ion-badge>
      </div>
      <br>
      <div class="ion-padding" v-html="fiche.contenu"/>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage } from "@ionic/vue"
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonTitle,
  IonToolbar,
  IonButton,
  IonLabel,
  IonBadge,
  IonAlert,
  IonBackButton
} from "@ionic/vue"
import {
  cloudDownloadOutline,
  informationCircleOutline,
  shareOutline
} from "ionicons/icons"
</script>

<script lang="ts">
import {defineComponent} from "vue"
import {Share} from "@capacitor/share";

export default defineComponent({
  data() {
    return {
      fiche: {
        contenu: "",
        description: "La fiche n'a pas été trouvée !",
        nom: "Pas de fiche",
        tags: [],
        slug: "",
        credits: {
          attributions: "",
          text: ""
        }
      }
    }
  },
  mounted() {
    this.loadSheet()
  },
  methods: {
    async loadSheet() {
      this.fiche = await fetch(`https://api-remede.camarm.fr/sheets/${this.$route.params.slug}`).then(resp => resp.json())
    },
    async shareSheet() {
      try {
        await Share.share({
          title: `"${this.fiche.nom}" sur Remède`,
          text: `La fiche de français "${this.fiche.nom}" est sur Remède !`,
          url: `https://remede-app.camarm.fr/fiches/${this.fiche.slug}`,
          dialogTitle: "Partager la fiche",
        })
      } catch {
        alert("Fonctionnalité non supportée par votre navigateur")
      }
    },
    getTagColor(tag: string) {
      switch (tag) {
        case "orthographe":
          return "primary"
        case "grammaire":
          return "success"
        case "lexique":
          return "tertiary"
        case "conjugaison":
          return "secondary"
        case "style":
          return "warning"
        case "typographie":
          return "danger"
        default:
          return "grey"
      }
    }
  }
})
</script>

