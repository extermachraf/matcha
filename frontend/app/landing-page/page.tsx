"use client";
import React from "react"; // Import React and useEffect
import LandingPage from "@/components/phone/LandingPage";
import useWindowSize from "@/hooks/useWindowSize";
import LandingPageTab from "@/components/pc/LandingPageTab";

const LandingPageComponent = () => {
  const { width, height } = useWindowSize();

  if (width <= 633) {
    return <LandingPage />;
  } else {
    return (
      <div className="h-screen">
        <LandingPageTab />
      </div>
    );
  }
};

export default LandingPageComponent;
