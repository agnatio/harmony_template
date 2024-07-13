// src/stores/auth.js
import { defineStore } from 'pinia';
import api from '@/core/apiClient';
import { router } from '@/router';
import authService from '@/core/authService';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        isAuthenticated: false,
        user: null, // Track user information
    }),
    actions: {
        async login(username, password) {
            try {
                const { token, username: logged_user } = await authService.login(username, password);
                this.isAuthenticated = true;
                this.user = { username: logged_user }; // Store the username in the user state
                console.log('User logged in:', this.user);
            } catch (error) {
                console.error('Error during login:', error);
                throw error;
            }
        },
        logout() {
            localStorage.removeItem('access_token');
            this.isAuthenticated = false;
            this.user = null;
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
                    this.user = { username: 'username_from_token' }; // Set user information from token payload if necessary
                    console.log('Auth check successful');
                } catch (error) {
                    this.isAuthenticated = false;
                    this.user = null;
                    console.log('Auth check failed, redirecting to login');
                }
            } else {
                this.isAuthenticated = false;
                this.user = null;
                console.log('No token found, redirecting to login');
            }
        },
    },
});
