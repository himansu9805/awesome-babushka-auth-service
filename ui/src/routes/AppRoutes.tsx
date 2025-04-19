import React from "react";
import { useRoutes } from "react-router-dom";
import routes from "./index";

const AppRoutes = () => {
  const element = useRoutes(routes);
  return element;
};

export default AppRoutes;
