import { RouteObject } from "react-router-dom";
import HomePage from "../pages/Home/HomePage";
// import ProfilePage from "../pages/User/ProfilePage";
import NotFound from "../pages/NotFound";
// import ProtectedRoute from "./ProtectedRoute";
import MainLayout from "../layouts/MainLayout";
import { SocialMediaLayout } from "@/layouts/SocialMediaLayout";

const routes: RouteObject[] = [
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      // {
      //   path: "profile/:username",
      //   element: (
      //     <ProtectedRoute>
      //       <ProfilePage />
      //     </ProtectedRoute>
      //   ),
      // },
    ],
  },
  {
    path: "/test",
    element: <SocialMediaLayout />,
  },
  { path: "*", element: <NotFound /> },
];

export default routes;
