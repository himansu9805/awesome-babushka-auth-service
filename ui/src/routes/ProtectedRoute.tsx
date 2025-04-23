import React from "react";
import { AuthContext } from "@/contexts/AuthContext";
import { Navigate, useLocation } from "react-router-dom";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const { user, setUser } = React.useContext(AuthContext);
  const accessToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("access_token="))
    ?.split("=")[1];
  const refreshToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("refresh_token="))
    ?.split("=")[1];

  const isAuthenticated = () => {
    if (user) {
      return true;
    } else if (accessToken && refreshToken) {
      const decodedAccessToken = JSON.parse(
        atob(accessToken.split(".")[1])
      );
      setUser(decodedAccessToken);
      return true;
    }
    return false;
  };

  if (!isAuthenticated()) {
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  React.useEffect(() => {
    console.log(document.cookie);
  }, []);

  return <>{children}</>;
};

export default ProtectedRoute;
