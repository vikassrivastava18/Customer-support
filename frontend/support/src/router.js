import { createWebHistory, createRouter } from 'vue-router'
import HomePage from './views/HomePage.vue'


const routes = [
    { path: '/', component: HomePage, meta: { requiresAuth: true } },
    { path: '/login', component: () => import('./views/LoginPage.vue')},
    { path: '/books', component: () => import('./views/BookPage.vue')},
    { path: '/tickets', component: () => import('./views/TicketsPage.vue'), meta: { requiresAuth: true }},
    { path: '/create-ticket', component: () => import('./views/CreateTicket.vue'), meta: { requiresAuth: true }},
    { path: '/staff', component: () => import('./views/AdminPage.vue'), meta: { requiresAuth: true }},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('Authentication-Token');
    if (token) {
      next(); // User is authenticated, allow access
    } else {
      next('/login'); // Redirect to login page if not authenticated
    }
  } else {
    next(); // No authentication required, allow access
  }
});

export default router