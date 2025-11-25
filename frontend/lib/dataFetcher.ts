import api from "./axiosInstance";
import { User } from "./types";
import { isAxiosError } from "axios";
import { useRouter } from "next/router";

export const fetchUser = async (): Promise<User | null> => {
  console.log("Fetching user durring session check...");
  try {
    const response = await api.get("/auth/me");
    if (response.data && response.data.user) {
      return response.data.user as User;
    }
  } catch (error) {
    if (isAxiosError(error) && error.response?.status === 401) {
      // deleat token from cookies if exists
      return null;
    }
    console.error("Error fetching user durring session check:", error);

    return null;
  }

  return null;
};

export const fetchUserTags = async (userId: number): Promise<any> => {
  try {
    const response = await api.get(`/tags/user-tags/${userId}`);
    if (response.data && response.data.tags) {
      return response.data.tags as string[];
    }
  } catch (error) {
    console.error("Error fetching user tags:", error);
    return null;
  }
};
