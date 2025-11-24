import React from "react";

const ConfirmationPage = () => {
  return (
    // 1. Full screen container to center the card
    <div className="flex min-h-screen items-center justify-center p-4 sm:p-6 bg-background">
      {/* 2. The main card container */}
      <div className="w-full max-w-lg space-y-6 rounded-lg border border-border bg-card p-8 text-center shadow-lg">
        {/* Main Heading/Icon (Using Primary Color) */}
        <h1 className="text-2xl font-bold tracking-tight text-primary sm:text-3xl">
          Confirmation Email Sent Successfully
        </h1>

        {/* Core Instructions (Using Foreground Color) */}
        <p className="text-lg text-foreground">
          We have successfully processed your registration.
        </p>

        {/* Specific Action (Using Muted Foreground for subtlety) */}
        <p className="text-base text-muted-foreground">
          Please **check your inbox** (and spam folder) for a verification
          email. Click the link inside the email to finalize your account setup.
        </p>
      </div>
    </div>
  );
};

export default ConfirmationPage;
