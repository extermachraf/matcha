"use client";
import React, { useEffect, useState } from "react";
import api from "@/lib/axiosInstance";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { fetchUserTags } from "@/lib/dataFetcher";

// get user tags from backend
// then if all those uinformations exist
// username, firstName, lastName, email, birthdate, gender, sexualPreferences, profilePictureId and tags
// then redirect to home page
// else render the complete account informations page form

const page = () => {
  const { user, isAuthenticated, isLoading, isProfileComplete } = useAuth();
  const router = useRouter();
  const [userTags, setUserTags] = useState<any[]>([]);

  // console.log(
  //   "this is the useAuth output:",
  //   user,
  //   isAuthenticated,
  //   isLoading,
  //   isProfileComplete
  // );
  useEffect(() => {
    // stop if user not ready
    if (!user || !isAuthenticated || isLoading) return;

    const loadTags = async () => {
      try {
        const tags = await fetchUserTags(user.id);
        setUserTags(tags);

        // redirect logic
        if (isProfileComplete && tags && tags.length > 0) {
          router.push("/profile");
        }
      } catch (error) {
        console.error("error fetching user tags:", error);
      }
    };

    loadTags();
  }, [user, isAuthenticated, isLoading, isProfileComplete]);

  // TODO: complet acount informations logique(split this into steps with componenets)
  // step1: username, firstName, lastName, biography
  // step2: birthdate, gender, sexualPreferences
  // step3: profile images and profile picture upload
  // step4: tags selection

  //TODO: strategy
  //parent wizzard component to handle steps and state
  // each step handle its form and backend api call
  //

  return <div>complet account info page</div>;
};

export default page;
