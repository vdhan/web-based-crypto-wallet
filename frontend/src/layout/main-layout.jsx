import { Outlet } from "react-router-dom";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar/Sidebar";

export const MainLayout = () => {
  return (
    <div className="flex flex-row   h-screen p-0 m-0">
      {/* Sidebar */}
      <div className="  top-0   w-[300px] p-0 m-0 ">
        <Sidebar />
      </div>
      <div className="flex-1 overflow-y-auto  ">
        {/* Header */}
        <div className="  w-full h-[100px]">
          <Header />
        </div>
        {/* Main */}
        <div className="h-[85vh]">
          <Outlet />
        </div>
      </div>
    </div>
  );
};
