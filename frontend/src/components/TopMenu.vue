<template>
    <nav class="flex justify-between items-center border border-sky-600 text-sm bg-sky-200 px-10">
        <div class="flex items-center gap-4">
            <router-link to="/" class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Home</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/about"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">About</router-link>
            <router-link v-if="!authStore.isAuthenticated" to="/register"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Register</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/dummyprotected"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Protected</router-link>
        </div>
        <div class="flex items-center gap-8">
            <span v-if="authStore.isAuthenticated && authStore.loginDataState">Hello, {{
                authStore.loginDataState.username }}</span>
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
    import { onMounted } from 'vue';

    const authStore = useAuthStore();

    const handleLogout = () => {
        authStore.logout();
    };

    onMounted(() => {
        authStore.checkAuth(); // Ensure authentication status is checked on component mount
    });
</script>
