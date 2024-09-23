import axios from 'axios';
import Cookies from 'js-cookie';

const apiClient = axios.create({
  baseURL: 'http://192.168.1.8:8001', // Update with your base URL
});

apiClient.interceptors.request.use((config) => {
  const token = Cookies.get('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginApi = async (username, password) => {
  const response = await apiClient.post(
    '/auth/token',
    new URLSearchParams({ username, password })
  );
  Cookies.set('token', response.data.access_token);
  return response.data;
};

export default apiClient;
