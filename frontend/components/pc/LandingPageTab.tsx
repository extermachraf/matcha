"use client";
import React from "react";
import Image from "next/image";
import Link from "next/link";
import { useBooleanContext } from "../context/NavBooleanContext";
const LandingPageTab = () => {
  const { dispatch } = useBooleanContext(); // Get the dispatch function from context

  // const hoverEffectClass = `
  //   transition-all duration-300 ease-in-out transform
  //   hover:text-darkblack hover:scale-105
  // `;
  const handleGetStartedClick = () => {
    dispatch({ type: "toggle" }); // Dispatch action to set state to true
  };
  return (
    <div className="h-full flex items-center justify-center  flex-col">
      <Image
        className="absolute mr-[470px] mb-[140px]"
        src="/assets/authimages/desktopimages/girl1.jpg"
        alt="Icon"
        width={90}
        height={100}
        quality={100} // Highest quality
      />
      <Image
        className="h-[180px] absolute ml-[500px] mb-[180px]"
        src="/assets/authimages/desktopimages/man1.jpg"
        alt="Icon"
        width={140}
        height={100}
        quality={100} // Highest quality
      />
      <Image
        className="absolute ml-[570px] mt-[248px]"
        src="/assets/authimages/desktopimages/girl2.jpg"
        alt="Icon"
        width={90}
        height={50}
      />
      <Image
        className="absolute mr-[370px] mt-[300px]"
        src="/assets/authimages/desktopimages/man2.jpg"
        alt="Icon"
        width={120}
        height={50}
      />
      <div className="absolute flex text-titlecolore flex-col items-center space-y-[-3px] justify-center">
        <p className="text-[40px] font-poppins">Heart Beat</p>
        <p className="text-[40px] font-abril font-medium tracking-[8px]">
          IT’S A DATING APP
        </p>
        <p className="text-[30px] leading font-abril font-normal tracking-[1px]">
          STEP INTO A WORLD OF POSSIBILITIES
        </p>
      </div>
      <Link href="/landing-page/sing-in-up" onClick={handleGetStartedClick}>
        {/* Apply the hover effect by concatenating the hoverEffectClass */}
        <p
          className={`absolute mt-[200px] items-end text-[35px] font-bold leading-normal tracking-[1.8px] font-poppins underline text-rose hover-effect`}
        >
          Get Started
        </p>
      </Link>
    </div>
  );
};

export default LandingPageTab;
