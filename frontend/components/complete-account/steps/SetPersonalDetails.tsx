import React from "react";
import { User } from "@/lib/types";

const SetPersonalDetails = (pros: {
  next: any;
  back: any;
  formUser: Partial<User> | undefined;
  setFormUser: React.Dispatch<React.SetStateAction<Partial<User> | undefined>>;
}) => {
  return <div>set personal details component</div>;
};

export default SetPersonalDetails;
