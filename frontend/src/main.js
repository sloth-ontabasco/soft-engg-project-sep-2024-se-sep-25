import './assets/main.css'
import 'primeicons/primeicons.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'

import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8081'

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8081'

});


const app = createApp(App)
router.app = app
app.config.globalProperties.$axios = axiosInstance

app.use(store)
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
})
app.mount('#app')

