import { createWebHistory, createRouter } from "vue-router";

  const routes =  [
    {
    path: "/",
    component: () => import('../components/login/Login.vue'),
  },
  {
    path: "/add",
    component: () => import('../components/form_transaction/formTransaction.vue'),
  },
  {
    path: "/main",
    component: () => import('../components/workspace/workspace.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
  linkActiveClass: 'active'
})



export default router;