<template>
  <ion-app>
    <ion-page>
      <ion-split-pane content-id="main-content" when="lg">
        <ion-menu content-id="main-content" type="overlay">
          <ion-content>
            <ion-list>
              <img class="ion-margin-start main-logo" height="50" src="/logo.png" alt="">
              <ion-note>Le dictionnaire.</ion-note>
              <ion-searchbar :value="query" @ionChange="query = $event.detail.value" ref="searchbar" @keydown="handleInput($event)" v-if="path != '/dictionnaire'" class="hidden-mobile" placeholder="Rechercher un mot..."></ion-searchbar>
              <div class="menu-links">
                <div class="start">
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/dictionnaire')" lines="none" :detail="false" class="hydrated" :class="path === '/dictionnaire' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="bookOutline"></ion-icon>
                      <ion-label>Dictionnaire</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/correction')" lines="none" :detail="false" class="hydrated" :class="path === '/correction' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="medicalOutline"></ion-icon>
                      <ion-label>Correction</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/fiches')" lines="none" :detail="false" class="hydrated" :class="path === '/fiches' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="documentOutline"></ion-icon>
                      <ion-label>Fiches</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item :disabled="!downloaded" @click="goTo('/rimes')" lines="none" :detail="false" class="hydrated" :class="path === '/rimes' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="swapHorizontalOutline"></ion-icon>
                      <ion-label>Rimes</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                </div>
                <div class="end">
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/marques-page')" lines="none" :detail="false" class="hydrated" :class="path === '/marques-page' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="bookmarkOutline"></ion-icon>
                      <ion-label>Marques Pages</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/parametres')" lines="none" :detail="false" class="hydrated" :class="path === '/parametres' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="cogOutline"></ion-icon>
                      <ion-label>Paramètres</ion-label>
                    </ion-item>
                  </ion-menu-toggle>
                  <ion-menu-toggle :auto-hide="false">
                    <ion-item @click="goTo('/a-propos')" lines="none" :detail="false" class="hydrated" :class="path === '/a-propos' ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="informationCircleOutline"></ion-icon>
                      <ion-label>À propos</ion-label>
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
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonMenu,
  IonMenuToggle,
  IonNote,
  IonRouterOutlet,
  IonSplitPane,
  IonApp,
  IonPage,
  IonSearchbar
} from "@ionic/vue"
import {
  bookOutline,
  informationCircleOutline,
  cogOutline, documentOutline, bookmarkOutline, medicalOutline, swapHorizontalOutline
} from "ionicons/icons"
</script>

<script lang="ts">
import {useRouter} from "vue-router"
import {getOfflineDictionaryStatus} from "@/functions/offline"
import { App } from "@capacitor/app"
import {defineComponent, Ref} from "vue";

export default defineComponent({
  mounted() {
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
  data() {
    return {
      router: useRouter(),
      path: location.pathname,
      downloaded: false,
      query: ''
    }
  },
  methods: {
    handleKeyDown(event: KeyboardEvent) {
      const searchbar = this.$refs.searchbar?.$el as HTMLIonSearchbarElement
      if (!searchbar.focused && !["dictionnaire", "fiches", "correction", "rimes"].includes(this.$route.name as string)) {
        searchbar.setFocus().then(() => {
          if (!searchbar.focused) {
            if (event.key == "backspace") {
              this.query = this.query.slice(0, this.query.length - 1)
              return
            }
            this.query += event.key.length == 1 ? event.key: ''
            return
          }
        })
      }
      switch (event.key) {
        case "Escape":
          this.$router.back()
        default:
            return
      }
    },
    isPage(path: string) {
      return location.pathname === path
    },
    goTo(path: string) {
      this.router.push(path)
      this.path = path
    },
    handleInput(event: KeyboardEvent) {
      const input = event.target as HTMLInputElement
      if(event.key == 'Enter') this.goTo(`/search/${input.value}`)
    }
  }
})
</script>

<style scoped>
.main-logo {
  max-height: 1.2em;
  width: max-content;
}

ion-menu {
  width: max-content;
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
