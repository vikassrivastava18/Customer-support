import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import router from './router'

import './assets/main.css'

import store from './store'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App)
    .use(router)
    .use(store)
    .mount('#app')
