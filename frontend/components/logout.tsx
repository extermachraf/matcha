"use client";

import { useRouter } from "next/navigation";
import { useUserStore } from "@/lib/userStore";
import api from "@/lib/axiosInstance";
import { Button } from "@/components/ui/button";

export default function LogoutButton() {
  const router = useRouter();
  const clearUser = useUserStore((state) => state.clearUser);
  const handleLogout = async () => {
    try {
      await api.post("/auth/logout");
      clearUser();
      router.push("/login");
    } catch (error) {
      console.error("Error during logout:", error);
    } finally {
      clearUser();
      router.replace("/login");
    }
  };

  return (
    <Button variant="destructive" onClick={handleLogout}>
      Logout
    </Button>
  );
}
