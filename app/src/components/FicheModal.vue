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
  IonBadge,
  IonAlert,
  useIonRouter,
  useBackButton
} from "@ionic/vue";
import {
  chevronBackOutline,
  cloudDownloadOutline,
  informationCircleOutline,
  shareOutline
} from "ionicons/icons";

const ionRouter = useIonRouter()

useBackButton(110, () => {
  if (ionRouter.canGoBack()) {
    ionRouter.back()
    return
  }
  ionRouter.navigate('/fiches', 'back', 'replace')
});
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
        :sub-header="`Attributions à ${credits.attributions}`"
        :message="credits.text">

    </ion-alert>
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
import {defineComponent} from "vue";
import {Share} from "@capacitor/share";
import {navigateBackFunction} from "@/functions/types/utils";

export default defineComponent({
  props: ['nom', 'description', 'contenu', 'tags', 'credits', 'slug'],
  data() {
    return {
      navigateBack: function () {
        return false
      } as navigateBackFunction
    }
  },
  mounted() {
    function navigateBackIfNoHistory() {
      if (!ionRouter.canGoBack()) {
        ionRouter.navigate('/fiches', 'back', 'replace')
        return true
      }
      return false
    }

    this.navigateBack = navigateBackIfNoHistory
  },
  methods: {
    goTo(path: string) {
      this.$router.push(path)
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
    },
  }
})
</script>
<style>
.alert .alert-message {
  text-align: justify;
  color: var(--ion-color-medium);
}

b, strong {
  display: inline-block;
  transition: .5s ease-in-out;
  font-weight: normal;
  margin-top: 0;
  padding: 0 5px;
  margin-bottom: 0;
  background: linear-gradient(to right, rgba(255, 235, 9, 0.5), rgba(255, 235, 9, 0.4), rgba(255, 235, 9, 0.5));
  border-radius: 3px;
}

b:hover, strong:hover {
  z-index: 50;
  transform: translateY(-1px);
  transition: .5s ease-in-out;
  cursor: pointer;
  background: var(--ion-color-light);
}

blockquote {
  margin-left: 5px;
  border-left: 4px rgba(var(--ion-color-primary-rgb), .7) solid;
  background-color: var(--ion-color-light);
  padding-left: 7px;
  border-radius: 3px;
  padding-top: 3px;
  padding-bottom: 3px;
}

blockquote p {
  margin: 0;
  padding-top: 5px;
  padding-bottom: 5px;
}

a {
  color: var(--ion-color-primary);
  text-decoration: none;
}

a:hover {
  color: var(--ion-color-primary-tint);
  text-decoration: underline var(--ion-color-primary-tint);
}
</style>