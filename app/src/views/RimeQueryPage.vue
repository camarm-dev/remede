<template>
  <ion-page>
    <RimePage :query-word="mot" />
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage } from "@ionic/vue"
import RimePage from "@/views/RimesPage.vue"
</script>

<script lang="ts">

export default {
  data() {
    return {
      mot: ""
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.mot = this.$route.params.mot
    }
  }
}
</script>

