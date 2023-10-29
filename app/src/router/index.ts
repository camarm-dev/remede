import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import Outlet from "@/Outlet.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: Outlet,
    children: [
      {
        path: '',
        redirect: '/dictionnaire',
      },
      {
        path: 'dictionnaire',
        component: () => import ('../views/HomePage.vue')
      },
      {
        path: 'fiches',
        component: () => import ('../views/HomePage.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
