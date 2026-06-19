/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // 🚀 Forces Next.js to build static HTML/CSS/JS pages
  images: {
    unoptimized: true, // Required for static exports
  },
};

module.exports = nextConfig;