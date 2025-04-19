import React from 'react';
import { Outlet } from 'react-router-dom';
import doodleBackground from '@/assets/images/doodle.png';

const MainLayout = () => {
  return (
    <main
      className="min-h-screen bg-gray-100"
      style={{
        backgroundImage: `radial-gradient(circle, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.75) 70%), url(${doodleBackground})`,
        backgroundSize: 'contain',
        backgroundPosition: 'center',
        backgroundBlendMode: 'darken',
      }}
    >
      <div className="mx-[100px]">
        <Outlet />
      </div>
    </main>
  );
};

export default MainLayout;
