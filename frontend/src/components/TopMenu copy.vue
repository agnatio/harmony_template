<template>
    <nav class="flex justify-between items-center border border-sky-600 text-sm bg-sky-200 px-10">
        <div class="flex items-center gap-4">
            <router-link v-for="route in filteredLeftRoutes" :key="route.name" :to="route.path"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1" active-class="font-bold">
                {{ route.name.charAt(0).toUpperCase() + route.name.slice(1) }}
            </router-link>
        </div>
        <div class="flex items-center gap-8">
            <span v-if="authStore.isAuthenticated && authStore.loginDataState">
                Hello, {{ authStore.loginDataState.username }}
            </span>
            <router-link v-if="!authStore.isAuthenticated" to="/login"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Login</router-link>
            <button v-else @click="handleLogout"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1">Logout</button>
        </div>
    </nav>
</template>

<script setup>
    import { useAuthStore } from '@/stores/authStore';
    import { onMounted, computed } from 'vue';
    import allRoutes from '@/data/allRoutesMenu.json';

    const authStore = useAuthStore();

    const xnor = (a, b) => !(a ^ b);

    const leftRoutes = allRoutes.filter(route => route.side === 'left');
    const rightRoutes = allRoutes.filter(route => route.side === 'right');

    const filteredLeftRoutes = computed(() => {
        return leftRoutes.filter(route => xnor(authStore.isAuthenticated, route.protected));
    });

    const handleLogout = () => {
        authStore.logout();
    };

    onMounted(() => {
        authStore.checkAuth(); // Ensure authentication status is checked on component mount
    });
</script>