"use client";
import React, { useState } from "react";
import SetBasicInformations from "./steps/SetBasicInformations";
import SetPersonalDetails from "./steps/SetPersonalDetails";
import SetPictures from "./steps/SetPictures";
import SetTags from "./steps/SetTags";
import { User } from "@/lib/types";

const Wizzard = (userTags: string[]) => {
  const [step, setStep] = useState(1);
  const next = () => setStep((prev) => prev + 1);
  const back = () => setStep((prev) => prev - 1);

  const [formUser, setFormUser] = useState<Partial<User> | undefined>();
  //   const [pictures, setPictures] = useState<File[]>([]);
  //   const [tags, setTags] = useState<string[]>(userTags);
  return (
    <div className="max-w-lg mx-auto mt-10">
      {step === 1 && (
        <SetBasicInformations
          next={next}
          formUser={formUser}
          setFormUser={setFormUser}
        />
      )}
      {step === 2 && (
        <SetPersonalDetails
          next={next}
          back={back}
          formUser={formUser}
          setFormUser={setFormUser}
        />
      )}
      {step === 3 && <SetPictures next={next} back={back} />}
      {step === 4 && <SetTags userTags={userTags} back={back} />}
    </div>
  );
};

export default Wizzard;
