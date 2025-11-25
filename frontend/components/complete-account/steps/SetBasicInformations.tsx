import { User } from "@/lib/types";
import React from "react";

const SetBasicInformations = (props: {
  next: any;
  formUser: Partial<User> | undefined;
  setFormUser: React.Dispatch<React.SetStateAction<Partial<User> | undefined>>;
}) => {
  return <div>set basic inform component</div>;
};

export default SetBasicInformations;
