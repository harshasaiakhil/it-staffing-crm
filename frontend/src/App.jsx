import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Pipeline from "./pages/Pipeline";
import "./styles/crm.css";

export default function App() {
  return (
    <div className="crm-app">
      <Sidebar />
      <div className="main">
        <Topbar />
        <Pipeline />
      </div>
    </div>
  );
}
