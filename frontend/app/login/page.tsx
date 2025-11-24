import { SignInUpForm } from "@/components/auth/signin-up-form";

// TASK-1: refactore sign in component to handle api logique
// TASK-2: refactore sign up component to handle api logique
// TASK-3: implement gloabal authentication status hook and helper
// TASK-4: protect routes that need authentication

export default function SignupPage() {
  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm md:max-w-4xl">
        <SignInUpForm />
      </div>
    </div>
  );
}
