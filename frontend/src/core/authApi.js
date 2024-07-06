import api from './api'
import router from '../router/index'

const authApi = {

  async login(userName, password) {
    const response = await api.post('/auth/login', {
      userName,
      password,
    });

    // Correctly access the token from the response
    const token = response.data.access_token;

    // Save the token in local storage or any other storage
    localStorage.setItem('access_token', token);

    // Redirect to the home page
    router.push({ name: 'home' });
  },

  async checkAuth() {
    console.log('401')
    router.push({ name: 'login' });
    //await api.get('/auth/checkauth')
  }
}

export default authApi;