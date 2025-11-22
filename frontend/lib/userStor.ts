import { create } from "zustand";
import { User } from "./types";

interface UserStore {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) => set(() => ({ user, isAuthenticated: !!user })),
  clearUser: () => set(() => ({ user: null, isAuthenticated: false })),
}));
