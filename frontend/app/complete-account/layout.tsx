import { ReactNode } from "react";
interface LayoutProps {
  children: ReactNode; // Type for children prop
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen min-w-screen flex items-center justify-center">
      <div
        className="hidden md:flex w-[50vh] h-[80vh] bg-cover bg-center transition-all duration-700 ease-in-out"
        style={{ backgroundImage: "url('/assets/complet-info.png')" }}
      ></div>
      <div className="w-screen h-[80vh] md:w-[50vw]">{children}</div>
    </div>
  );
};

export default Layout;
