import { createWebHistory, createRouter } from 'vue-router'
import HomePage from './views/HomePage.vue'


const routes = [
    //   { path: '/', component: HomePage, meta: { requiresAuth: true } },
    { path: '/', component: HomePage},
    { path: '/login', component: () => import('./views/LoginPage.vue') },

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAuth) {
//     const token = localStorage.getItem('Authentication-Token');
//     if (token) {
//       next(); // User is authenticated, allow access
//     } else {
//       next('/login'); // Redirect to login page if not authenticated
//     }
//   } else {
//     next(); // No authentication required, allow access
//   }
// });

export default router