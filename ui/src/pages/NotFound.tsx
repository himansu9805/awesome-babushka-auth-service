import React from 'react';
import { Link } from 'react-router-dom';
import NeumorphButton from '../components/commons/neumorph-button';

const NotFound = () => {
  return (
    <div className="h-screen flex flex-col justify-center items-center text-center p-4">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-gray-600 mb-6">Oops! This page doesn't exist.</p>
      <Link to="/">
        <NeumorphButton>
          Back to Home
        </NeumorphButton>
      </Link>
    </div>
  );
};

export default NotFound;
