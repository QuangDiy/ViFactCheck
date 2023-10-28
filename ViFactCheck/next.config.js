/** @type {import('next').NextConfig} */
const nextConfig = {
    async headers() {
      return [
        {
          source: "/api", 
          headers: [
            { 
              key: "Access-Control-Allow-Origin", 
              value: "*"  
            }
          ]
        }
      ]
    },
    // async redirects() {
    //   return [
    //     {
    //       source: '/api/:path*', 
    //       destination: '/api/:path*',
    //       permanent: false
    //     },
    //   ]
    // },
    webpack: (config, { isServer }) => {
        config.module.rules.push({
            test: /\.html$/,
            loader: 'html-loader'
        })
        return config
    },
    // rewrites: async () => [
    //     {
    //       source: "/public/myfile.html",
    //       destination: "/pages/api/myfile.js",
    //     },
    // ],
  }
  
  module.exports = nextConfig