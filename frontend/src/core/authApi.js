import api from './api';
import router from '../router/index';

const authApi = {
  async login(username, password) {
    const response = await api.post('/auth/login', {
      username,
      password,
    });

    const token = response.data.access_token;
    localStorage.setItem('access_token', token);
    router.push({ name: 'home' });
  },

  async checkAuth() {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      router.push({ name: 'login' });
      return false;
    }

    try {
      await api.get('/auth/checkauth');
      return true;
    } catch (error) {
      localStorage.removeItem('access_token');
      router.push({ name: 'login' });
      return false;
    }
  }
};

export default authApi;
