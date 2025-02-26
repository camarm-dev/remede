<script setup lang="ts">
import {
  IonContent,
  IonIcon
} from "@ionic/vue"
import {compassOutline, informationCircleOutline, saveOutline, searchOutline} from "ionicons/icons"
</script>

<template>
  <ion-content class="ion-padding">
    <h1>{{ $t('settingsPage.dictServers') }}</h1>
    <div class="section">
      <div class="icon">
        <ion-icon color="primary" :icon="informationCircleOutline"></ion-icon>
      </div>
      <p>{{ $t('settingsPage.information1RemedeDictClient') }}</p>
    </div>
    <div class="section">
      <div class="icon">
        <ion-icon color="primary" :icon="compassOutline"></ion-icon>
      </div>
      <p>{{ $t('settingsPage.information2ExploreServers') }}</p>
    </div>
    <div class="section">
      <div class="icon">
        <ion-icon color="primary" :icon="saveOutline"></ion-icon>
      </div>
      <p>{{ $t('settingsPage.information3SaveCustomServers') }}</p>
    </div>
    <div class="section">
      <div class="icon">
        <ion-icon color="primary" :icon="searchOutline"></ion-icon>
      </div>
      <p>{{ $t('settingsPage.information4HowToUse') }}</p>
    </div>
  </ion-content>
</template>

<style scoped>
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
