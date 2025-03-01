<script setup lang="ts">
import {arrowBackOutline, arrowForwardOutline} from "ionicons/icons"
import {IonIcon, IonLabel} from "@ionic/vue"
</script>

<template>
  <ion-list>
    <ion-item
        v-for="log in logs"
        :key="log.raw"
        :color="getLogColor(log)"
        lines="none"
    >
      <ion-icon slot="start" :icon=" log.type != 'COMMAND' ? arrowBackOutline : arrowForwardOutline"></ion-icon>
      <ion-label>{{ log.raw }}</ion-label>
    </ion-item>
  </ion-list>
</template>

<script lang="ts">
import {PropType} from "vue"
import {DictResponseLine} from "@/functions/dictProtocol"

export default {
  props: {
    logs: {
      type: Object as PropType<DictResponseLine[]>
    }
  },
  methods: {
    getLogColor(log: DictResponseLine) {
      if (log.type == "HEADER")
        return "medium"
      if (log.type == "COMMAND")
        return "primary"
      return log.success && log.type == "STATUS" ? "success"
          : !log.success ? "danger"
              : "light"
    }
  }
}
</script>
<style scoped>
ion-list {
  border-radius: 12px;
}

ion-item::part(native) {
  background: rgba(var(--ion-color-base-rgb), .1);
  color: var(--ion-color-base);
}

ion-item.ion-color-light::part(native) {
  color: var(--ion-text-color);
}
</style>
