import TopBar from "./TopBar";
import Sidebar from "./Sidebar";
import Pipeline from "../pages/Pipeline";

export default function AppShell() {
  return (
    <div className="h-screen w-screen bg-[#eef2f6] flex flex-col">
      <TopBar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <Pipeline />
      </div>
    </div>
  );
}
