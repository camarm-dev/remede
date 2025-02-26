<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button :text="$t('back')" default-href="/settings"></ion-back-button>
        </ion-buttons>
        <ion-buttons slot="end">
          <ion-button id="open-dict-info">
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
        {{ $t('settings') }}
      </div>

      <ion-list inset>
        <ion-item color="light">
          <ion-toggle>
            {{ $t('settingsPage.DICTSearch') }}
          </ion-toggle>
        </ion-item>
        <ion-item color="light" button>
          <ion-icon :icon="addOutline" slot="start"></ion-icon>
          <ion-label>{{ $t('settingsPage.addServer') }}</ion-label>
        </ion-item>
      </ion-list>

      <div class="list-title">
        {{ $t('dictClient.myServers') }}
      </div>

      <ion-list inset>
        <ion-item v-if="savedServers.length == 0" color="light">
          <ion-note color="dark">{{ $t('dictClient.noServerSaved') }}</ion-note>
        </ion-item>
        <ion-item v-else v-for="server in savedServers" :key="server.host" color="light">
          <ion-toggle>
            <ion-label>
              <h3>{{ server.name }}</h3>
              <p>{{ server.description }}</p>
            </ion-label>
          </ion-toggle>
        </ion-item>
      </ion-list>

      <div class="list-title">
        {{ $t('settingsPage.serversRepertory') }}
      </div>
      <ion-list inset>
        <ion-item v-for="server in dictServers" :key="server.host" color="light">
          <ion-toggle>
            <ion-label class="formatted">
              <h3>{{ server.name }}</h3>
              <span>{{ server.host }}</span>
              <p>{{ server.description }}</p>
            </ion-label>
          </ion-toggle>
        </ion-item>
      </ion-list>

      <ion-modal trigger="open-dict-info" :initial-breakpoint="0.75" :breakpoints="[0, .75, 1]">
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
    IonToggle
} from "@ionic/vue"
import {
  addOutline,
  informationCircleOutline
} from "ionicons/icons"
import DictServersGuide from "@/components/DictServersGuide.vue"
import dictServers from "@/data/dictServers.json"
</script>

<script lang="ts">
import {DictServer} from "@/functions/dictProtocol"

export default {
  data() {
    return {
      savedServers: [] as DictServer[]
    }
  },
  methods: {
  }
}
</script>
<style scoped>
.formatted h3 {
  font-size: 1.15em;
  margin: 0;
  line-height: .9em;
}

.formatted span {
  font-size: .9em;
  color: var(--ion-color-medium);
  margin: 0;
}

.formatted p {
  margin-top: 2px;
}
</style>
