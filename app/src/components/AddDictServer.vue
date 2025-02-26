<script setup lang="ts">
import {
  IonContent,
  IonInput,
  IonTextarea,
  IonButton,
  IonNote
} from "@ionic/vue"
import {addServer} from "@/functions/dictPreferences"
</script>

<template>
  <ion-content>
    <h1 class="ion-padding-start ion-padding-top">{{ $t('settingsPage.addServer') }}</h1>

    <div class="list-title">Connexion</div>
    <ion-list inset>
      <div class="field join">
        <ion-input class="large" :value="newServer.host" @ionInput="newServer.host = ($event.target.value || '').toString(); testServer()" type="text" placeholder="dict.org"></ion-input>
        <div class="block">:</div>
        <ion-input :value="newServer.port" @ionInput="newServer.port = Number($event.target.value) || 0" type="number" placeholder="2628"></ion-input>
      </div>
      <ion-note v-if="validServer === undefined" color="light" class="ion-padding-horizontal">{{ $t('dictClient.loading') }}</ion-note>
      <ion-note v-else-if="!validServer" color="danger" class="ion-padding-horizontal">{{ $t('dictClient.invalidServer') }}</ion-note>
      <ion-note v-else color="success" class="ion-padding-horizontal">{{ $t('dictClient.validServer') }}</ion-note>
    </ion-list>

    <div class="list-title">Métadonnées</div>
    <ion-list inset>
      <ion-item color="light">
        <ion-input label-placement="stacked" @ionInput="newServer.name = ($event.target.value || '').toString()" label="Nom" placeholder="My DICT server"></ion-input>
      </ion-item>
      <ion-item color="light">
        <ion-textarea label-placement="stacked" @ionInput="newServer.description = $event.target.value || ''" label="Description" placeholder="My self hosted DICT server."></ion-textarea>
      </ion-item>
    </ion-list>

    <ion-button expand="block" class="ion-padding-horizontal" :disabled="!validServer || newServer.name == '' || newServer.description == ''" @click="addServer(newServer).then(() => close())">Enregistrer</ion-button>
  </ion-content>
</template>

<script lang="ts">
import {DictServer} from "@/functions/dictProtocol"
import TCPClient from "@/functions/plugins/tcpClient"

export default {
  props: {
    host: {
      type: String,
      required: false,
      default: ""
    },
    port: {
      type: Number,
      required: false,
      default: 2628
    },
    close: {
      type: Function,
      required: true,
      default: () => undefined
    }
  },
  data() {
    return {
      newServer: {
        host: this.host,
        port: this.port,
        name: "",
        description: ""
      } as DictServer,
      testTimeout: window.setTimeout(() => undefined, 500),
      validServer: false as boolean | undefined
    }
  },
  methods: {
    testServer() {
      window.clearTimeout(this.testTimeout)
      window.setTimeout(() => {
        this.validServer = undefined
        TCPClient.request({
          host: this.newServer.host,
          port: this.newServer.port,
          messages: ["SHOW SERVER"]
        })
            .catch(() => {
              this.validServer = false
            })
            .then(() => {
              this.validServer = true
            })
      }, 500)
    }
  }
}
</script>
<style scoped>
.field {
  padding: 0 !important;
  border-radius: 10px;
  background: var(--ion-color-light, #f4f5f8) !important;
}

.field ion-input, .field .block {
  background: var(--ion-color-light, #f4f5f8) !important;
}
</style>
