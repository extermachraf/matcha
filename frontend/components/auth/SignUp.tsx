import React from "react";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldSeparator,
} from "../ui/field";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { FcGoogle } from "react-icons/fc";

const SignUp = ({
  setSwitchToSignIn,
}: {
  setSwitchToSignIn: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  return (
    <form className="p-6 md:p-8">
      <FieldGroup>
        <div className="text-lg font-semibold mb-4 text-center">SignUp</div>
        <Field>
          {/* <FieldLabel htmlFor="username">Username</FieldLabel> */}
          <Input placeholder="username" id="username" type="text" required />
        </Field>
        <>
          <Field className="grid grid-cols-2 gap-4">
            <Field>
              {/* <FieldLabel htmlFor="first-name">First Name</FieldLabel> */}
              <Input
                placeholder="first name"
                id="first-name"
                type="text"
                required
              />
            </Field>
            <Field>
              {/* <FieldLabel htmlFor="last-name">Last Name</FieldLabel> */}
              <Input
                placeholder="last name"
                id="last-name"
                type="text"
                required
              />
            </Field>
          </Field>
        </>
        <Field>
          {/* <FieldLabel htmlFor="email">Email</FieldLabel> */}
          <Input placeholder="email" id="email" type="email" required />
        </Field>
        <>
          <Field className="grid grid-cols-2 gap-4">
            <Field>
              {/* <FieldLabel htmlFor="password">Password</FieldLabel> */}
              <Input
                placeholder="password"
                id="password"
                type="password"
                required
              />
            </Field>
            <Field>
              {/* <FieldLabel htmlFor="confirm-password">
                        Confirm Password
                      </FieldLabel> */}
              <Input
                placeholder="confirm password"
                id="confirm-password"
                type="password"
                required
              />
            </Field>
          </Field>
        </>
        <Field>
          <Button className="cursor-pointer" type="submit">
            Create Account
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
          Already have an account?{" "}
          <button
            className="hover:text-primary cursor-pointer"
            type="button"
            onClick={() => setSwitchToSignIn(true)}
          >
            Sign in
          </button>
        </FieldDescription>
      </FieldGroup>
    </form>
  );
};

export default SignUp;
