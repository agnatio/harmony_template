<template>
    <main class="flex items-center justify-center h-[calc(100vh-1.8rem)] bg-gray-500">
        <div class="w-full max-w-sm bg-gray-200 p-4 border-2 border-gray-600 rounded-lg shadow-lg">
            <h1 class="text-2xl font-bold text-gray-900 mb-1 text-center">Login</h1>
            <form @submit.prevent="handleLogin" class="space-y-3">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 py-2">Username</label>
                    <input type="text" id="username" v-model="username"
                        class="w-full px-3 py-2 text-sm border bg-gray-100 border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 py-2">Password</label>
                    <input type="password" id="password" v-model="password"
                        class="w-full px-3 py-2 text-sm border bg-gray-100 border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</div>
                <button type="submit"
                    class="w-full bg-sky-500 text-white py-2 rounded-md hover:bg-sky-600 focus:outline-none focus:ring focus:ring-blue-200">
                    Login
                </button>
            </form>
            <p class="text-center text-gray-600 mt-2">
                Don't have an account? <router-link to="/register"
                    class="text-blue-500 hover:underline">Register</router-link>
            </p>
        </div>
    </main>
</template>


<script setup>
    import { ref } from 'vue';
    import authApi from '@/core/authService';
    import { useAuthStore } from '@/stores/authStore';
    import { router, accessSource } from '@/router/index';

    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');

    const authStore = useAuthStore();

    const handleLogin = async () => {
        try {
            authStore.login(username.value, password.value);
            if (accessSource.value) {
                router.push({ name: accessSource })
                accessSource.value = ''
            }
            else {
                router.push('/')
            }
        } catch (error) {
            console.error('Error during login:', error);

            if (error.response) {
                console.error('Response data:', error.response.data);
                console.error('Response status:', error.response.status);
                console.error('Response headers:', error.response.headers);
                errorMessage.value = `Login failed: ${error.response.data.detail || 'Please check your credentials and try again.'}`;
            } else if (error.request) {
                console.error('Request data:', error.request);
                errorMessage.value = 'Login failed: No response received from the server.';
            } else if (error.message.includes('No match for')) {
                // Handle routing errors specifically
                errorMessage.value = 'Login successful, but the specified route could not be found. Please check the route configuration.';
            } else {
                console.error('Error message:', error.message);
                errorMessage.value = `Login failed: ${error.message}`;
            }
        }
    };


</script>
