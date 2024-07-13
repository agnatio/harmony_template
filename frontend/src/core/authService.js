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

// src/core/authService.js
import apiClient from './apiClient';

const authService = {
  async login(username, password) {
    try {
      const response = await apiClient.post('/auth/login', {
        username,
        password,
      });
      const loginData = response.data;
      console.log("response.data: ", loginData);
      return loginData; // Return the login data object
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  },

  async checkAuth() {
    const accessToken = JSON.parse(localStorage.getItem('login_data'))?.access_token;
    if (!accessToken) {
      return false;
    }

    try {
      await apiClient.get('/auth/checkauth');
      return true;
    } catch (error) {
      localStorage.removeItem('login_data');
      return false;
    }
  },

  logout() {
    localStorage.removeItem('login_data');
  }
};

export default authService;



// const authService = {
//   async login(username, password) {
//     try {
//       const response = await apiClient.post('/auth/login', {
//         username,
//         password,
//       });
//       const token = response.data.access_token;
//       const logged_user = response.data.username;
//       const login_data = response.data;
//       console.log("response.data: ", response.data)
//       console.log("1: ", login_data.access_token)
//       console.log("2: ", login_data.token_type)
//       console.log("3: ", login_data.username)
//       localStorage.setItem('access_token', token); // Store the token in localStorage
//       localStorage.setItem('logged_user', logged_user); // Store the username in localStorage
//       return { token, username: logged_user }; // Return the token and username for further processing if needed
//     } catch (error) {
//       console.error('Error during login:', error);
//       throw error;
//     }
//   },

//   async checkAuth() {
//     const accessToken = localStorage.getItem('access_token');
//     if (!accessToken) {
//       return false;
//     }

//     try {
//       await apiClient.get('/auth/checkauth');
//       return true;
//     } catch (error) {
//       localStorage.removeItem('access_token');
//       localStorage.removeItem('logged_user');
//       return false;
//     }
//   },

//   logout() {
//     localStorage.removeItem('access_token');
//     localStorage.removeItem('logged_user');
//   }
// };

// export default authService;
