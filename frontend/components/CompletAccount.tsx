"use client";

import React, { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { ChevronRightIcon } from "@radix-ui/react-icons";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { MdPhotoCamera } from "react-icons/md";
import Image from "next/image";

// Zod validation schema
const formSchema = z.object({
  firstName: z
    .string()
    .min(2, "First name must be at least 2 characters long."),
  lastName: z.string().min(2, "Last name must be at least 2 characters long."),
  gender: z.enum(["Male", "Female", "Other"]),
  sexualPreference: z.enum(["Male", "Female"]),
  age: z.string(),
  profilePicture: z.any(),
});

const CompletAccount = () => {
  const defaultImageUrl = "/path/to/your/default/image.jpg"; // Replace with your actual default image path
  const [previewPhoto, setPreviewPhoto] = useState<string | null>(
    defaultImageUrl
  );
  const [file, setFile] = useState<File | null>(null);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      gender: "",
      sexualPreference: "",
      age: undefined,
    },
  });

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const fileURL = URL.createObjectURL(selectedFile);
      setPreviewPhoto(fileURL);
      form.setValue("profilePicture", selectedFile); // Set the selected file in the form
    } else {
      setPreviewPhoto(defaultImageUrl);
      form.setValue("profilePicture", null); // Reset the value in the form
    }
  };

  const onSubmit = (values: any) => {
    console.log("Form Data:", values);
  };

  return (
    <div className=" flex items-center justify-center transition-transform duration-700 ease-in-out shadow-lg w-full h-full p-4">
      <div className="transition-transform duration-700 ease-in-out w-full  h-full sm:w-[50vh] flex items-center justify-center flex-col ">
        <h1 className="font-medium text-titlecolore text-[15px] md:text-[25px] font-abril ">
          Complete Your Profile
        </h1>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-7 w-full p-4"
          >
            {/* Profile Picture */}
            <FormField
              control={form.control}
              name="profilePicture"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div>
                      <div className="flex items-center justify-center">
                        <div className="border  flex justify-center mb-4 rounded-full overflow-hidden w-24 h-24">
                          <Image
                            src={previewPhoto || defaultImageUrl}
                            alt="Profile Preview"
                            width={100}
                            height={100}
                            className="rounded-full object-cover transition-transform duration-300 transform hover:scale-110"
                          />
                        </div>
                      </div>
                      <Input
                        type="file"
                        id="profilePicture"
                        accept="image/*"
                        {...field}
                        onChange={(e) => {
                          handlePhotoChange(e);
                          field.onChange(e); // Let react-hook-form handle the field change
                        }}
                        style={{ display: "none" }}
                      />
                      <div
                        className="flex items-center justify-center cursor-pointer hover:opacity-80 transition-opacity duration-200"
                        onClick={() =>
                          document.getElementById("profilePicture")?.click()
                        }
                      >
                        <MdPhotoCamera className="text-rose" size={30} />
                      </div>
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* First Name */}
            <FormField
              control={form.control}
              name="firstName"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      placeholder="First Name"
                      {...field}
                      className="focus:ring-rose focus:border-rose  transition-colors duration-200"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Last Name */}
            <FormField
              control={form.control}
              name="lastName"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      placeholder="Last Name"
                      {...field}
                      className="focus:ring-rose focus:border-rose  transition-colors duration-200"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Gender */}
            <FormField
              control={form.control}
              name="gender"
              render={({ field }) => (
                <FormItem>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    className="focus:ring-rose focus:border-rose transition-colors duration-200"
                  >
                    <FormControl>
                      <SelectTrigger className="">
                        <SelectValue placeholder="Select Gender" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="Male">Male</SelectItem>
                      <SelectItem value="Female">Female</SelectItem>
                      <SelectItem value="Other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Sexual Preference */}
            <FormField
              control={form.control}
              name="sexualPreference"
              render={({ field }) => (
                <FormItem>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    className="focus:ring-rose focus:border-rose transition-colors duration-200"
                  >
                    <FormControl>
                      <SelectTrigger className="">
                        <SelectValue placeholder="Select Sexual Preference" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="Male">Male</SelectItem>
                      <SelectItem value="Female">Female</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Age */}
            <FormField
              control={form.control}
              name="age"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      type="number"
                      placeholder="Age"
                      {...field}
                      className="focus:ring-rose focus:border-rose  transition-colors duration-200"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="flex flex-col items-center justify-center space-y-2">
              <Button
                type="submit"
                variant="outline"
                size="icon"
                className="font-abril rounded-full md:text-[15px]  transition-colors duration-300 transform hover:bg-rose hover:text-matchawith hover:scale-105"
              >
                <ChevronRightIcon className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </Form>
      </div>
    </div>
  );
};

export default CompletAccount;
