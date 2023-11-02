<template>
  <ion-app>
    <ion-split-pane content-id="main-content">
      <ion-menu content-id="main-content" type="overlay">
        <ion-content>
          <ion-list>
            <img class="ion-margin-start" width="50" alt="Remède icon" src="/favicon.png" height="50"/>
            <ion-list-header>Remède</ion-list-header>
            <ion-note>Retrouvez vos mots en toute simplicité</ion-note>

            <div class="menu-links">
              <div class="start">
                <ion-menu-toggle :auto-hide="false">
                  <router-link to="/dictionnaire">
                    <ion-item lines="none" :detail="false" class="hydrated" :class="isPage('/dictionnaire') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="bookOutline"></ion-icon>
                      <ion-label>Dictionnaire</ion-label>
                    </ion-item>
                  </router-link>
                </ion-menu-toggle>
                <ion-menu-toggle :auto-hide="false">
                  <router-link to="/marques-page">
                    <ion-item lines="none" :detail="false" class="hydrated" :class="isPage('/marques-page') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="bookmarkOutline"></ion-icon>
                      <ion-label>Marques Pages</ion-label>
                    </ion-item>
                  </router-link>
                </ion-menu-toggle>
                <ion-menu-toggle :auto-hide="false">
                  <router-link to="/correction">
                    <ion-item lines="none" :detail="false" class="hydrated" :class="isPage('/correction') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="medicalOutline"></ion-icon>
                      <ion-label>Correction</ion-label>
                    </ion-item>
                  </router-link>
                </ion-menu-toggle>
                <ion-menu-toggle :auto-hide="false">
                  <router-link to="/fiches">
                    <ion-item disabled lines="none" :detail="false" class="hydrated" :class="isPage('/fiches') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="documentOutline"></ion-icon>
                      <ion-label>Fiches</ion-label>
                    </ion-item>
                  </router-link>
                </ion-menu-toggle>
              </div>
              <div class="end">
                <ion-menu-toggle :auto-hide="false">
                  <router-link to="/parametres">
                    <ion-item lines="none" :detail="false" class="hydrated" :class="isPage('/parametres') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="cogOutline"></ion-icon>
                      <ion-label>Paramètres</ion-label>
                    </ion-item>
                  </router-link>
                </ion-menu-toggle>
                <ion-menu-toggle :auto-hide="false">
                  <router-link to="/a-propos">
                    <ion-item lines="none" :detail="false" class="hydrated" :class="isPage('/a-propos') ? 'selected': ''">
                      <ion-icon aria-hidden="true" slot="start" :icon="informationCircleOutline"></ion-icon>
                      <ion-label>À propos</ion-label>
                    </ion-item>
                  </router-link>
                </ion-menu-toggle>
              </div>
            </div>
          </ion-list>

        </ion-content>
      </ion-menu>
      <ion-router-outlet id="main-content"></ion-router-outlet>
    </ion-split-pane>
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
  IonListHeader,
  IonMenu,
  IonMenuToggle,
  IonNote,
  IonRouterOutlet,
  IonSplitPane,
} from '@ionic/vue';
import {
  bookOutline,
  informationCircleOutline,
  cogOutline, documentOutline, bookmarkOutline, medicalOutline
} from 'ionicons/icons';

</script>

<script lang="ts">
export default {
  mounted() {
    document.body.classList.add(localStorage.getItem('userTheme') || 'light')
  },
  methods: {
    isPage(path: string) {
      return location.pathname === path
    }
  }
}
</script>

<style scoped>
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
