<template>
  <ion-app>
    <ion-page>
      <ion-split-pane content-id="main-content" when="lg">
        <ion-menu content-id="main-content" type="overlay">
          <ion-content>
            <ion-list>
              <RemedeLogo class="ion-margin-start"/>
              <ion-note>{{ $t('theDictionary') }}</ion-note>
              <ion-searchbar :value="query" @ionChange="query = $event.detail.value as string" ref="searchbar" @keydown.enter="handleFastSearch($event.target.value)" :class="`hidden-mobile ${isPage('/dictionnaire') ? 'hidden': ''}`" :placeholder="$t('home.searchWord')"></ion-searchbar>
              <div class="menu-links">
                <div class="start">
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/dictionnaire')" lines="none" :detail="false" class="hydrated" :class="isPage('/dictionnaire') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="bookOutline"></ion-icon>
                      <ion-label>{{ $t('dictionary') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/correction')" lines="none" :detail="false" class="hydrated" :class="isPage('/correction') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="medicalOutline"></ion-icon>
                      <ion-label>{{ $t('correction') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/fiches')" lines="none" :detail="false" class="hydrated" :class="isPage('/fiches') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="documentOutline"></ion-icon>
                      <ion-label>{{ $t('sheets') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item :disabled="!downloaded" @click="goTo('/rimes')" lines="none" :detail="false" class="hydrated" :class="isPage('/rimes') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="swapHorizontalOutline"></ion-icon>
                      <ion-label>{{ $t('rhymes') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                </div>
                <div class="end">
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/marques-page')" lines="none" :detail="false" class="hydrated" :class="isPage('/marques-page') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="bookmarkOutline"></ion-icon>
                      <ion-label>{{ $t('bookmarks') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/parametres')" lines="none" :detail="false" class="hydrated" :class="isPage('/parametres') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="cogOutline"></ion-icon>
                      <ion-label>{{ $t('settings') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/a-propos')" lines="none" :detail="false" class="hydrated" :class="isPage('/a-propos') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="informationCircleOutline"></ion-icon>
                      <ion-label>{{ $t('about') }}</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                </div>
              </div>
            </ion-list>
          </ion-content>
        </ion-menu>
        <ion-router-outlet id="main-content"></ion-router-outlet>
      </ion-split-pane>
    </ion-page>
  </ion-app>
</template>

<script setup lang="ts">
import {
  IonApp,
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonMenu,
  IonMenuToggle,
  IonNote,
  IonPage,
  IonRouterOutlet,
  IonSearchbar,
  IonSplitPane
} from "@ionic/vue"
import {
  bookmarkOutline,
  bookOutline,
  cogOutline,
  documentOutline,
  informationCircleOutline,
  medicalOutline,
  swapHorizontalOutline
} from "ionicons/icons"
import RemedeLogo from "@/components/RemedeLogo.vue"
</script>

<script lang="ts">
import {useRouter} from "vue-router"
import {getOfflineDictionaryStatus} from "@/functions/offline"
import { App } from "@capacitor/app"
import {defineComponent} from "vue"
import {wordExists} from "@/functions/dictionnary"
import {getDeviceLocale} from "@/functions/device"

export default defineComponent({
  mounted() {
    this.router.afterEach(() => {
      this.path = location.pathname
    })
    document.body.classList.add(localStorage.getItem("userTheme") || "light")
    getOfflineDictionaryStatus().then(status => {
      this.downloaded = status.downloaded
    })

    App.getLaunchUrl().then(object => {
      const url = object ? object.url: ""
      if (url.startsWith("remede://")) {
        this.router.push(url.replaceAll("remede:/", ""))
      }
    })
    window.addEventListener("keydown", this.handleKeyDown)
  },
  beforeMount() {
    this.setLocale()
  },
  data() {
    return {
      router: useRouter(),
      path: location.pathname,
      downloaded: false,
      query: ""
    }
  },
  methods: {
    async setLocale() {
      this.$i18n.locale = localStorage.getItem("interfaceLanguage") || await getDeviceLocale()
    },
    async handleFastSearch(query: string) {
      if (await wordExists(query)) {
        this.goTo(`/dictionnaire/${query}`)
      } else {
        this.goTo(`/search/${query}`)
      }
    },
    async handleKeyDown(event: KeyboardEvent) {
      switch (event.key) {
        case "Escape":
          this.$router.back()
          return
      }
      const searchbar = (this.$refs.searchbar as any).$el
      if (!searchbar?.focused && !["dictionnaire", "fiches", "correction", "rimes"].includes(this.$route.name as string)) {
        await searchbar.setFocus()
        if (!searchbar.focused) {
          if (event.key == "backspace") {
            this.query = this.query.slice(0, this.query.length - 1)
            return
          }
          this.query += event.key.length == 1 ? event.key: ""
          return
        }
      }
    },
    isPage(path: string) {
      return this.path === path
    },
    goTo(path: string) {
      this.router.push(path)
    }
  }
})
</script>

<style scoped>
ion-menu-toggle {
  cursor: pointer;
}

ion-menu {
  z-index: 1000000;
}

ion-menu ion-content {
  --background: var(--ion-item-background, var(--ion-background-color, #fff));
}

ion-menu.ios ion-content {
  --padding-bottom: 20px;
}

ion-menu.ios ion-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px 0 0 0;
}

ion-menu.ios ion-note {
  line-height: 24px;
  margin-bottom: 20px;
}

ion-menu.ios ion-item {
  --padding-start: 16px;
  --padding-end: 16px;
  --min-height: 50px;
}

ion-menu.ios ion-item.selected ion-icon {
  color: var(--ion-color-primary);
}

ion-menu.ios ion-item ion-icon {
  font-size: 24px;
  color: #73849a;
}

ion-menu.ios ion-list#labels-list ion-list-header {
  margin-bottom: 8px;
}

ion-menu.ios ion-list-header,
ion-menu.ios ion-note {
  padding-left: 16px;
  padding-right: 16px;
}

ion-menu.ios ion-note {
  margin-bottom: 8px;
}

ion-note {
  display: inline-block;
  font-size: 16px;

  color: var(--ion-color-medium-shade);
}

ion-item.selected {
  --color: var(--ion-color-primary);
}

.first-end-element {
  margin-top: 100%;
}

ion-menu-toggle * {
  text-decoration: none;
}

.menu-links {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}
</style>
