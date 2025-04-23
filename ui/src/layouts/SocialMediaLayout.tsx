import React from 'react';
import { Outlet } from 'react-router-dom';

const SocialMediaLayout = () => {
  return (
    <main className="mx-4 md:mx-20">
      <Outlet />
    </main>
  )
};

export default SocialMediaLayout;