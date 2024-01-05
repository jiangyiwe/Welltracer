import { createApp } from 'vue'
//import Vue from 'vue'
import App from './App.vue'

import router from './router'


import VueCookies from 'vue-cookies'

//$cookies.set("key", "value");




import './assets/main.css'

const app = createApp(App)

app.use(router)

app.mount('#app')

