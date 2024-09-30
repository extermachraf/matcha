/** @type {import('next').NextConfig} */
const nextConfig = {
    webpack(config) {
      config.module.rules.push({
        test: /\.svg$/, // Add this rule for SVG
        use: ['@svgr/webpack'], // Use @svgr/webpack to handle SVGs as React components
      });
  
      return config;
    },
  };
  
  export default nextConfig;
