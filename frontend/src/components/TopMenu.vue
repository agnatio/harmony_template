<template>
    <nav class="flex justify-between items-center border border-sky-600 text-sm bg-sky-200 px-10">
        <div class="flex items-center gap-4">
            <router-link to="/" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Home</router-link>
            <router-link to="/about" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">About</router-link>
            <router-link to="/register" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Register</router-link>
            <router-link to="/dummyprotected" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Protected</router-link>
        </div>
        <div class="flex items-center gap-8">
            <router-link v-if="!isAuthenticated" to="/login"
                class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Login</router-link>
            <button v-else @click="handleLogout"
                class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1">Logout</button>
        </div>
    </nav>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import authApi from '@/core/authApi';

    const isAuthenticated = ref(false);

    const checkAuthStatus = async () => {
        isAuthenticated.value = await authApi.checkAuth();
    };

    const handleLogout = () => {
        authApi.logout();
        isAuthenticated.value = false;
    };

    onMounted(() => {
        checkAuthStatus();
    });
</script>