import React from "react";
import Image from "next/image";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import PlayerFetcher from "@/components/PlayerFetcher";
import PlayerTable from "@/components/PlayerTable";
import GameCarousel from "@/components/GameCarousel";

const Home: React.FC = () => {
  return (
    <main>
      {/* use client */}
      <Navbar />
      {/* use client */}
      <GameCarousel />
      {/* use client */}
      <PlayerTable />
    </main>
  );
};

export default Home;