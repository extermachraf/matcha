'use client'
import { useEffect, useState } from "react";

// Define an interface for the window size
interface WindowSize {
  width: number | undefined;
  height: number | undefined;
}

// Custom hook to track window size
const useWindowSize = (): WindowSize => {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: undefined,
    height: undefined,
  });

  useEffect(() => {
    // Only run this code in the browser
    const updateSize = () => {
      if (typeof window !== "undefined") {
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      }
    };

    // Set initial size
    updateSize();

    // Add resize event listener
    window.addEventListener("resize", updateSize);

    // Cleanup event listener on unmount
    return () => {
      window.removeEventListener("resize", updateSize);
    };
  }, []);

  return windowSize;
};

export default useWindowSize;
