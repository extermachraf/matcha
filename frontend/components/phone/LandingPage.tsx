"use client"; // Ensure this component is a Client Component

import React from "react";
import Image from "next/image";
import Link from "next/link";
import { useBooleanContext } from "../context/NavBooleanContext"; // Import the context

const LandingPage = () => {
  const { dispatch } = useBooleanContext(); // Get the dispatch function from context

  const handleGetStartedClick = () => {
    dispatch({ type: "toggle" }); // Dispatch action to set state to true
  };

  return (
    <div>
      <div>
        {/* Background image with logo */}
        <div
          className="h-[300px] bg-cover bg-center flex items-end pl-2 pb-2"
          style={{ backgroundImage: "url('/assets/authimages/dakar.png')" }}
        >
          <Image
            className=""
            src="./assets/logo/white-logo.svg"
            alt="Icon"
            width={150}
            height={50}
          />
        </div>

        {/* Text Section */}
        <div className="relative z-50">
          <p className="font-abril text-[30px] font-bold text-titlecolore leading-[134.853%] tracking-[0.64px]">
            STEP INTO A WORLD{" "}
          </p>
          <p className="font-abril text-[30px] font-bold text-titlecolore leading-[134.853%] tracking-[0.64px]">
            OF POSSIBILITIES
          </p>
        </div>

        {/* Image container, with adjusted z-index to stay behind text */}
        <div className="mt-[-15px] flex justify-end z-20 relative">
          <div
            className="w-[154px] h-[214px] bg-cover bg-center"
            style={{ backgroundImage: "url('/assets/authimages/2ounta.png')" }}
          ></div>
        </div>
        <div className="font-poppins mt-[-15px] text-[16px] font-normal leading-normal text-titlecolore -z-20">
          Sign up today and find your <br />
          perfect match! Your journey to love is secured ,<br />
          and protected
        </div>
        <Link href="/landing-page/sing-in-up" onClick={handleGetStartedClick}>
          <p className="text-[20px] font-normal leading-normal tracking-[1.8px] font-abril underline text-rose">
            Get Started
          </p>
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;
