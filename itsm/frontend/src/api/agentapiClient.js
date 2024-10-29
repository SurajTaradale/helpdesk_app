import axios from 'axios';
import Cookies from 'js-cookie';
const agentapiClient = axios.create({
  baseURL: 'http://192.168.1.8:8001', // Update with your base URL
});

agentapiClient.interceptors.request.use((config) => {
  const token = Cookies.get('agent_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default agentapiClient;
