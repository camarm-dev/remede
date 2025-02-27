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
        <ion-item color="light" button id="add-dict-server">
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
        <ion-item-sliding v-else v-for="server in savedServers" :key="server.host">
          <ion-item color="light">
            <ion-toggle>
              <ion-label class="formatted">
                <h3>{{ server.name }}</h3>
                <span>{{ server.host }}</span>
                <p>{{ server.description }}</p>
              </ion-label>
            </ion-toggle>
          </ion-item>
          <ion-item-options>
            <ion-item-option color="danger" @click="deleteServer(server).then(refreshSavedServers)"><ion-icon slot="icon-only" :icon="trashOutline"/></ion-item-option>
          </ion-item-options>
        </ion-item-sliding>

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

      <ion-modal trigger="add-dict-server" ref="addServerModal" :initial-breakpoint="0.75" :breakpoints="[0, .75, 1]" @didDismiss="refreshSavedServers()">
        <AddDictServer :close="closeAddServerModal"/>
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
    IonToggle,
    IonItemSliding,
  IonItemOptions,
  IonItemOption
} from "@ionic/vue"
import {
  addOutline,
  informationCircleOutline, trashOutline
} from "ionicons/icons"
import DictServersGuide from "@/components/DictServersGuide.vue"
import dictServers from "@/data/dictServers.json"
import AddDictServer from "@/components/AddDictServer.vue"
import {deleteServer} from "@/functions/dictPreferences"
</script>

<script lang="ts">
import {DictServer} from "@/functions/dictProtocol"
import {getSavedDictServers} from "@/functions/dictPreferences"

export default {
  data() {
    return {
      savedServers: [] as DictServer[]
    }
  },
  mounted() {
    this.refreshSavedServers()
  },
  methods: {
    async refreshSavedServers() {
      this.savedServers = await getSavedDictServers()
    },
    closeAddServerModal() {
      this.$refs.addServerModal.$el.dismiss()
    }
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
