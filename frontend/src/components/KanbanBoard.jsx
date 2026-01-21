import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import api from "../api/client";
import LeadCard from "./LeadCard";

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

export default function KanbanBoard({ leads, setLeads }) {
  const grouped = {};
  STAGES.forEach(s => (grouped[s] = []));
  leads.forEach(l => grouped[l.current_stage].push(l));

  const onDragEnd = async (result) => {
    const { destination, source, draggableId } = result;

    if (!destination) return;
    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) return;

    const leadId = parseInt(draggableId);
    const newStage = destination.droppableId;

    // Optimistic UI update
    const updatedLeads = leads.map(l =>
      l.id === leadId ? { ...l, current_stage: newStage } : l
    );
    setLeads(updatedLeads);

    try {
      await api.put(`/pipeline/${leadId}/move`, {
        new_stage: newStage,
        user_id: 2, // TEMP: manager user id
      });
    } catch (err) {
      alert(err.response?.data?.detail || "Stage change failed");
    }
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex gap-4 overflow-x-auto">
        {STAGES.map(stage => (
          <Droppable droppableId={stage} key={stage}>
            {(prov) => (
              <div
                ref={prov.innerRef}
                {...prov.droppableProps}
                className="w-64 bg-gray-100 rounded p-2"
              >
                <h2 className="font-bold mb-2 text-sm">{stage}</h2>
                {grouped[stage].map((lead, i) => (
                  <Draggable draggableId={lead.id.toString()} index={i} key={lead.id}>
                    {(prov) => (
                      <div
                        ref={prov.innerRef}
                        {...prov.draggableProps}
                        {...prov.dragHandleProps}
                        className="mb-2"
                      >
                        <LeadCard lead={lead} />
                      </div>
                    )}
                  </Draggable>
                ))}
                {prov.placeholder}
              </div>
            )}
          </Droppable>
        ))}
      </div>
    </DragDropContext>
  );
}
