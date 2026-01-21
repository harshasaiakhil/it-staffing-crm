import { useEffect, useState } from "react";
import api from "../api/client";
import PipelineBoard from "../components/PipelineBoard";
import LeadDrawer from "../components/LeadDrawer";

export default function Pipeline() {
  const [leads, setLeads] = useState([]);
  const [selectedLead, setSelectedLead] = useState(null);

  useEffect(() => {
    api.get("/leads").then(res => setLeads(res.data));
  }, []);

  return (
    <div className="pipeline">
      <PipelineBoard
        leads={leads}
        setLeads={setLeads}
        onLeadClick={setSelectedLead}
      />

      <LeadDrawer
        lead={selectedLead}
        onClose={() => setSelectedLead(null)}
      />
    </div>
  );
}
