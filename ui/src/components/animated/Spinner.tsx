import React from "react";

interface ISpinnerProps {
  size?: 'small' | 'medium' | 'large';
}

const Spinner: React.FC<ISpinnerProps> = ({ size = 'small' }) => {
  const sizeClasses = {
    small: 'w-6 h-6 border-4',
    medium: 'w-8 h-8 border-4',
    large: 'w-10 h-10 border-4',
  };

  return (
    <div className="flex items-center justify-center">
      <div className={`${sizeClasses[size]} border-gray-300 border-t-[#36322F] rounded-full animate-spin`} />
    </div>
  );
}

export default Spinner;