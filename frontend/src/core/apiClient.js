import axios from 'axios'
import * as appsettings from '../../appsettings.json'
import { router } from '../router/index'

const api = axios.create({
  baseURL: appsettings.baseUrl
})

api.interceptors.request.use((config) => {
  console.log("Base URL:", appsettings.baseUrl); // Debug the base URL
  const accessToken = localStorage.getItem('access_token')
  console.log("Access token from localStorage:", accessToken); // Debug the token
  if (accessToken) {
    config.headers.authorization = `Bearer ${accessToken}`
    console.log("Authorization header set:", config.headers.authorization); // Confirm the header is set
  }
  return config
})

api.interceptors.response.use((response) => response, (err) => {
  console.log("Error response status:", err.response.status); // Debug the error status
  if (err.response.status === 401) {
    console.log("Unauthorized error, redirecting to login"); // Confirm redirection
    router.push({ path: '/' })
  }
  return Promise.reject(err)
})

export default api
