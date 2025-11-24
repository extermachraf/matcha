import axios from "axios";

const api = axios.create({
  // Prefer env if set; otherwise use relative `/api` so Next proxy (if present)
  // is used and cookies remain same-origin during development.
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn(
        "API request failed with 401. Session may be expired. error: ",
        error
      );
    }
    return Promise.reject(error);
  }
);

export default api;
