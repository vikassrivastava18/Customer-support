import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import router from './router'

import './assets/main.css'

import store from './store'
import { createApp } from 'vue'
import App from './App.vue'

let app = createApp(App)
            .use(router)
            .use(store)

app.config.globalProperties.$axios = axios
app.mount('#app')


// Request interceptor
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('Authentication-Token')
  if (token) {
    config.headers['Content-Type'] = 'application/json';
    config.headers.Authorization = `Token ${token}`
  }
  return config
})
