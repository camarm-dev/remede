<template>
  <ion-button data-swiper-parallax-opacity="0.5" fill="clear" expand="full" @click="swiper.slideNext()">
    Continuer <ion-icon slot="end" :icon="chevronForward"/>
  </ion-button>
</template>

<script lang="ts">
import {
  IonButton, IonIcon
} from "@ionic/vue";
import {useSwiper} from "swiper/vue";
import {chevronForward} from "ionicons/icons";

export default {
  components: {
    IonButton,
    IonIcon
  },
  setup() {
    const swiper = useSwiper()
    return {
      swiper,
      chevronForward
    };
  },
}
</script>
