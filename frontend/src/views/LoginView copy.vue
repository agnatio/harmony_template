<!-- src/views/LoginView.vue -->
<template>
    <main class="flex items-center justify-center h-[calc(100vh-4rem)] bg-gray-50">
        <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
            <h1 class="text-4xl font-bold text-gray-900 mb-4 text-center">Login</h1>
            <p class="text-lg text-gray-600 mb-6 text-center">Welcome to the Login page</p>
            <form @submit.prevent="handleLogin">
                <div class="mb-4">
                    <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Username</label>
                    <input type="text" id="username" v-model="username"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div class="mb-4">
                    <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password</label>
                    <input type="password" id="password" v-model="password"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div v-if="errorMessage" class="mb-4 text-red-500 text-sm">{{ errorMessage }}</div>
                <button type="submit"
                    class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-200">
                    Login
                </button>
            </form>
        </div>
    </main>
</template>


<script setup>
    import { ref } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';

    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const handleLogin = async () => {
        try {
            console.log(username.value);
            console.log(password.value);
            const response = await axios.post('http://localhost:8000/auth/login', {
                username: username.value,
                password: password.value,
            });

            console.log(response);

            // Correctly access the token from the response
            const token = response.data.access_token;

            // Save the token in local storage or any other storage
            localStorage.setItem('token', token);

            // Redirect to the home page
            router.push({ name: 'home' });
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
