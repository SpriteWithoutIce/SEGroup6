// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import CryptoJS from 'crypto-js'
import VueCookies from 'vue-cookies';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.config.globalProperties.$axios = axios
app.provide('$identity_num', '0')
app.config.productionTip = false;

app.use(router)
app.use(ElementPlus) // 全局注册 Element Plus 组件
app.use(CryptoJS)
app.mount('#app')
