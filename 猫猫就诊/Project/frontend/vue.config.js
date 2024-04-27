const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 输出目录
  assetsDir: 'static',
  // 基本路径
  // baseUrl: './',
  proxyTable: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
      pathRewrite: {
        '/api': '/api'
      }
    }
  }
})