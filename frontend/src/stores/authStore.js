// src/stores/auth.js
import { defineStore } from 'pinia';
import api from '@/core/apiClient';
import { router } from '@/router';
import authApi from '@/core/authService';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        isAuthenticated: false,
        userPath: '',
    }),
    actions: {
        async login(username, password) {
            try {
                await authApi.login(username, password)
                this.isAuthenticated = true;
                // const response = await api.post('/auth/login', {
                //     username,
                //     password,
                // });
                // const token = response.data.access_token;
                // localStorage.setItem('access_token', token);
                // this.isAuthenticated = true;
                // console.log('Login successful, token set:', token);
                // router.push({ name: 'home' });
            } catch (error) {
                console.error('Error during login:', error);
                throw error;
            }
        },
        logout() {
            localStorage.removeItem('access_token');
            this.isAuthenticated = false;
            console.log('Logged out, token removed');
            router.push({ name: 'home' });
        },
        async checkAuth() {
            const token = localStorage.getItem('access_token');
            console.log('Checking auth, token:', token);
            if (token) {
                try {
                    await api.get('/auth/checkauth');
                    this.isAuthenticated = true;
                    console.log('Auth check successful');
                } catch (error) {
                    this.isAuthenticated = false;
                    console.log('Auth check failed, redirecting to login');
                    // router.push({ name: 'login' });
                }
            } else {
                this.isAuthenticated = false;
                console.log('No token found, redirecting to login');
                // router.push({ name: 'login' });
            }
        },
    },
});
