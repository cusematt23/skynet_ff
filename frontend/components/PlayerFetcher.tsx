"use client";


import React, { useState, useEffect } from 'react';





const PlayerFetcher = () => {

  const [playerData, setPlayerData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://0.0.0.0:8003/slateplayers/9');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setPlayerData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData(); // Call the function to fetch data when the component mounts
  }, []); // Empty dependency array means this effect runs only once after the initial render

  return (
    <div>
      {playerData ? (
        <div>
          {/* Render fetched player data here */}
          <p>Name: {playerData[1].player_name}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default PlayerFetcher;



