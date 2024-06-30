<!-- src/views/LoginView.vue -->
<template>
    <main class="flex items-center justify-center h-[calc(100vh-2rem)] bg-gray-500">
        <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
            <h1>Login</h1>
            <p>Welcome to the Login page</p>
            <form @submit.prevent="handleLogin">
                <div>
                    <label for="username">Username</label>
                    <input type="text" id="username" v-model="username" required />
                </div>
                <div>
                    <label for="password">Password</label>
                    <input type="password" id="password" v-model="password" required />
                </div>
                <div v-if="errorMessage">{{ errorMessage }}</div>
                <button type="submit">Login</button>
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
