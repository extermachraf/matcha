// src/hooks/useAuth.ts
"use client";
import { useUserStore } from "@/lib/userStore";
import { shallow } from "zustand/shallow";
import { User } from "@/lib/types"; // Import your User interface
import api from "@/lib/axiosInstance";

interface AuthStatus {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isProfileComplete: boolean;
}

/**
 * Checks if a user object contains all required profile information.
 * @param user The user object from the global store.
 * @returns boolean
 */
const checkProfileCompletion = (user: User | null): boolean => {
  if (!user) return false;

  // Define the required fields based on your User interface
  const requiredFields: (keyof User)[] = [
    "biography",
    "birthdate",
    "gender",
    "sexualPreferences",
    "profilePictureId",
  ];

  // 1. Check for basic required fields (string/number values)
  const isBasicDataComplete = requiredFields.every((field) => {
    const value = user[field];
    return value !== null && value !== undefined && value !== "";
  });

  // 2. Check for the profile picture (requires profilePictureId to be a number, not null)
  const hasProfilePicture = user.profilePictureId !== null;
  // Return true only if both data and picture are present
  return isBasicDataComplete && hasProfilePicture;
};

export const useAuth = (): AuthStatus => {
  // Use a selector to pull necessary state from Zustand
  // Select primitives separately to avoid returning a new object each render
  // (this prevents unnecessary re-renders and infinite loops).
  const user = useUserStore((state) => state.user);
  const isAuthenticated = useUserStore((state) => state.isAuthenticated);

  // 📌 We can't easily track `isLoading` here without modifying the store to expose it.
  // For now, we assume `isAuthenticated` being true means the session check in the Provider is done.
  const isLoading = false; // Simplified assumption for this task

  const isProfileComplete = checkProfileCompletion(user);

  return {
    user,
    isAuthenticated,
    isLoading,
    isProfileComplete,
  };
};
