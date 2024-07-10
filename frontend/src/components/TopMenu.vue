<template>
    <nav class="flex justify-between items-center border border-sky-600 text-sm bg-sky-200 px-10">
        <div class="flex items-center gap-4">
            <router-link to="/" class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Home</router-link>
            <router-link to="/about" class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">About</router-link>
            <router-link v-if="!authStore.isAuthenticated" to="/register"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Register</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/dummyprotected"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Protected</router-link>
        </div>
        <div class="flex items-center gap-8">
            <router-link v-if="!authStore.isAuthenticated" to="/login"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Login</router-link>
            <button v-else @click="handleLogout"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1">Logout</button>
        </div>
    </nav>
</template>

<script setup>
    import { useAuthStore } from '@/stores/auth';
    import { onMounted } from 'vue';

    const authStore = useAuthStore();

    const handleLogout = () => {
        authStore.logout();
    };

    const handleLogin = async () => {
        try {
            const token = await authStore.login('username', 'password'); // Replace with actual login credentials
            console.log('Login successful, token:', token);
            // Optionally perform other actions after successful login (e.g., redirect)
        } catch (error) {
            console.error('Error during login:', error);
            // Handle login error (e.g., show error message)
        }
    };

    onMounted(() => {
        authStore.checkAuth(); // Ensure authentication status is checked on component mount
    });
</script>