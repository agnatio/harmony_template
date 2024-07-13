/**
 * This module provides authentication-related functionalities, encapsulating API calls 
 * and handling authentication state within the application.
 * 
 * Key functionalities:
 * 
 * 1. **Login**: Sends a POST request to the login endpoint with the provided username 
 *    and password. If successful, stores the received access token in local storage 
 *    and returns the token.
 * 
 * 2. **Check Authentication**: Checks if an access token is present in local storage.
 *    Sends a GET request to verify the token's validity. If the token is invalid or 
 *    the request fails, it removes the token from local storage and returns false.
 * 
 * 3. **Logout**: Removes the access token from local storage, effectively logging the user out.
 * 
 * The module ensures that authentication logic is centralized and consistently applied 
 * across the application, enhancing security and maintainability.
 */


import apiClient from './apiClient';

const authService = {
  async login(username, password) {
    try {
      const response = await apiClient.post('/auth/login', {
        username,
        password,
      });
      const resp_data = response.data;
      console.log("resp_data: ", resp_data)
      const token = response.data.access_token;
      const logged_user = response.data.username;
      localStorage.setItem('access_token', token); // Store the token in localStorage
      console.log('access_token: ', token);
      console.log('logged_user: ', logged_user);
      return { token, username: logged_user }; // Return the token for further processing if needed
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
      await apiClient.get('/auth/checkauth');
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

export default authService;
