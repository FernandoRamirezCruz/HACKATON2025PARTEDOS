import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Asegúrate que coincide con tu backend
  timeout: 5000,
});

export default api;