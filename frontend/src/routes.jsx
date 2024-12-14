import { Route, Routes } from "react-router-dom";
import Home from "./views/Home";
import { MainLayout } from "./layout/main-layout";

export const Routers = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route path="/" element={<Home />} />
      </Route>
    </Routes>
  );
};
