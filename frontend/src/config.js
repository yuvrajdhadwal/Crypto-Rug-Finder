let baseURL;
if (import.meta.env) {
    const isDevelopment = import.meta.env.MODE === 'development';
    baseURL = isDevelopment ? import.meta.env.VITE_API_BASE_URL_LOCAL : import.meta.env.VITE_API_BASE_URL_PROD;
}

const config = {
    baseURL: baseURL ?? 'http://localhost:8000'
};

export default config;