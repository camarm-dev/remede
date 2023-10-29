<template>
  <ion-app>
    <ion-nav :root="HomePage"></ion-nav>
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonNav } from '@ionic/vue';
import HomePage from "@/views/HomePage.vue";
</script>
