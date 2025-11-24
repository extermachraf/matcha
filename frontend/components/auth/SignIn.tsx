"use client";

import React from "react";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldSeparator,
} from "../ui/field";
import { Button } from "../ui/button";
import { FcGoogle } from "react-icons/fc";
import { Input } from "../ui/input";
import api from "@/lib/axiosInstance";
import { useUserStore } from "@/lib/userStore";
import { User } from "@/lib/types";
import { useState } from "react";
import { useRouter } from "next/navigation";
const SignIn = ({
  setSwitchToSignIn,
}: {
  setSwitchToSignIn: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [Loading, setLoading] = useState(false);

  const router = useRouter();
  const setUser = useUserStore((state) => state.setUser);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });
      const user: User = response.data.user as User;
      setUser(user);
      router.push("/profile");
    } catch (err: any) {
      let errorMessage =
        "login failed. Please check your credentials and try again.";
      if (err.response && err.response.data && err.response.data.error) {
        setError(errorMessage);
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="p-6 md:p-8" onSubmit={handleSubmit}>
      <FieldGroup>
        <div className="text-lg font-semibold mb-4 text-center">SignIn</div>
        {error && (
          <div className="mb-4 text-sm text-red-600 text-center">{error}</div>
        )}
        <Field>
          {/* <FieldLabel htmlFor="email">Email</FieldLabel> */}
          <Input
            placeholder="email"
            id="email"
            type="email"
            required
            onChange={(e) => {
              setEmail(e.target.value);
            }}
          />
        </Field>
        <Field>
          <Field>
            {/* <FieldLabel htmlFor="password">Password</FieldLabel> */}
            <Input
              placeholder="password"
              id="password"
              type="password"
              required
              onChange={(e) => {
                setPassword(e.target.value);
              }}
            />
          </Field>
        </Field>
        <Field>
          <Button className="cursor-pointer" type="submit" disabled={Loading}>
            {Loading ? "Signing In..." : "Sign In"}
          </Button>
        </Field>
        <FieldSeparator className="*:data-[slot=field-separator-content]:bg-card">
          Or continue with
        </FieldSeparator>
        <Button
          variant="outline"
          type="button"
          className="flex items-center justify-center cursor-pointer"
        >
          <FcGoogle className="size-5" />
        </Button>
        <FieldDescription className="text-center">
          Don't have an account?{" "}
          <button
            className="hover:text-primary cursor-pointer"
            type="button"
            onClick={() => setSwitchToSignIn(false)}
          >
            Sign up
          </button>
        </FieldDescription>
      </FieldGroup>
    </form>
  );
};

export default SignIn;
