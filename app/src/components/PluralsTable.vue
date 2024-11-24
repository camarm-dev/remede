<script setup lang="ts">

import {IonItem, IonLabel, IonList} from "@ionic/vue"
</script>

<template>
  <ion-list inset class="border-radius border">
    <ion-item color="light" lines="full">
      <ion-label slot="start" v-if="plurals.some(plural => plural.label != '')">
        <p>{{ $t('definition.form') }}</p>
      </ion-label>
      <ion-label slot="start">
        <p>{{ $t('definition.singular') }}</p>
      </ion-label>
      <ion-label slot="end">
        <p>{{ $t('definition.plural') }}</p>
      </ion-label>
    </ion-item>
    <ion-item lines="full" v-for="plural in plurals">
      <ion-label slot="start" v-if="plurals.some(plural => plural.label != '')">
        <h5 v-html="plural.label"/>
      </ion-label>
      <ion-label slot="start">
        <h5 v-html="plural.singular"/>
      </ion-label>
      <ion-label slot="end">
        <h5 v-html="plural.plural"/>
      </ion-label>
    </ion-item>
  </ion-list>
</template>

<script lang="ts">
import {PropType} from "vue"
import {RemedeWordDocument} from "@/functions/types/remede";

export default {
  props: {
    plurals: {
      type: Object as PropType<RemedeWordDocument["plurals"]>,
      required: true
    }
  }
}
</script>
