import axios from 'axios'
import * as appsettings from '../../appsettings.json'
import router from '../router/index'

const api = axios.create({
  baseURL: appsettings.baseUrl
})

api.interceptors.request.use((config) => {
  console.log(appsettings.baseURL)
  const accessToken = localStorage.getItem('access_token')
  if (accessToken) {
    config.headers.authorization = `Bearer ${accessToken}`
  }
  return config
})

api.interceptors.response.use((response) => response, (err) => {
  if (err.response.status === 401) {
    router.push({ path: '/login' })
  }
  return Promise.reject(err)
})

export default api
