import { useEffect, useState } from "react";
import api from "../api/client";

export default function LeadDrawer({ lead, onClose }) {
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  const [resume, setResume] = useState(null);

  useEffect(() => {
    if (!lead) return;
    api.get(`/leads/${lead.id}/comments`).then(res => setComments(res.data));
  }, [lead]);

  if (!lead) return null;

  const addComment = async () => {
    if (!comment.trim()) return;
    const res = await api.post(`/leads/${lead.id}/comments`, { text: comment });
    setComments(prev => [res.data, ...prev]);
    setComment("");
  };

  const uploadResume = async () => {
    if (!resume) return;
    const form = new FormData();
    form.append("file", resume);

    await api.post(`/leads/${lead.id}/resume`, form);
    alert("Resume uploaded");
  };

  return (
    <div className="drawer">
      <div className="drawer-header">
        <strong>{lead.candidate_name}</strong>
        <button onClick={onClose}>✕</button>
      </div>

      <div className="drawer-body">
        <p><b>Email:</b> {lead.email}</p>
        <p><b>Phone:</b> {lead.phone}</p>

        <hr />

        <h4>Resume</h4>
        <input
          type="file"
          accept=".pdf"
          onChange={e => setResume(e.target.files[0])}
        />
        <button onClick={uploadResume}>Upload</button>

        <hr />

        <h4>Comments</h4>
        <textarea
          rows="3"
          placeholder="Add conversation notes..."
          value={comment}
          onChange={e => setComment(e.target.value)}
        />
        <button onClick={addComment}>Add Comment</button>

        <div style={{ marginTop: 12 }}>
          {comments.map(c => (
            <div key={c.id} className="comment">
              <div>{c.text}</div>
              <small>{new Date(c.created_at).toLocaleString()}</small>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
