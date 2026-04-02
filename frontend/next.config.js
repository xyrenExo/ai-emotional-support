/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  images: {
    domains: ["localhost"],
  },
  async rewrites() {
    // Get the API base URL and ensure it doesn't include /api twice
    let apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

    // Remove trailing /api if it exists
    if (apiUrl.endsWith("/api")) {
      apiUrl = apiUrl.slice(0, -4);
    }

    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
