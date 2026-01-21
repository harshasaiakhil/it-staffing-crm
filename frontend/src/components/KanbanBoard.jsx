import PipelineColumn from "./PipelineColumn";

const STAGES = [
  "NEW_LEAD",
  "DNR_1",
  "DNR_2",
  "DNR_3",
  "CONNECTED",
  "QUALIFIED",
  "HOT_PROSPECT",
  "LEAD_WON",
];

export default function KanbanBoard({ leads }) {
  const grouped = {};
  STAGES.forEach(stage => (grouped[stage] = []));

  leads.forEach(lead => {
    if (grouped[lead.current_stage]) {
      grouped[lead.current_stage].push(lead);
    }
  });

  return (
    <div className="flex gap-6 min-h-full">
      {STAGES.map(stage => (
        <PipelineColumn
          key={stage}
          stage={stage}
          leads={grouped[stage]}
        />
      ))}
    </div>
  );
}
