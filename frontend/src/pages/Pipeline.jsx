import { useEffect, useState } from "react";
import api from "../api/client";
import KanbanBoard from "../components/KanbanBoard";

export default function Pipeline() {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    api.get("/leads").then(res => setLeads(res.data));
  }, []);

  return (
    <div className="p-6">
      <KanbanBoard leads={leads} setLeads={setLeads} />
    </div>
  );
}
