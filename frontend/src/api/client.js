import axios from 'axios';

const client = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Django 后端地址
  timeout: 10000,
  withCredentials: true, // 允许携带 Cookie (Session ID)
});

// 响应拦截器：处理错误
client.interceptors.response.use(
  response => response.data,
  error => {
    console.error("API Error:", error);
    return Promise.reject(error);
  }
);

export default client;