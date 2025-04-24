import React, { ReactNode } from "react";

interface DialogBoxProps {
  isOpen: boolean;
  onClose: () => void;
  children?: ReactNode;
}

const DialogBox: React.FC<DialogBoxProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
      <div className="relative bg-white rounded-lg shadow-md">

        <button
          onClick={onClose}
          className="absolute top-3 right-5 text-gray-500 hover:text-gray-700 text-lg font-bold focus:outline-none"
          aria-label="Close"
        >
          &times;
        </button>
        {children}
      </div>
    </div >
  );
};

export default DialogBox;
