import React from "react";
import { Navigate, useLocation } from "react-router-dom";

const isAuthenticated = () => {
  // TODO: replace with real auth logic
  return !!localStorage.getItem("token");
};

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();

  if (!isAuthenticated()) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
