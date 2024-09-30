import { ReactNode } from "react";
import Navbar from "@/components/navbars/Navbar";
import { BooleanProvider } from "@/components/context/NavBooleanContext";
interface LayoutProps {
  children: ReactNode; // Type for children prop
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <BooleanProvider>
      <div className="min-h-screen flex flex-col">
        {/* Navbar at the top */}
        <Navbar />

        {/* Main content */}
        <main className="w-full h-full px-2">{children}</main>

        {/* Footer at the bottom */}
        {/* <Footer /> */}
      </div>
    </BooleanProvider>
  );
};

export default Layout;
