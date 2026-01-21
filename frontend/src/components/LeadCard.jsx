export default function LeadCard({ lead }) {
  return (
    <div className="lead-card">
      <strong>{lead.candidate_name}</strong>
      <span>{lead.email}</span>
      <span>{lead.phone}</span>
    </div>
  );
}
