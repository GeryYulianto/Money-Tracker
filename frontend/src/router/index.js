import { createWebHistory, createRouter } from "vue-router";

  // array routes yang akan digunakan
  const routes =  [
    {
    path: "/",
    component: () => import('../components/login/Login.vue'),
  },
  {
    path: "/main",
    component: () => import('../components/workspace/workspace.vue'),
  },
  {
    path: "/add",
    component: () => import('../components/form_transaction/formTransaction.vue'),
  },
  {
    path: "/more",
    component: () => import('../components/transaction_card/transactionCard.vue'),
  },
  {
    path: "/card",
    component: () => import('../components/transaction_card/test2.vue'),
  },
]

// Create router
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
  linkActiveClass: 'active'
})

export default router;