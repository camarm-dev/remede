<template>
  <ion-page>
    <WordModal :mot-remede="this.$route.params.mot"/>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage } from "@ionic/vue"
import WordModal from "@/components/WordModal.vue"
</script>

