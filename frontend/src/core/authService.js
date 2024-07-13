import api from './apiClient';

const authApi = {
  async login(username, password) {
    let username_back = ''
    try {
      const response = await api.post('/auth/login', {
        username,
        password,
      });
      const resp_data = response.data;
      console.log("resp_data: ", resp_data)
      const token = response.data.access_token;
      localStorage.setItem('access_token', token); // Store the token in localStorage
      console.log('access_token', token);
      return token; // Return the token for further processing if needed
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  },

  async checkAuth() {
    const accessToken = localStorage.getItem('access_token');
    console.log('checkAuth function returned: ', accessToken)
    if (!accessToken) {
      return false;
    }

    try {
      await api.get('/auth/checkauth');
      return true;
    } catch (error) {
      localStorage.removeItem('access_token');
      return false;
    }
  },

  logout() {
    localStorage.removeItem('access_token');
  }
}

export default authApi;
