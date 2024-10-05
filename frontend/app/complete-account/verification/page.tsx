"use client";
import React, { useRef } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp";
import { useRouter } from "next/navigation";

import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";

interface FormInputs {
  otp: string;
}

const Page = () => {
  const {
    handleSubmit,
    formState: { errors },
  } = useForm<FormInputs>();

  // Use ref to capture the entire OTP input
  const otpRef = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const onSubmit: SubmitHandler<FormInputs> = () => {
    // Get the OTP value from the ref
    const otp = otpRef.current?.value || "";
    console.log("Submitted OTP:", otp);
    alert(`OTP Submitted: ${otp}`);
    router.push("/dashboard");
  };

  return (
    <div className="w-full h-full flex items-center justify-center flex-col">
      <div className="flex items-center justify-center flex-col space-y-3">
        <h1 className="font-medium text-titlecolore font-abril text-[20px]">
          Complete Your Profile
        </h1>
        <p>A Code Has Been Sent to Confirm Your Email</p>
        <Separator className="my-2" />

        {/* Form for OTP Input */}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col space-y-4"
        >
          <InputOTP
            ref={otpRef}
            maxLength={6}
            pattern={REGEXP_ONLY_DIGITS_AND_CHARS}
          >
            <InputOTPGroup>
              {[...Array(6)].map((_, index) => (
                <InputOTPSlot key={index} index={index} className="otp-slot" />
              ))}
            </InputOTPGroup>
          </InputOTP>

          {/* Show validation errors if OTP is not filled */}
          {errors.otp && (
            <p className="text-red-500">Please fill in all OTP slots.</p>
          )}

          {/* Submit Button */}
          <Button type="submit">Verify OTP</Button>
        </form>
      </div>
    </div>
  );
};

export default Page;
