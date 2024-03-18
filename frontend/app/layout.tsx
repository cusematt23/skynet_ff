import { Inter } from "next/font/google";
import "./globals.css";
import React from "react";

const inter = Inter({ subsets: ["latin"] });

interface Metadata {
  title: string;
  description: string;
}

interface RootLayoutProps {
  children: React.ReactNode;
}

const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export const RootLayout: React.FC<RootLayoutProps> = ({ children }) => {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
};

export default RootLayout;