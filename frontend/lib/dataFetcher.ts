import api from "./axiosInstance";
import { User } from "./types";
import { isAxiosError } from "axios";

export const fetchUser = async (): Promise<User | null> => {
  try {
    const response = await api.get("/auth/me");
    if (response.data && response.data.user) {
      return response.data.user as User;
    }
  } catch (error) {
    if (isAxiosError(error) && error.response?.status === 401) {
      return null;
    }
    console.error("Error fetching user durring session check:", error);

    return null;
  }

  return null;
};
