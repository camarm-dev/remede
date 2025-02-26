<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button :text="$t('back')" default-href="/settings"></ion-back-button>
        </ion-buttons>
        <ion-buttons slot="end">
          <ion-button id="open-info">
            <ion-icon slot="icon-only" :icon="informationCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">{{ $t('settingsPage.dictServers') }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <div class="list-title">
      </div>

      <ion-modal trigger="open-info" :initial-breakpoint="0.75" :breakpoints="[0, .75, 1]">
        <DictServersGuide/>
      </ion-modal>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonPage,
  IonTitle,
  IonToolbar,
  IonItem,
  IonLabel,
  IonList, IonModal, IonBackButton,
} from "@ionic/vue"
import {
  informationCircleOutline
} from "ionicons/icons"
import DictServersGuide from "@/components/DictServersGuide.vue"
</script>

<script lang="ts">
export default {
  data() {
    return {
    }
  },
  methods: {
  }
}
</script>

