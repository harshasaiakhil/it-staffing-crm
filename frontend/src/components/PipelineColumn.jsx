import LeadCard from "./LeadCard";

export default function PipelineColumn({ stage, leads }) {
  return (
    <div className="min-w-[320px] max-w-[320px] bg-[#f7f9fc] rounded-lg shadow-sm flex flex-col">
      
      {/* HEADER */}
      <div className="px-4 py-3 bg-white border-b sticky top-0 z-10">
        <div className="flex justify-between items-center">
          <span className="text-sm font-semibold tracking-wide">
            {stage.replace("_", " ")}
          </span>
          <span className="text-xs bg-gray-200 px-2 py-0.5 rounded-full">
            {leads.length}
          </span>
        </div>
      </div>

      {/* CARDS */}
      <div className="p-3 overflow-y-auto">
        {leads.map(lead => (
          <LeadCard key={lead.id} lead={lead} />
        ))}
      </div>
    </div>
  );
}
