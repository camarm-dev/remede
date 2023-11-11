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
        <h2>Utilitaires</h2>
        <ion-list class="ion-no-padding" inset>
          <ion-item button color="light">
            <ion-icon slot="start" :icon="reloadOutline"/>
            <ion-label>
              <h3>Mise à jour</h3>
            </ion-label>
          </ion-item>
          <ion-item button color="light">
            <ion-icon slot="start" :icon="logoGooglePlaystore"/>
            <ion-label>
              <h3>Ouvrir le Store</h3>
            </ion-label>
          </ion-item>
        </ion-list>
        <h2>Crédits / Source</h2>
        <a href="https://labse.camarm.fr" target="_blank">
          <img width="150" alt="Powered by Labse Softwares" src="/labse_powered_by.png" />
        </a>
        <p>
          <a href="https://github.com/camarm-dev/remede#données-remède" target="_blank">Données Remède</a>
          •
          <a href="https://github.com/camarm-dev/remede" target="_blank">Github</a>
          •
          <a href="https://github.com/camarm-dev/remede/blob/main/LICENSE" target="_blank">Licence Remède</a>
        </p>
      </ion-content>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {IonButtons, IonContent, IonHeader, IonIcon, IonMenuButton, IonPage, IonTitle, IonToolbar, IonItem, IonLabel, IonList} from '@ionic/vue';
import {logoGooglePlaystore, reloadOutline} from "ionicons/icons";
</script>

