import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import LeadCard from "./LeadCard";
import api from "../api/client";

const STAGES = [
  "NEW_LEAD",
  "DNR1",
  "DNR2",
  "DNR3",
  "CONNECTED",
  "QUALIFIED",
  "HOT_PROSPECT",
  "LEAD_WON",
];

export default function PipelineBoard({ leads, setLeads, onLeadClick }) {
  const grouped = {};
  STAGES.forEach(s => (grouped[s] = []));
  leads.forEach(l => grouped[l.current_stage]?.push(l));

  const onDragEnd = async (result) => {
    if (!result.destination) return;

    const leadId = parseInt(result.draggableId);
    const newStage = result.destination.droppableId;

    setLeads(prev =>
      prev.map(l =>
        l.id === leadId ? { ...l, current_stage: newStage } : l
      )
    );

    await api.put(`/leads/${leadId}/stage`, {
      stage: newStage,
    });
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="board">
        {STAGES.map(stage => (
          <Droppable droppableId={stage} key={stage}>
            {(provided) => (
              <div
                className="column"
                ref={provided.innerRef}
                {...provided.droppableProps}
              >
                <h3>{stage.replace("_", " ")}</h3>

                {grouped[stage].map((lead, index) => (
                  <Draggable
                    draggableId={String(lead.id)}
                    index={index}
                    key={lead.id}
                  >
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        onClick={() => onLeadClick(lead)}
                      >
                        <LeadCard lead={lead} />
                      </div>
                    )}
                  </Draggable>
                ))}

                {provided.placeholder}
              </div>
            )}
          </Droppable>
        ))}
      </div>
    </DragDropContext>
  );
}
