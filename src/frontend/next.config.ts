/** @type {import('next').NextConfig} */
const nextConfig = {
  // In newer versions, 'turbo' is often a top-level key
  turbo: {
    root: '..',
  },
  // If the above still warns, try this specifically for the root issue:
  experimental: {
    // Some versions use this instead of the 'turbo' object for root issues
    outputFileTracingRoot: '../',
  }
};

export default nextConfig;