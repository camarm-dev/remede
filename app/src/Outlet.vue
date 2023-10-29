<template>
  <ion-app>
    <ion-nav :root="Root"></ion-nav>
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonNav } from '@ionic/vue';
import Root from "@/Root.vue";
</script>
