module.exports = {
    // 配置跨域请求
    devServer: {
        port: 80,
        host: 'localhost',
        open: true,
        https: false,
        proxy: {
            '/api': {
                target: 'http://localhost:5000/',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '/'
                }
            }
        }

    }

}
