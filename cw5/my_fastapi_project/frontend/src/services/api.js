import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    return Promise.reject(error);
  }
);

export const itemsAPI = {
  getAll: (skip = 0, limit = 100, title = "") =>
    apiClient.get(`/items/?skip=${skip}&limit=${limit}&title=${title}`),
  getById: (id) => apiClient.get(`/items/${id}`),
  create: (data) => apiClient.post("/items/", data),
  update: (id, data) => apiClient.put(`/items/${id}`, data),
  delete: (id) => apiClient.delete(`/items/${id}`),
  analyze: (id) => apiClient.post(`/items/${id}/analyze`),
  suggestImprovements: (id) => apiClient.post(`/items/${id}/suggest-improvements`),
};

export const chatGPTAPI = {
  chat: (messages, temperature = 0.7, max_tokens = 1000) =>
    apiClient.post("/chatgpt/chat", { messages, temperature, max_tokens }),
  analyzeDescription: (description) =>
    apiClient.post("/chatgpt/analyze-item", { description }),
  generateTitles: (description) =>
    apiClient.post("/chatgpt/generate-titles", { description }),
  health: () => apiClient.get("/chatgpt/health"),
};

export const healthAPI = {
  check: () => apiClient.get("/health"),
};

export default apiClient;
