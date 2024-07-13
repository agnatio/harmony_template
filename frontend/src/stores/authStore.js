// src/stores/authStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { router } from '@/router';
import authService from '@/core/authService';

export const useAuthStore = defineStore('auth', () => {
    const isAuthenticated = ref(false);
    const loginDataState = ref(null);

    const login = async (username, password) => {
        try {
            const loginData = await authService.login(username, password);
            loginDataState.value = loginData;
            isAuthenticated.value = true;
            console.log('User logged in:', loginDataState.value);

            // Store the entire login_data object in localStorage
            localStorage.setItem('login_data', JSON.stringify(loginData));
        } catch (error) {
            console.error('Error during login:', error);
            throw error;
        }
    };

    const logout = () => {
        authService.logout();
        isAuthenticated.value = false;
        loginDataState.value = null;
        localStorage.removeItem('login_data'); // Remove login_data from localStorage
        console.log('Logged out, token and user removed');
        router.push({ name: 'home' });
    };

    const checkAuth = async () => {
        const storedLoginData = JSON.parse(localStorage.getItem('login_data'));
        if (storedLoginData && storedLoginData.access_token) {
            try {
                const isAuthValid = await authService.checkAuth();
                isAuthenticated.value = isAuthValid;
                if (isAuthValid) {
                    loginDataState.value = storedLoginData;
                    console.log('Auth check successful', loginDataState.value);
                } else {
                    loginDataState.value = null;
                    console.log('Auth check failed, redirecting to login');
                }
            } catch (error) {
                isAuthenticated.value = false;
                loginDataState.value = null;
                console.log('Auth check failed, redirecting to login');
            }
        } else {
            isAuthenticated.value = false;
            loginDataState.value = null;
            console.log('No token found, redirecting to login');
        }
    };

    return {
        isAuthenticated,
        loginDataState,
        login,
        logout,
        checkAuth,
    };
});
