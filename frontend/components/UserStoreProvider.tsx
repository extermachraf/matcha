"use client";
import { ReactNode, use, useEffect, useState } from "react";
import { useUserStore } from "@/lib/userStore";
import { fetchUser } from "@/lib/dataFetcher";
import { useRouter } from "next/navigation";

interface UserStoreProviderProps {
  children: ReactNode;
}

export function UserStoreProvider({ children }: UserStoreProviderProps) {
  const setUser = useUserStore((state) => state.setUser);
  const [isInitialized, setInitialized] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const hydrateSession = async () => {
      try {
        const user = await fetchUser();
        if (user) {
          setUser(user);
        } else {
          // middleware will handle redirect to login
          setUser(null);
          router.push("/login");
        }
      } catch (error) {
        console.error("Error hydrating session:", error);
        setUser(null);
      } finally {
        setInitialized(true);
      }
    };
    hydrateSession();
  }, [setUser]);

  if (!isInitialized) {
    return <div>Loading Application...</div>;
  }
  // const user = useUserStore((state) => state.user);
  return <>{children}</>;
}
