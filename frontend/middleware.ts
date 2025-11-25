import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PATHS = [
  "/dashboard",
  "/profile",
  "/settings",
  "/complete-account-informations",
];
const AUTH_ROUTE = [
  "/login",
  "/forgot-password",
  "/confirm-email",
  "/reset-password",
];

function decodeJwt(token: string) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(Buffer.from(payload, "base64").toString());
  } catch {
    return null;
  }
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const authToken = request.cookies.get("auth_token")?.value;

  const isProtectedPath = PROTECTED_PATHS.some((path) =>
    pathname.startsWith(path)
  );
  const isAuthRoute = AUTH_ROUTE.some((path) => pathname.startsWith(path));

  // ===========================
  // 🔥 JWT Expiration Check
  // ===========================
  if (authToken) {
    const decoded = decodeJwt(authToken);
    const isExpired = !decoded || decoded.exp * 1000 < Date.now();

    if (isExpired) {
      // Delete the invalid token
      const response = NextResponse.redirect(new URL("/login", request.url));
      response.cookies.delete("auth_token");
      return response;
    }
  }

  if (isProtectedPath && !authToken) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (isAuthRoute && authToken) {
    return NextResponse.redirect(new URL("/profile", request.url));
  }

  return NextResponse.next();
}

export const config = {
  // Apply middleware to all paths except API, static files, and Next internals
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
