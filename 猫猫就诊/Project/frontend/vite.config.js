import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // VueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  transpileDependencies: true,
  devServer : {
    proxy: {
      '/api/user_service': {
        target: 'http://127.0.0.1:5004',
        changeOrigin: true,
        pathRewrite: { '^/api/user_service': '' }
      },
      '/api/patient_service': {
      target: 'http://127.0.0.1:5001',
      changeOrigin: true,
      pathRewrite: { '^/api/patient_service': '' }
      },
      '/api/doctor_service': {
        target: 'http://127.0.0.1:5002',
        changeOrigin: true,
        pathRewrite: { '^/api/doctor_service': '' }
      },
      '/api/administrator_service': {
        target: 'http://127.0.0.1:5003',
        changeOrigin: true,
        pathRewrite: { '^/api/administrator_service': '' }
      }
    }
  },
  // 修改打包配置，实现静态资源分类打包和分拆打包
  build: {
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        chunkFileNames: 'static/js/[name]-[hash].js',
        entryFileNames: 'static/js/[name]-[hash].js',
        assetFileNames: 'static/[ext]/[name]-[hash].[ext]',
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString();
          }
        }
      }
    }
  }
})
