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
      <img src="/og.png" alt="Remède"/>
      <br>
      <br>
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">À propos</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-content class="ion-padding">
        <p>
          Remède est un dictionnaire français libre, construit sur plusieurs services tiers.
        </p>
        <h2>Licence</h2>
        <p>
          Remède est un logiciel libre sous licence <a href="https://github.com/camarm-dev/remede/blob/main/LICENSE" target="_blank">CeCill V2.1</a>, disponible sur <a href="https://github.com/camarm-dev/remede" target="_blank">Github</a>
        </p>
        <ion-list class="ion-no-padding">
          <ion-item button>
            <ion-icon slot="start" :icon="reloadOutline"/>
            <ion-label>
              <h3>Mise à jour</h3>
            </ion-label>
          </ion-item>
          <ion-item button>
            <ion-icon slot="start" :icon="logoGooglePlaystore"/>
            <ion-label>
              <h3>Ouvrir le Store</h3>
            </ion-label>
          </ion-item>
        </ion-list>
        <br>
        <img alt="Powered by Labse Softwares" src="/labse_powered_by.png" />
      </ion-content>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {IonButtons, IonContent, IonHeader, IonIcon, IonMenuButton, IonPage, IonTitle, IonToolbar} from '@ionic/vue';
import {logoGooglePlaystore, reloadOutline} from "ionicons/icons";
</script>

