import axios from "axios";

const api = axios.create({
  baseURL: "https://inventory-management-system-main-production.up.railway.app",
});

export default api;
