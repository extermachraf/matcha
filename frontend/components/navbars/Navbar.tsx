"use client";

import Image from "next/image";
import Link from "next/link";
import { MdCancel } from "react-icons/md";
import { useBooleanContext } from "../context/NavBooleanContext";
import { useEffect, useState } from "react";

const Navbar = () => {
  const { state, dispatch } = useBooleanContext();
  const [isClient, setIsClient] = useState(false); // State to check if we're on the client

  useEffect(() => {
    // Ensure this only runs on the client
    setIsClient(true);
  }, []);

  const toggleLanding = () => {
    dispatch({ type: "toggle" }); // Toggle the state on button click
  };

  return (
    <div className="bg-matchawith fixed w-full flex items-center justify-between h-[50px] p-[20px]">
      <Image
        className=""
        src="/assets/logo/logo.svg"
        alt="Icon"
        width={120}
        height={50}
      />
      <Link
        href={state.isToggled ? "/landing-page/" : "/landing-page/sing-in-up"} // Use the boolean state
        className="w-fit p-2 h-[30px] text-center bg-darkblack text-matchawith text-[14px] rounded-[4px] font-poppins font-bold transition-all duration-300 ease-in-out transform hover:bg-matchawith hover:text-darkblack hover:scale-105 flex items-center justify-center"
        onClick={toggleLanding} // Call toggleLanding on click
      >
        {/* Conditionally render the icon only if we're on the client */}
        {state.isToggled && isClient ? (
          <MdCancel className="text-[20px]" />
        ) : (
          "Sign In/Up"
        )}{" "}
      </Link>
    </div>
  );
};

export default Navbar;
