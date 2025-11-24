/**
 * Next.js config: proxy API requests to backend to avoid cross-origin cookie issues
 * This makes the frontend server act as a same-origin proxy for `/api/*` requests.
 */
/** @type {import('next').NextConfig} */
module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:5000/api/:path*",
      },
    ];
  },
};
