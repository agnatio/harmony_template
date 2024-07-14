import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { ref } from 'vue';
import allRoutes from '@/data/allRoutesMenu.json';

// Function to recursively declare routes for children
function declareRoutes(route) {
  const routes = [];

  // Add parent route
  routes.push({
    path: route.path,
    name: route.name,
    component: () => import(`../views/${route.component}.vue`),
    meta: {
      protected: route.protected // Optionally pass any metadata
    }
  });

  // Add children routes if present
  if (route.children && route.children.length > 0) {
    route.children.forEach(child => {
      const childRoute = {
        path: child.path,
        name: child.name,
        component: () => import(`../views/${child.component}.vue`),
        meta: {
          protected: child.protected // Optionally pass any metadata
        }
      };
      routes.push(childRoute);
    });
  }

  return routes;
}

const routes = [];

// Iterate through allRoutes to declare routes and nested routes
allRoutes.forEach(route => {
  const declaredRoutes = declareRoutes(route);
  routes.push(...declaredRoutes);
});

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const freeNames = allRoutes.filter(route => !route.protected).map(route => route.name);
const accessSource = ref('');

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const storedLoginData = localStorage.getItem('login_data');

  let isAuthenticated = false;

  if (storedLoginData) {
    const parsedLoginData = JSON.parse(storedLoginData);
    isAuthenticated = parsedLoginData?.access_token;
  }

  // Check if route is protected and user is not authenticated
  if (to.meta.protected && !isAuthenticated) {
    next({ name: 'login' });
  } else if (to.name === 'login' && isAuthenticated) {
    // Redirect authenticated users away from the login page
    next({ name: 'home' });
  } else {
    next();
  }
});

export { router, accessSource };