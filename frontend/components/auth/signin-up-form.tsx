"use client";
import { cn } from "@/lib/utils";
import * as React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { useState } from "react";
import SignUp from "./SignUp";
import SignIn from "./SignIn";

export function SignupForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const [switchToSignIn, setSwitchToSignIn] = useState(true);

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0 md:grid-cols-2">
          {switchToSignIn ? (
            <SignIn setSwitchToSignIn={setSwitchToSignIn} />
          ) : (
            <SignUp setSwitchToSignIn={setSwitchToSignIn} />
          )}
          <div className="bg-muted relative hidden md:block">
            <img
              src="/signInUp.png"
              alt="Image"
              className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
