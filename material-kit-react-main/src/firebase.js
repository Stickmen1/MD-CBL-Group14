// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAbTlml9M4NtG7Ru6u4QP9qEM8kAxrxXX4",
  authDomain: "university-crime.firebaseapp.com",
  projectId: "university-crime",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "120058697534",
  appId: "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
