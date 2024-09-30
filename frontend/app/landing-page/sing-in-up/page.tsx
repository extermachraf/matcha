"use client";
import React, { useState } from "react";
import SingIn from "@/components/sing-component/SingIn";
import SignUp from "@/components/sing-component/SignUp"; // Import the SignUp component
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import Image from "next/image";

const Page = () => {
  const [selectedComponent, setSelectedComponent] = useState("signIn");
  const [isSwapped, setIsSwapped] = useState(false);
  const handleSwitch = (component: string) => {
    setSelectedComponent(component);
    setIsSwapped(component === "signUp"); // Swap when "Sign Up" is selected
  };
  const backgroundImage =
    selectedComponent === "signIn"
      ? "url('/assets/authimages/3aziya.jpg')" // Image for Sign In
      : "url('/assets/authimages/bayda.png')"; // Image for Sign Up

  return (
    <div className="w-full min-h-screen pt-[10vh] flex items-center justify-center space-x-3 ">
      <div className="w-[100vh]">
        {/* Parent container with flex-row-reverse for layout switch */}
        <div
          className={`flex items-center justify-center w-full transition-transform duration-700 ease-in-out shadow-lg rounded-lg ${
            isSwapped ? "flex-row-reverse" : ""
          }`}
        >
          <div
            className="hidden md:flex w-[50vh] h-[80vh] bg-cover bg-center transition-all duration-700 ease-in-out"
            style={{ backgroundImage }}
          ></div>

          <div className="w-[90%] sm:w-[50vh] flex items-center h-[80vh] flex-col bg-[#F5F5F5]  transition-all duration-700 ease-in-out justify-around">
            <div className="flex space-y-7 flex-col items-center justify-center">
              <h1 className="text-titlecolore font-abril text-[30px] md:font-bold">
                {selectedComponent === "signIn" ? "Sign In" : "Sign Up"}
              </h1>
              <p className="font-poppins text-darkblack md:font-semibold text-[15px]">
                You are a step away from something great!
              </p>
            </div>
            <Separator className=" m-3"></Separator>
            {selectedComponent === "signIn" ? <SingIn /> : <SignUp />}
            <Separator className=" m-3"></Separator>

            <div className="flex items-center justify-center space-x-4">
              <Button
                type="button"
                onClick={() => handleSwitch("signIn")}
                className={`font-abril transition-all duration-300 ease-in-out rounded-full px-6 py-3 ${
                  selectedComponent === "signIn"
                    ? "bg-[#DC5949B8] text-white"
                    : "bg-white border text-darkblack border-[#DADCE0] hover:bg-[#DC5949B8] hover:text-white"
                }`}
              >
                Sign In
              </Button>
              <Button
                type="button"
                onClick={() => handleSwitch("signUp")}
                className={`font-abril transition-all duration-300 ease-in-out rounded-full px-6 py-3 ${
                  selectedComponent === "signUp"
                    ? "bg-[#DC5949B8] text-white"
                    : "bg-white border border-[#DADCE0] hover:bg-[#DC5949B8] hover:text-white text-black"
                }`}
              >
                Sign Up
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div className="absolute -z-30 hidden sm:block">
        <Image
          className="relative  ml-[53vw] mt-[35vh]"
          src="/assets/authimages/plume.svg"
          alt="Icon"
          width={270}
          height={50}
        />
      </div>
    </div>
  );
};

export default Page;
