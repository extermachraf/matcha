"use client";

import { UserStoreProvider } from "@/components/UserStoreProvider";

export function Providers({ children }: { children: React.ReactNode }) {
  return <UserStoreProvider>{children}</UserStoreProvider>;
}
