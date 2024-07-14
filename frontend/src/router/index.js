import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { ref } from 'vue';
import allRoutes from '@/data/allRoutesMenu.json';

const routes = allRoutes.map(route => ({
  path: route.path,
  name: route.name,
  component: () => import(`../views/${route.component}.vue`),
}));

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const freeNames = allRoutes.filter(route => !route.protected).map(route => route.name);
console.log(freeNames)
const accessSource = ref('');

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
