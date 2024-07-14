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
        <div class="flex items-center gap-8 relative">
            <span v-if="authStore.isAuthenticated && authStore.loginDataState" @click="toggleSubmenu">
                Hello, {{ authStore.loginDataState.username }}
            </span>
            <router-link v-if="!authStore.isAuthenticated" to="/login"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Login</router-link>
            <button v-else @click="handleLogout"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1">Logout</button>
            <div v-if="showSubmenu" class="absolute right-0 top-full bg-white border border-sky-600 mt-2 p-2">
                <button @click="handleLogout"
                    class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300">Logout</button>
                <router-link to="/settings"
                    class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300">Settings</router-link>
                <router-link to="/user-details"
                    class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300">User Details</router-link>
            </div>
        </div>
    </nav>
</template>

<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import { onMounted } from 'vue';

    const authStore = useAuthStore();
    const showSubmenu = ref(false);

    const toggleSubmenu = () => {
        showSubmenu.value = !showSubmenu.value;
    };

    const handleLogout = () => {
        authStore.logout();
        showSubmenu.value = false;
    };

    onMounted(() => {
        authStore.checkAuth(); // Ensure authentication status is checked on component mount
    });
</script>

<style scoped>

    /* Add styles for the submenu */
    .submenu {
        position: absolute;
        right: 0;
        top: 100%;
        background-color: white;
        border: 1px solid #38bdf8;
        margin-top: 0.5rem;
        padding: 0.5rem;
        z-index: 10;
    }

    .submenu button,
    .submenu a {
        display: block;
        width: 100%;
        text-align: left;
        padding: 0.5rem 1rem;
        color: #4b5563;
        text-decoration: none;
    }

    .submenu button:hover,
    .submenu a:hover {
        background-color: #7dd3fc;
    }
</style>
