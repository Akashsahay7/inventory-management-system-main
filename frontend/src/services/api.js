import axios from "axios";

const api = axios.create({
  baseURL: "https://inventory-management-system-production-a0d7.up.railway.app",
});

export default api;