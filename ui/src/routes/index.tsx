import { RouteObject } from "react-router-dom";
import WelcomePage from "@/pages/Welcome/WelcomePage";
import NotFound from "@/pages/NotFound";
import MainLayout from "@/layouts/MainLayout";
import SocialMediaLayout from "@/layouts/SocialMediaLayout";
import ProtectedRoute from "@/routes/ProtectedRoute";
import HomePage from "@/pages/Home/HomePage";

const routes: RouteObject[] = [
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <WelcomePage /> },
    ],
  },
  {
    path: "/home",
    element: (
      <ProtectedRoute>
        <SocialMediaLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <HomePage /> },
    ],
  },
  { path: "*", element: <NotFound /> },
];

export default routes;
