<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">{{ $t('settings') }}</ion-title>
        </ion-toolbar>
      </ion-header>

      <div class="list-title">
        {{ $t('settingsPage.personalization') }}
      </div>
      <ion-list inset>
        <ion-item color="light">
          <ion-icon slot="start" :icon="contrastOutline"/>
          <ion-select :label="$t('settingsPage.theme')" :value="getCurrentTheme()" :placeholder="$t('settingsPage.lightTheme')" @ionChange="handleThemeChangement($event.detail.value)" :cancel-text="$t('cancel')" :ok-text="$t('confirm')" interface="action-sheet">
            <ion-select-option value="light">{{ $t('settingsPage.lightTheme') }}</ion-select-option>
            <ion-select-option value="dark">{{ $t('settingsPage.darkTheme') }}</ion-select-option>
          </ion-select>
        </ion-item>
        <ion-item color="light">
          <ion-icon slot="start" :icon="languageOutline"/>
          <ion-select :label="$t('settingsPage.tongue')" :value="getCurrentLang()" placeholder="System" @ionChange="handleLangChangement($event.detail.value)" :cancel-text="$t('cancel')" :ok-text="$t('confirm')" interface="action-sheet">
            <ion-select-option v-for="locale in availableLocales" :value="locale" :key="locale">{{ getLocaleName(locale) }}</ion-select-option>
            <ion-select-option value="system">System</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>

      <div class="list-title">
        {{ $t('settingsPage.dictionaries') }}
      </div>

      <ion-list inset>
        <ion-item color="light" button @click="goTo('/settings/offline')">
          <ion-icon slot="start" :icon="fileTrayFullOutline"/>
          <ion-label>{{ $t('settingsPage.downloadedDictionaries') }}</ion-label>
        </ion-item>
        <ion-item v-if="supportsDICT" color="light" button @click="goTo('/settings/servers')">
          <ion-icon slot="start" :icon="radioOutline"/>
          <ion-label>{{ $t('settingsPage.dictServers') }}</ion-label>
        </ion-item>
      </ion-list>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonMenuButton,
  IonPage,
  IonSelect,
  IonSelectOption,
  IonTitle,
  IonToolbar,
  IonItem,
  IonLabel,
  IonList,
} from "@ionic/vue"
import {
  contrastOutline,
  languageOutline,
  radioOutline,
  fileTrayFullOutline
} from "ionicons/icons"
</script>

<script lang="ts">

import {getDeviceLocale} from "@/functions/device"
import locales, {localeCode} from "@/functions/locales"
import {Capacitor} from "@capacitor/core"

export default {
  data() {
    return {
      supportsDICT: Capacitor.getPlatform() === "android" || true,
      availableLocales: this.$i18n.availableLocales as any[] as localeCode[]
    }
  },
  methods: {
    handleThemeChangement(theme: string) {
      localStorage.setItem("userTheme", theme)
      document.body.classList.remove("dark")
      document.body.classList.remove("light")
      document.body.classList.add(theme)
    },
    getLocaleName(locale: localeCode) {
      return locales[locale] || locale
    },
    getCurrentTheme() {
      return localStorage.getItem("userTheme") || "light"
    },
    async handleLangChangement(lang: string) {
      if (lang == "system") {
        localStorage.removeItem("interfaceLanguage")
        this.$i18n.locale = await getDeviceLocale()
        return
      }
      localStorage.setItem("interfaceLanguage", lang)
      this.$i18n.locale = lang
    },
    getCurrentLang() {
      return localStorage.getItem("interfaceLanguage") || "system"
    },
    goTo(path: string) {
      this.$router.push(path)
    }
  }
}
</script>

