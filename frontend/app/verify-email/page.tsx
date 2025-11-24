"use client";
// Use 'use client' since 'useSearchParams' is a client-side hook

import React, { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/lib/axiosInstance";
import { useRouter } from "next/navigation";

// Define the API endpoint structure

const VerifyEmailPage = () => {
  // 1. Hook to access URL search parameters
  const searchParams = useSearchParams();
  const token = searchParams.get("token"); // This extracts the token value
  const router = useRouter();

  // State to manage the UI response
  const [status, setStatus] = useState<"loading" | "success" | "error">(
    "loading"
  );
  const [message, setMessage] = useState("Verifying your email...");

  // 2. useEffect to trigger the API call only once when the component mounts
  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Verification link is missing or invalid.");
      return;
    }

    // Function to handle the token verification
    const verifyToken = async () => {
      try {
        // Make the GET request to the backend (using axios instance)
        const response = await api.get(`/auth/verify-email?token=${token}`);

        // axios throws on non-2xx responses, so if we reach here it's a success
        setStatus("success");
        setMessage("Email successfully verified! You can now log in.");
        router.push("/complete-account-informations");
      } catch (err: any) {
        // Handle API errors (e.g., token expired, token invalid) and network errors
        const errorMessage =
          err?.response?.data?.message ||
          "Verification failed. The link may be expired or invalid.";
        setStatus("error");
        setMessage(errorMessage);
      }
    };

    verifyToken();
  }, [token]); // Dependency array includes 'token' to ensure the effect runs if it becomes available

  // --- Render based on status (Applying your Tailwind CSS styles) ---

  const getStyle = (currentStatus: "loading" | "success" | "error") => {
    switch (currentStatus) {
      case "success":
        // Primary color for success
        return "text-primary border-primary shadow-lg";
      case "error":
        // Destructive color for error (using your defined destructive variable)
        return "text-destructive border-destructive shadow-lg";
      case "loading":
      default:
        // Muted or Secondary for loading/neutral state
        return "text-secondary border-secondary shadow-md animate-pulse";
    }
  };

  const cardClasses = getStyle(status);

  return (
    <div className="flex min-h-screen items-center justify-center p-4 bg-background">
      <div
        className={`w-full max-w-lg space-y-6 rounded-lg border bg-card p-8 text-center ${cardClasses}`}
      >
        <h1 className="text-3xl font-bold tracking-tight">
          {status === "loading"
            ? "⏳ Processing..."
            : status === "success"
            ? "✅ Success!"
            : "❌ Error!"}
        </h1>
        <p className="text-lg text-foreground">{message}</p>

        {/* Optional: Show token for debugging */}
        {/* <p className="text-sm text-muted-foreground break-all">Token: {token || 'N/A'}</p> */}
      </div>
    </div>
  );
};

export default VerifyEmailPage;
