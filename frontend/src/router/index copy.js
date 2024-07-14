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

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  const storedLoginData = localStorage.getItem('login_data');

  console.log("storedLoginData: ", storedLoginData);

  let isAuthenticated = false;

  if (storedLoginData) {
    const parsedLoginData = JSON.parse(storedLoginData);
    isAuthenticated = parsedLoginData?.access_token;
    console.log('parsedLoginData: ', parsedLoginData);
    console.log('isAuthenticated: ', isAuthenticated);
  }

  if (!freeNames.includes(to.name) && !isAuthenticated) {
    accessSource.value = to.name;
    console.log(accessSource.value);
    next({ name: 'login' });
  } else if (to.name === 'login' && isAuthenticated) {
    // Redirect authenticated users away from the login page
    next({ name: 'home' });
  } else {
    next();
  }
});


export { router, accessSource };