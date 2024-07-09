// src/stores/auth.js
import { defineStore } from 'pinia';
import api from '@/core/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        isAuthenticated: false,
    }),
    actions: {
        async login(username, password) {
            try {
                const response = await api.post('/auth/login', {
                    username,
                    password,
                });
                const token = response.data.access_token;
                localStorage.setItem('access_token', token);
                this.isAuthenticated = true;
                console.log('Login successful, token set:', token);
                router.push({ name: 'home' });
            } catch (error) {
                console.error('Error during login:', error);
                throw error;
            }
        },
        logout() {
            localStorage.removeItem('access_token');
            this.isAuthenticated = false;
            console.log('Logged out, token removed');
            router.push({ name: 'login' });
        },
        async checkAuth() {
            const token = localStorage.getItem('access_token');
            console.log('Checking auth, token:', token);
            if (token) {
                try {
                    await api.get('/auth/checkauth'); // Assuming this endpoint verifies the token
                    this.isAuthenticated = true;
                    console.log('Auth check successful');
                } catch {
                    this.isAuthenticated = false;
                    console.log('Auth check failed, redirecting to login');
                    router.push({ name: 'login' });
                }
            } else {
                this.isAuthenticated = false;
                console.log('No token found, redirecting to login');
                router.push({ name: 'login' });
            }
        },
    },
});
