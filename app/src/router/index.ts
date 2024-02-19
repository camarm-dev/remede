import { createRouter, createWebHistory } from "@ionic/vue-router"
import { RouteRecordRaw } from "vue-router"
import Outlet from "@/AppOutlet.vue"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/dictionnaire/:mot",
    component: () => import ("../views/WordPage.vue")
  },
  {
    path: "/fiches/:slug",
    component: () => import ("../views/FichePage.vue")
  },
  {
    path: "/rimes/:mot",
    component: () => import ("../views/RimeQueryPage.vue")
  },
  {
    path: "/",
    component: Outlet,
    children: [
      {
        path: "",
        redirect: "/dictionnaire",
      },
      {
        path: "dictionnaire",
        component: () => import ("../views/HomePage.vue")
      },
      {
        path: "a-propos",
        component: () => import ("../views/AboutPage.vue")
      },
      {
        path: "correction",
        component: () => import ("../views/CorrectionPage.vue")
      },
      {
        path: "fiches",
        component: () => import ("../views/FichesPage.vue")
      },
      {
        path: "rimes",
        component: () => import ("../views/RimesPage.vue")
      },
      {
        path: "parametres",
        component: () => import ("../views/SettingsPage.vue")
      },
      {
        path: "marques-page",
        component: () => import ("../views/FavoritesPage.vue")
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
