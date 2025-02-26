<script setup lang="ts">

import {
  readerOutline,
  informationCircleOutline,
  compassOutline,
  saveOutline,
  filterOutline,
  searchOutline
} from "ionicons/icons"
import {
  IonPage,
  IonIcon,
  IonMenuButton,
  IonToolbar,
  IonButtons,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonModal,
  IonLabel,
  IonHeader,
  IonProgressBar
} from "@ionic/vue"
import dictServers from "@/data/dictServers.json"
</script>

<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar class="hidden-desktop">
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
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
          <ion-buttons slot="end">
            <ion-button id="open-servers">
              <ion-icon slot="icon-only" :icon="compassOutline"></ion-icon>
            </ion-button>
          </ion-buttons>
          <div class="field join" slot="start">
            <ion-input class="large" :value="request.server" @ionInput="request.server = ($event.target.value || '').toString(); refreshServer()" type="text" placeholder="dict.org"></ion-input>
            <div class="block">:</div>
            <ion-input :value="request.port" @ionInput="request.port = Number($event.target.value) || 0; refreshServer()" type="number" placeholder="2628"></ion-input>
          </div>
        </ion-toolbar>
        <ion-toolbar class="ion-padding-bottom">
          <ion-buttons slot="end">
            <ion-button id="open-options">
              <ion-icon slot="icon-only" :icon="filterOutline"></ion-icon>
            </ion-button>
          </ion-buttons>
          <div class="field" slot="start">
            <ion-input :value="request.word" @ionInput="handleSearchbarInput(($event.target.value || '').toString())" slot="start" :placeholder="$t('home.searchWord')"></ion-input>
          </div>
          <ion-progress-bar v-if="loading" type="indeterminate" color="medium"
                            style="width: 95%; margin: auto"></ion-progress-bar>
        </ion-toolbar>
      </ion-header>

      <div class="ion-padding">
        <div :key="def.word + def.databaseId" v-for="def in definitions" class="result">
          <h3>{{ def.word }} <span><b>{{ def.database }}</b> ({{ def.databaseId }})</span></h3>
          <p>{{ def.definition }}</p>
        </div>
        <div v-if="definitions.length == 0" class="no-result">
          <p>
            Pas de résultats
          </p>
        </div>
      </div>

      <div class="list-title">{{ $t('dictClient.actions') }}</div>
      <ion-list inset>
        <ion-item button color="light" id="open-logs">
          <ion-icon :icon="readerOutline" slot="start"></ion-icon>
          <ion-label>{{ $t('dictClient.transmissionLogs') }}</ion-label>
        </ion-item>
        <ion-item button color="light">
          <ion-icon :icon="saveOutline" slot="start"></ion-icon>
          <ion-label>{{ $t('dictClient.saveServer') }}</ion-label>
        </ion-item>
      </ion-list>

      <ion-button expand="block" class="ion-margin" @click="refreshResponse()">Rechercher</ion-button>

      <ion-modal trigger="open-servers" :initial-breakpoint="0.75" :breakpoints="[0, .5, 1]">
        <ion-content class="ion-padding-top">
          <div class="list-title">{{ $t('dictClient.myServers') }}</div>
          <ion-list inset>
            <ion-item v-if="savedServers.length == 0" color="light">
              <ion-note color="dark">{{ $t('dictClient.noServerSaved') }}</ion-note>
            </ion-item>
            <ion-item v-else v-for="server in savedServers" :key="server.host" color="light" @click="selectServer(server)" button>
              <ion-label>
                <h3>{{ server.name }}</h3>
                <p>{{ server.description }}</p>
              </ion-label>
            </ion-item>
          </ion-list>
          <div class="list-title">{{ $t('dictClient.exploreServers') }}</div>
          <ion-list inset>
            <ion-item v-for="server in dictServers" :key="server.host" color="light" @click="selectServer(server)" button>
              <ion-label class="formatted">
                <h3>{{ server.name }}</h3>
                <span>{{ server.host }}</span>
                <p>{{ server.description }}</p>
              </ion-label>
            </ion-item>
          </ion-list>
        </ion-content>
      </ion-modal>

      <ion-modal trigger="open-options" :initial-breakpoint="0.75" :breakpoints="[0, .5, 1]">
        <ion-content>
          <h1 class="ion-padding-start ion-padding-top">{{ $t('dictClient.options') }}</h1>
          <ion-list inset>
            <ion-item color="light">
              <ion-select :label="$t('dictionary')" :value="request.database || '!'" @ionChange="request.database = $event.detail.value" interface="action-sheet" :cancelText="$t('cancel')">
                <ion-select-option v-for="db in availableDictionaries" :value="db.id" :key="db.id">{{ db.name }}</ion-select-option>
                <ion-select-option v-if="availableDictionaries.length == 0 && !['', '!', '*', undefined].includes(request.database)" :value="request.database">{{ request.database }}</ion-select-option>
                <ion-select-option value="!">{{ $t('dictClient.all') }} ({{ $t('dictClient.stopsAtFirstMatch') }})</ion-select-option>
                <ion-select-option value="*">{{ $t('dictClient.all') }}</ion-select-option>
              </ion-select>
            </ion-item>
            <ion-item color="light">
              <ion-select :value="request.method || 'DEFINE'" @ionChange="request.method = $event.detail.value" :label="$t('dictClient.strategy')" placeholder="Define" interface="action-sheet" :cancelText="$t('cancel')">
                <ion-select-option value="DEFINE">Define</ion-select-option>
                <ion-select-option value="MATCH">Match</ion-select-option>
              </ion-select>
            </ion-item>
            <ion-item color="light" v-if="request.method == 'MATCH'">
              <ion-select :value="request.strat || '.'" @ionChange="request.strat = $event.detail.value" :label="$t('dictClient.strategy')" placeholder="Prefix" interface="action-sheet" :cancelText="$t('cancel')">
                <ion-select-option v-for="strat in availableStrategies" :value="strat.id" :key="strat.id">{{ strat.name }}</ion-select-option>
                <ion-select-option value=".">{{ $t('dictClient.default') }}</ion-select-option>
              </ion-select>
            </ion-item>
          </ion-list>
        </ion-content>
      </ion-modal>

      <ion-modal trigger="open-logs" :initial-breakpoint="0.75" :breakpoints="[0, .5, 1]">
        <ion-content class="ion-padding">
          <h1>Journaux</h1>
          <ion-list>
            <ion-item
              v-for="log in logs"
              :key="log.raw"
              :color="getLogColor(log)"
            >
              {{ log.raw }}
            </ion-item>
          </ion-list>
        </ion-content>
      </ion-modal>

      <ion-modal trigger="open-info" :initial-breakpoint="0.75" :breakpoints="[0, .75, 1]">
        <ion-content class="ion-padding">
          <h1>Serveurs de dictionnaire</h1>
          <div class="section">
            <div class="icon">
              <ion-icon color="primary" :icon="informationCircleOutline"></ion-icon>
            </div>
            <p>Cette interface te permet d'explorer des serveurs de dictionnaire utilisant le protocole DICT.</p>
          </div>
          <div class="section">
            <div class="icon">
              <ion-icon color="primary" :icon="compassOutline"></ion-icon>
            </div>
            <p>Trouve et explore une grand variété de serveurs de dictionnaires.</p>
          </div>
          <div class="section">
            <div class="icon">
              <ion-icon color="primary" :icon="saveOutline"></ion-icon>
            </div>
            <p>Enregistre de nouveaux serveurs personnalisés. Rends-toi dans les paramètres activer la recherche par serveurs de dictionnaire.</p>
          </div>
          <div class="section">
            <div class="icon">
              <ion-icon color="primary" :icon="searchOutline"></ion-icon>
            </div>
            <p>Sélectionne "Serveurs de dictionnaire" comme source de recherche et parcourt les dictionnaires distants directement dans Remède !</p>
          </div>
        </ion-content>
      </ion-modal>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">

import {
  decodeRequest,
  DictDatabase,
  DictRequest, DictResponseLine, DictStrategy, DictServer, DictRequestType,
  getDictionaries,
  getStrategies,
  makeRequest, DictDefinition
} from "@/functions/dictProtocol"

export default {
  data() {
    return {
      request: {} as DictRequest,
      availableDictionaries: [] as DictDatabase[],
      availableStrategies: [] as DictStrategy[],
      definitions: [] as DictDefinition[],
      logs: [] as DictResponseLine[],
      savedServers: [] as DictServer[],
      searchTimeout: window.setTimeout(() => undefined, 500),
      loading: false,
      errors: []
    }
  },
  mounted() {
    const request = new URLSearchParams(location.search).get("request")
    if (request) {
      this.request = decodeRequest(request)
      this.refreshServer()
      this.refreshResponse()
    }
  },
  methods: {
    async refreshServer() {
      this.loading = true
      this.availableDictionaries = await getDictionaries(this.request.server, this.request.port)
      this.availableStrategies = await getStrategies(this.request.server, this.request.port)
      this.request.database = "!"
      this.request.strat = "."
      this.request.method = DictRequestType.Define
      this.loading = false
    },
    async refreshResponse() {
      this.loading = true
      const { rawDecoded, definitions } = await makeRequest(this.request)
      this.loading = false
      this.logs = rawDecoded
      this.definitions = definitions
    },
    selectServer(server: DictServer) {
      this.request.server = server.host
      this.request.port = server.port
      this.refreshServer()
    },
    handleSearchbarInput(input: string) {
      this.request.word = input
      if (input != "") {
        this.searchTimeout = window.setTimeout(this.refreshResponse, 500)
      } else {
        window.clearTimeout(this.searchTimeout)
        this.definitions = []
      }
    },
    getLogColor(log: DictResponseLine) {
      if (log.type == "HEADER")
        return "medium"
      if (log.type == "COMMAND")
        return "primary"
      return log.success && log.type == "STATUS" ? "success"
          : !log.success ? "danger"
              : "light"
    }
  }
}
</script>

<style scoped>
.field {
  display: flex;
  width: 100%;
  padding-inline-start: 7px;
}

.field ion-input {
  background: rgba(var(--ion-text-color-rgb, 0, 0, 0), 0.07);
  border-radius: 10px;
  padding: 0 12px !important;
  min-height: 36px !important;
}

.field ion-input.large {
  width: 80%;
}

.field ion-input.large + .block + ion-input {
  width: 20%;
}

.field ion-select {
  max-width: 50%;
}

.field.join ion-input:nth-child(1) {
  border-bottom-right-radius: 0;
  border-top-right-radius: 0;
}

.field .block {
  background: rgba(var(--ion-text-color-rgb, 0, 0, 0), 0.07);
  min-height: 36px !important;
  display: flex;
  align-items: center;
  padding-bottom: 4px;
}

.field.join ion-input:last-child {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.result h3 span {
  color: var(--ion-color-medium);
  font-size: 15px;
  font-weight: normal;
  margin-left: auto;
}

.result h3 {
  margin: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result p {
  padding-inline-start: 7px;
}

.no-result {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: var(--ion-color-medium);
}

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

.section {
  display: flex;
  justify-content: start;
  align-items: start;
  gap: 1em;
  margin-top: 2em;
}

.section p {
  margin: 0;
}

.section .icon ion-icon {
  background: rgba(var(--ion-color-primary-rgb), .1);
  margin: 0;
  padding: .4em;
  width: 25px;
  height: 25px;
  border-radius: 50%;
}
</style>
