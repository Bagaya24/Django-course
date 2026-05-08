import axios from "axios";
import { ACCESS_TOKEN } from "@/utils/constant";

const urlBase = process.env.NEXT_PUBLIC_API_URL

const api = axios.create({
    baseURL: urlBase,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
    }
});

const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop()?.split(";").shift() || null;
    }
    return null;
};

api.interceptors.request.use(
    (config) => {
        const token = getCookie(ACCESS_TOKEN);
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
)
export default api;