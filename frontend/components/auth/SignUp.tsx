"use client";
import React, { useState } from "react";
import { isAxiosError } from "axios";

// Import UI components
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldSeparator,
} from "../ui/field";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { FcGoogle } from "react-icons/fc";

// Import utilities
import api from "@/lib/axiosInstance";
import { useRouter } from "next/navigation";

// Define the expected structure for uniqueness/validation errors from Flask
interface ErrorDetails {
  username?: string;
  email?: string;
  password?: string;
  [key: string]: string | undefined; // Allow other specific field errors
}

const SignUp = ({
  setSwitchToSignIn,
}: {
  setSwitchToSignIn: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirmPassword: "", // Matches the state key
  });

  const [statusMessage, setStatusMessage] = useState<string | null>(null); // 💡 FIX 1: Change type to handle structured error details object
  const [errorDetails, setErrorDetails] = useState<ErrorDetails | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    let key = id;

    // 💡 FIX 2: Handle the specific ID mapping for the confirm field
    // We map 'confirm-password' (from JSX) to 'confirmPassword' (in state)
    if (id === "confirm-password") {
      key = "confirmPassword";
    } else {
      // For all other fields like 'first_name', 'username', the key is the ID
      key = id;
    }

    setFormData({
      ...formData,
      [key]: value,
    });
  };

  const router = useRouter();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setStatusMessage(null);
    setErrorDetails(null);

    if (formData.password !== formData.confirmPassword) {
      setErrorDetails({ password: "Passwords do not match." });
      setStatusMessage("Validation failed.");
      setIsLoading(false);
      return;
    }

    try {
      // 💡 FIX 4: Corrected endpoint from "/api/auth/register" to "/auth/register"
      const response = await api.post("/auth/register", {
        username: formData.username,
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        password: formData.password,
      });

      setStatusMessage(
        response.data.message ||
          "Account created successfully! Please check your email for verification."
      );
      // 💡 FIX 3: route the user to confirm his email

      router.push("/confirm-email");
      // Clear form data for next use
      // setFormData({
      //   username: "",
      //   first_name: "",
      //   last_name: "",
      //   email: "",
      //   password: "",
      //   confirmPassword: "",
      // });
    } catch (err) {
      let message = "Registration failed. Please try again.";

      if (isAxiosError(err) && err.response) {
        const data = err.response.data;
        if (data.details) {
          // Store the structured error object
          setErrorDetails(data.details);
          message = data.error || message;
        } else {
          // General errors (e.g., 500)
          message = data.error || message;
        }
      }
      setStatusMessage(message);
    } finally {
      setIsLoading(false);
    }
  }; // Helper to check if any field-specific error exists

  const hasFieldErrors =
    errorDetails &&
    (errorDetails.username || errorDetails.email || errorDetails.password);

  return (
    <form onSubmit={handleSubmit} className="p-6 md:p-8">
      <FieldGroup>
        <div className="text-lg font-semibold mb-4 text-center">SignUp</div>
        {/* Display Status/Error Message (General) */}{" "}
        {statusMessage && (
          <div
            className={`text-sm text-center mb-4 p-2 border rounded ${
              hasFieldErrors // Use the helper to determine if it's a validation error style
                ? "text-red-500 border-red-500"
                : "text-green-600 border-green-600"
            }`}
          >
            {statusMessage}{" "}
          </div>
        )}{" "}
        <Field>
          {" "}
          <Input
            placeholder="username"
            id="username"
            type="text"
            required
            onChange={handleChange}
            value={formData.username}
          />
          {errorDetails?.username && (
            <p className="text-red-500 text-xs mt-1">{errorDetails.username}</p>
          )}{" "}
        </Field>{" "}
        <Field className="grid grid-cols-2 gap-4">
          {" "}
          <Field>
            {" "}
            <Input
              placeholder="first name"
              id="first_name" // Note: This ID matches the snake_case in state
              type="text"
              required
              onChange={handleChange}
              value={formData.first_name}
            />{" "}
          </Field>{" "}
          <Field>
            {" "}
            <Input
              placeholder="last name"
              id="last_name" // Note: This ID matches the snake_case in state
              type="text"
              required
              onChange={handleChange}
              value={formData.last_name}
            />{" "}
          </Field>{" "}
        </Field>{" "}
        <Field>
          {" "}
          <Input
            placeholder="email"
            id="email"
            type="email"
            required
            onChange={handleChange}
            value={formData.email}
          />
          {errorDetails?.email && (
            <p className="text-red-500 text-xs mt-1">{errorDetails.email}</p>
          )}{" "}
        </Field>{" "}
        <Field className="grid grid-cols-2 gap-4">
          {" "}
          <Field>
            {" "}
            <Input
              placeholder="password"
              id="password"
              type="password"
              required
              onChange={handleChange}
              value={formData.password}
            />{" "}
          </Field>{" "}
          <Field>
            {" "}
            <Input
              placeholder="confirm password"
              id="confirm-password" // This ID is mapped to confirmPassword in handleChange
              type="password"
              required
              onChange={handleChange}
              value={formData.confirmPassword}
            />{" "}
          </Field>
          {/* Display password validation errors below the inputs */}
          {errorDetails?.password && (
            <p className="text-red-500 text-xs mt-1 col-span-2">
              {errorDetails.password}
            </p>
          )}{" "}
        </Field>{" "}
        <Field>
          {" "}
          <Button className="cursor-pointer" type="submit" disabled={isLoading}>
            {isLoading ? "Signing Up..." : "Create Account"} {" "}
          </Button>{" "}
        </Field>{" "}
        <FieldSeparator className="*:data-[slot=field-separator-content]:bg-card">
          Or continue with{" "}
        </FieldSeparator>{" "}
        <Button
          variant="outline"
          type="button"
          className="flex items-center justify-center cursor-pointer"
        >
          <FcGoogle className="size-5" /> {" "}
        </Button>{" "}
        <FieldDescription className="text-center">
          Already have an account?{" "}
          <button
            className="hover:text-primary cursor-pointer"
            type="button"
            onClick={() => setSwitchToSignIn(true)}
          >
            Sign in{" "}
          </button>{" "}
        </FieldDescription>{" "}
      </FieldGroup>{" "}
    </form>
  );
};

export default SignUp;
