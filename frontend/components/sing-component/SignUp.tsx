"use client";
import { Separator } from "../ui/separator";
import { Button } from "@/components/ui/button";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { Checkbox } from "@/components/ui/checkbox"; // Ensure you have a Checkbox component
import { z } from "zod";
import { FcGoogle } from "react-icons/fc";

// Define form validation schema with username, email, password, and terms acceptance
const formSchema = z.object({
  username: z
    .string()
    .min(2, { message: "Username must be at least 2 characters." }),
  email: z.string().email({ message: "Invalid email address." }),
  password: z
    .string()
    .min(8, { message: "Password must be at least 8 characters long." }),
  acceptTerms: z.boolean().refine((val) => val === true, {
    message: "You must accept the terms and conditions.",
  }), // Ensure the user accepts the terms
});

const SignUp = () => {
  // Initialize the form using useForm hook and the schema resolver
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      acceptTerms: false, // Initial default value for terms checkbox
    },
  });

  // Define the submit handler function
  function onSubmit(values: any) {
    console.log(values); // Form values: { username, email, password, acceptTerms }
  }

  return (
    <div className="flex items-center justify-center">
      <div className="h-full sm:w-[50vh]">
        <div className="flex items-center justify-center font-poppins font-medium">
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="space-y-7 w-full p-4"
            >
              {/* Field for Username */}
              <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormControl>
                      <Input
                        className="rounded-full"
                        placeholder="Enter your username"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Field for Email */}
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormControl>
                      <Input
                        className="rounded-full"
                        type="email"
                        placeholder="Enter your email"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Field for Password */}
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormControl>
                      <Input
                        className="rounded-full"
                        type="password"
                        placeholder="Enter your password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Checkbox for Accepting Terms */}
              <FormField
                control={form.control}
                name="acceptTerms"
                render={({ field }) => (
                  <FormItem className="flex items-center justify-center space-x-2 text-center">
                    <div className="flex items-center justify-center space-x-2">
                      <FormControl>
                        <div>
                          <Checkbox {...field} />
                        </div>
                      </FormControl>
                      <div className="flex flex-col">
                        <div className="text-[11px] md:text-[15px] text-darkblack">
                          I agree to{" "}
                          <span className="underline text-rose">
                            terms of services.
                          </span>
                        </div>
                        <FormMessage />
                      </div>
                    </div>
                  </FormItem>
                )}
              />

              {/* Submit Button */}
              <div className="flex flex-col items-center justify-center space-y-2">
                <div className="flex items-center justify-center  w-full ">
                  <Button
                    type="submit"
                    className="font-abril w-[60%] rounded-full md:text-[15px]"
                  >
                    Sign Up
                  </Button>
                </div>
                <div className="flex flex-col items-center justify-center space-y-2 w-full">
                  <Button className="w-full md:w-[60%] rounded-full flex items-center justify-around border border-[#DADCE0] bg-white hover:bg-[#DC5949B8] hover:scale-105 transition-all duration-300 ease-in-out">
                    <FcGoogle />
                    <p className="text-darkblack hover:text-matchawith font-abril font-semibold">
                      Sign up with Google
                    </p>
                  </Button>
                </div>
              </div>
            </form>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
