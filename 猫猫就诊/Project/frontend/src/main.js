// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.config.productionTip = false;

app.use(router)
app.use(ElementPlus) // 全局注册 Element Plus 组件
app.mount('#app')
