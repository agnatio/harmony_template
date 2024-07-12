// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import { useAuthStore } from '@/stores/authStore';
import { ref } from 'vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/dummyprotected',
    name: 'dummyprotected',
    component: () => import('../views/DummyProtectedView.vue'),
  }

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const freeNames = ['home', 'login', 'register']
const accessSource = ref('')

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token');

  // const fullUrl = window.location.href; // Get the full URL
  // const baseUrl = window.location.origin; // Get the base URL (scheme + host + port)
  // const urlPath = fullUrl.replace(baseUrl, ''); // Subtract base URL to get the path
  // console.log("URL:", urlPath);
  // // console.log("TO: ", to);
  // // console.log("FROM:", from);
  // console.log("freeNames.includes(to.name): ", freeNames.includes(urlPath))
  // console.log("isAuthenticated: ", isAuthenticated)
  // debugger
  if (!freeNames.includes(to.name) && !isAuthenticated) {
    accessSource.value = to.name
    console.log(accessSource.value)
    next({ name: 'login' })
  }
  // to.name !== 'login' && 
  else next()

})

export { router, accessSource };
