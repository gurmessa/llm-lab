// src/lib/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL:  'http://localhost:8083', //process.env.NEXT_PUBLIC_API_URL, // e.g. http://localhost:8000/api
  timeout: 10_000,
});
