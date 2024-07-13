/**
 * This module configures and exports an Axios instance for making HTTP requests
 * with a base URL and interceptors for request and response handling.
 * 
 * Key functionalities:
 * 
 * 1. **Base URL Configuration**: Sets the base URL for all HTTP requests using the configuration
 *    from the `appsettings.json` file.
 * 
 * 2. **Request Interceptor**: Attaches an authorization header with a bearer token from 
 *    local storage to every outgoing request if the token is available.
 * 
 * 3. **Response Interceptor**: Handles responses globally, specifically:
 *    - Logs error response statuses for debugging purposes.
 *    - Redirects to the login page if a 401 Unauthorized status is encountered.
 * 
 * The module ensures secure communication by attaching tokens to requests and handling
 * authentication errors consistently across the application.
 */



import axios from 'axios'
import * as appsettings from '../../appsettings.json'
import { router } from '../router/index'

const apiClient = axios.create({
  baseURL: appsettings.baseUrl
})

apiClient.interceptors.request.use((config) => {
  console.log("Base URL:", appsettings.baseUrl); // Debug the base URL
  const accessToken = localStorage.getItem('access_token')
  console.log("Access token from localStorage:", accessToken); // Debug the token
  if (accessToken) {
    config.headers.authorization = `Bearer ${accessToken}`
    console.log("Authorization header set:", config.headers.authorization); // Confirm the header is set
  }
  return config
})

apiClient.interceptors.response.use((response) => response, (err) => {
  console.log("Error response status:", err.response.status); // Debug the error status
  if (err.response.status === 401) {
    console.log("Unauthorized error, redirecting to login"); // Confirm redirection
    router.push({ path: '/' })
  }
  return Promise.reject(err)
})

export default apiClient
