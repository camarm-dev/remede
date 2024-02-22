<template>
  <ion-page>
    <ion-header>
      <button class="handle"></button>
    </ion-header>
    <ion-content :fullscreen="true">
      <swiper
          :pagination="{ clickable: true, enabled: true }"
          :parallax="{ enabled: true }"
          :modules="[Pagination, Parallax]"
          :speed="600"
      >
        <div
            slot="container-start"
            class="parallax-bg"
            data-swiper-parallax="-23%"
        ></div>
        <swiper-slide>
          <div>
            <div class="title" data-swiper-parallax="-100">
              <h1 class="remede-font no-capitalize">Bienvenue sur <span class="contrast">Remède</span> !</h1>
            </div>
            <div class="subtitle" data-swiper-parallax="-200">
              Votre nouveau dictionnaire préféré !
            </div>
          </div>
          <div
              class="text"
              data-swiper-parallax="-300"
              data-swiper-parallax-duration="600"
          >
            <img class="slide-image remede" :src="Icon" alt="Remède icon"/>
            <img class="image quote" :src="Quote" alt="Remède icon"/>
            <img class="image ellipse" :src="Ellipse" alt="Remède icon"/>
          </div>
          <LandingScreenNextButton class="margin-bottom" text="Commencer"/>
        </swiper-slide>
        <swiper-slide>
          <div>
            <div class="title" data-swiper-parallax="-100">
              <h1 class="remede-font no-capitalize">Une application, tous vos <span class="contrast">mots</span> !</h1>
            </div>
            <div class="subtitle" data-swiper-parallax="-200">
              + 240 000 mots, mais aussi des rimes, des exemples, un correcteur et plus encore... Remède est bien plus qu'un dictionnaire !
            </div>
          </div>
          <div
              class="text"
              data-swiper-parallax="-300"
              data-swiper-parallax-duration="600"
          >
            <img class="slide-image large" :src="FunctionalitiesIllustration" alt="Illustration"/>
          </div>
          <LandingScreenNextButton/>
        </swiper-slide>
        <swiper-slide>
          <div>
            <div class="title" data-swiper-parallax="-100">
              <h1 class="remede-font no-capitalize">Mais surtout ... <span class="contrast">open source</span> !</h1>
            </div>
            <div class="subtitle" data-swiper-parallax="-200">
              Et oui ! Remède grandi avec sa communauté et est 100% open source !
            </div>
          </div>
          <div
              class="text"
              data-swiper-parallax="-300"
              data-swiper-parallax-duration="600"
          >
            <img class="slide-image" :src="OpenSourceIcon" alt="Illustration"/>
          </div>
          <LandingScreenNextButton/>
        </swiper-slide>
        <swiper-slide>
          <div>
            <div class="title" data-swiper-parallax="-100">
              <h1 class="remede-font no-capitalize">Prêts à entrer dans l'<span class="contrast">aventure</span> ?</h1>
            </div>
            <div class="subtitle" data-swiper-parallax="-200">
              Guérir vos maux face au français, c'est possible dès maintenant avec Remède !
            </div>
          </div>
          <div
              class="text"
              data-swiper-parallax="-300"
              data-swiper-parallax-duration="600"
          >
            <img class="slide-image" :src="RocketIcon" alt="Illustration">
          </div>
          <ion-button @click="close()" shape="round" expand="full" fill="outline">
            C'est parti <ion-icon slot="end" :icon="arrowForward"/>
          </ion-button>
        </swiper-slide>
      </swiper>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {
  IonContent,
  IonHeader,
  IonIcon,
  IonPage,
  IonButton
} from "@ionic/vue"
import {Swiper, SwiperSlide} from "swiper/vue"
import {Pagination, Parallax} from "swiper/modules"
import "swiper/css"
import "swiper/css/navigation"
import "@ionic/vue/css/ionic-swiper.css"
import Icon from "@/assets/remede3d.png"
import Quote from "@/assets/quote3d.png"
import Ellipse from "@/assets/ellipse3d.png"
import FunctionalitiesIllustration from "@/assets/functionalities.png"
import RocketIcon from "@/assets/rocket.png"
import OpenSourceIcon from "@/assets/osi.png"
import LandingScreenNextButton from "@/components/LandingScreenNextButton.vue"
import {arrowForward} from "ionicons/icons"

export default {
  components: {
    LandingScreenNextButton,
    IonPage,
    IonHeader,
    IonIcon,
    IonContent,
    Swiper,
    SwiperSlide,
    IonButton
  },
  setup() {
    return {
      Pagination,
      Parallax,
      Icon,
      Quote,
      Ellipse,
      FunctionalitiesIllustration,
      RocketIcon,
      OpenSourceIcon,
      arrowForward
    }
  },
  methods: {
    close() {
      const event = new Event("landingScreenClosed")
      window.dispatchEvent(event)
    },
  }
}
</script>

<style scoped>
.handle {
  width: 36px;
  height: 5px;
  border-radius: 8px;
  display: block;
  margin: 6px auto auto;
  background: var(--ion-color-step-350, #c0c0be) !important;
  cursor: pointer;
}

.no-capitalize {
  text-transform: none;
}

ion-content {
  height: 100%;
}

.swiper, .swiper-wrapper, .swiper-slide {
  height: 100%;
}

.swiper-slide {
  padding: 2em 1em 2.5em;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.remede-font {
  text-align: left;
}

.subtitle {
  text-align: left;
  line-break: strict;
  word-break: normal;
}

.subtitle {
  font-family: "Amiko", sans-serif;
  font-weight: normal;
  color: var(--ion-color-dark-tint);
}

.remede-font {
  font-size: 2em;
  margin-top: 0
}

.contrast {
  color: var(--ion-color-medium);
}

.parallax-bg {
  background-image: url('/parallax-background.png');
  position: absolute;
  left: 0;
  top: 0;
  width: 130%;
  height: 100%;
  -webkit-background-size: cover;
  background-size: cover;
  background-position: center;
}

.slide-image {
  height: 60% !important;
}

.slide-image.large {
  height: 90% !important;
}

.slide-image:not(.remede) {
  animation: floating 10s infinite ease-in-out;
  transition: .5s ease-in-out;
}

@keyframes floating {
  0% {
    transform: translate(0%, 0%);
    scale: 1;
  }
  50% {
    transform: translate(0%, -8%);
  }
  60% {
    transform: translate(0%, -8%);
    scale: 1.05;
  }
  90% {
    transform: translate(0%, 0%);
    scale: 1;
  }
  100% {
    transform: translate(0%, 0%);
    scale: 1;
  }
}

.slide-image.remede {
  rotate: -9deg;
  animation: float 20s infinite ease-in-out;
  transition: .5s ease-in-out;
}

@keyframes float {
  0% {
    transform: translate(0%, 0%);
    scale: 1;
  }
  50% {
    transform: translate(-2%, -8%);
    scale: 1;
  }
  60% {
    transform: translate(-2%, -8%);
    scale: 1.02;
  }
  90% {
    transform: translate(0%, 0%);
    scale: 1.02;
  }
  100% {
    transform: translate(0%, 0%);
    scale: 1;
  }
}

.image {
  width: 4em !important;
  position: absolute;
  z-index: 100;
}

.quote {
  left: 1.5em;
  bottom: 10em;
  animation: float 5s infinite reverse ease-in-out;
  transition: .5s ease-in-out;
}

.ellipse {
  right: 1.5em;
  top: 12em;
  animation: float 5s infinite ease-in-out;
  animation-delay: 3s;
  transition: .5s ease-in-out;
}

.text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-height: 70%;
}
</style>
