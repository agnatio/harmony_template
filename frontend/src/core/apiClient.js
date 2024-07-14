import axios from 'axios';
import * as appsettings from '../../appsettings.json';
import { router } from '../router/index';

const apiClient = axios.create({
  baseURL: appsettings.baseUrl
});

apiClient.interceptors.request.use((config) => {
  const storedLoginData = localStorage.getItem('login_data');
  if (storedLoginData) {
    const parsedLoginData = JSON.parse(storedLoginData);
    const accessToken = parsedLoginData.access_token;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (err) => {
    if (err.response.status === 401) {
      router.push({ path: '/' }); // Redirect to login page on 401 Unauthorized
    }
    return Promise.reject(err);
  }
);

export default apiClient;
