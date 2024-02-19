<template>
  <ion-page>
    <FicheModal v-bind="fiche" />
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage } from "@ionic/vue"
import FicheModal from "@/components/FicheModal.vue"
</script>

<script lang="ts">

export default {
  data() {
    return {
      fiche: {
        contenu: "",
        description: "La fiche n'a pas été trouvée !",
        nom: "Pas de fiche",
        tags: [],
        slug: "",
        credits: ""
      }
    }
  },
  mounted() {
    this.loadSheet()
  },
  methods: {
    async loadSheet() {
      this.fiche = await fetch(`https://api-remede.camarm.fr/sheets/${this.$route.params.slug}`).then(resp => resp.json())
    }
  }
}
</script>

