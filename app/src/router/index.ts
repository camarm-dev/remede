import { createRouter, createWebHistory } from "@ionic/vue-router"
import { RouteRecordRaw } from "vue-router"
import Outlet from "@/AppOutlet.vue"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: Outlet,
    children: [
      {
        path: "",
        redirect: "/dictionnaire",
      },
      {
        path: "dict",
        name: "dict",
        component: () => import ("../views/DictClient.vue"),
      },
      {
        path: "dictionnaire",
        name: "dictionnaire",
        component: () => import ("../views/HomeView.vue"),
      },
      {
        path: "dictionnaire/:mot",
        component: () => import ("../views/DefinitionView.vue")
      },
      {
        path: "search/:mot",
        component: () => import ("../views/SearchResultsView.vue")
      },
      {
        path: "a-propos",
        component: () => import ("../views/AboutView.vue")
      },
      {
        path: "correction",
        name: "correction",
        component: () => import ("../views/CorrectionView.vue")
      },
      {
        path: "fiches",
        name: "fiches",
        component: () => import ("../views/SheetsView.vue")
      },
      {
        path: "fiches/:slug",
        component: () => import ("../views/ReadSheetView.vue")
      },
      {
        path: "rimes",
        name: "rimes",
        component: () => import ("../views/RhymesDictionaryView.vue")
      },
      {
        path: "rimes/:mot",
        component: () => import ("../views/RhymesDictionarySearchResultsView.vue")
      },
      {
        path: "parametres",
        redirect: "/settings"
      },
      {
        path: "settings",
        component: () => import ("../views/SettingsView.vue")
      },
      {
        path: "settings/offline",
        component: () => import ("../views/SettingsOfflineDictionariesView.vue")
      },
      {
        path: "settings/servers", // TODO
        component: () => import ("../views/SettingsOfflineDictionariesView.vue")
      },
      {
        path: "marques-page",
        component: () => import ("../views/BookmarksView.vue")
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
