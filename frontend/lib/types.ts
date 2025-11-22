export interface User {
  id: number;
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  biography: string;
  birthdate: string;
  fameRating: number;
  gender: string;
  isVerified: boolean;
  lastSeen: string;
  profilePictureId: number | null;
  sexualPreferences: string;
  createdAt: string;
}
