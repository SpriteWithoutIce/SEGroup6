module.exports = {
    // 配置跨域请求
    devServer: {
        port: 80,
        host: '127.0.0.1',
        open: true,
        https: false,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5000/',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '/'
                }
            }
        }

    }

}
