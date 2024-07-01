<template>
    <main class="flex items-center justify-center h-[calc(100vh-1.8rem)] bg-gray-500">
        <div class="w-full max-w-sm bg-gray-200 p-4 border-2 border-gray-600 rounded-lg shadow-lg">
            <h1 class="text-2xl font-bold text-gray-900 mb-1 text-center">Register</h1>
            <form @submit.prevent="handleRegister" class="space-y-3">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 py-2">Username</label>
                    <input type="text" id="username" v-model="username"
                        class="w-full px-3 py-2 text-sm border bg-gray-100 border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 py-2">Email</label>
                    <input type="email" id="email" v-model="email"
                        class="w-full px-3 py-2 text-sm border bg-gray-100 border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 py-2">Password</label>
                    <input type="password" id="password" v-model="password"
                        class="w-full px-3 py-2 text-sm border bg-gray-100 border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div>
                    <label for="passwordRepeat" class="block text-sm font-medium text-gray-700 py-2">Repeat
                        Password</label>
                    <input type="password" id="passwordRepeat" v-model="passwordRepeat"
                        class="w-full px-3 py-2 text-sm border bg-gray-100 border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-200"
                        required />
                </div>
                <div v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</div>
                <button type="submit"
                    class="w-full bg-sky-500 text-white py-2 rounded-md hover:bg-sky-600 focus:outline-none focus:ring focus:ring-blue-200">
                    Register
                </button>
            </form>
            <p class="text-center text-gray-600 mt-2">
                Already have an account? <router-link to="/login"
                    class="text-blue-500 hover:underline">Login</router-link>
            </p>
        </div>
    </main>
</template>

<script setup>
    import { ref } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';

    const username = ref('');
    const email = ref('');
    const password = ref('');
    const passwordRepeat = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const handleRegister = async () => {
        try {
            if (password.value !== passwordRepeat.value) {
                errorMessage.value = 'Passwords do not match.';
                return;
            }

            // Prepare the payload to be sent
            const payload = {
                username: username.value,
                email: email.value,
                password: password.value,
            };

            // Log the payload to console to see what is being sent
            console.log('Sending registration data:', payload);

            const response = await axios.post('http://localhost:8000/users/register', payload);

            // Assuming registration is successful and backend responds with some data
            console.log('Registration response:', response.data);

            // Redirect to login page or handle success as per your application flow
            router.push({ name: 'login' });
        } catch (error) {
            if (error.response) {
                errorMessage.value = `Registration failed: ${error.response.data.detail || 'Please check your credentials and try again.'}`;
            } else if (error.request) {
                errorMessage.value = 'Registration failed: No response received from the server.';
            } else {
                errorMessage.value = `Registration failed: ${error.message}`;
            }
        }
    };
</script>
