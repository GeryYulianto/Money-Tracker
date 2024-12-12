import { createWebHistory, createRouter } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import('../components/login/login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: "/main",
    component: () => import('../components/workspace/workspace.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: "/add",
    component: () => import('../components/form_transaction/formTransaction.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: "/card",
    component: () => import('../components/transaction_card/transactionCard.vue'),
    meta: { requiresAuth: true }
  },

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
  linkActiveClass: 'active'
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('jwt_token');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/");  // Redirect to login if not authenticated
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next("/main");  // Redirect to main if authenticated and trying to access login
  } else {
    next();
  }
})

export default router;