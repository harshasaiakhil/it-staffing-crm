import { useEffect, useState } from "react";
import api from "../api/client";

export default function LeadDetailDrawer({ lead, onClose }) {
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  useEffect(() => {
    if (lead) {
      api.get(`/comments/${lead.id}`).then(res => setComments(res.data));
    }
  }, [lead]);

  if (!lead) return null;

  const addComment = async () => {
    await api.post(`/comments/${lead.id}`, {
      user_id: 2,
      text,
    });
    setComments([...comments, { text, user_id: 2 }]);
    setText("");
  };

  const uploadResume = async () => {
    const formData = new FormData();
    formData.append("file", file);

    await api.post(`/resumes/${lead.id}`, formData);
    alert("Resume uploaded");
  };

  return (
    <div className="fixed top-0 right-0 w-96 h-full bg-white shadow-lg p-4 z-50">
      <button
        onClick={onClose}
        className="text-sm text-gray-500 mb-3"
      >
        Close
      </button>

      <h2 className="text-lg font-bold">{lead.candidate_name}</h2>
      <p className="text-sm">{lead.email}</p>
      <p className="text-sm mb-4">{lead.phone}</p>

      {/* Resume */}
      <div className="mb-4">
        <h3 className="font-semibold mb-1">Resume</h3>
        <input
          type="file"
          accept=".pdf"
          onChange={e => setFile(e.target.files[0])}
        />
        <button
          onClick={uploadResume}
          className="mt-2 bg-blue-600 text-white px-3 py-1 rounded"
        >
          Upload
        </button>
      </div>

      {/* Comments */}
      <div>
        <h3 className="font-semibold mb-2">Comments</h3>
        <div className="h-40 overflow-y-auto border p-2 mb-2 text-sm">
          {comments.map((c, i) => (
            <div key={i} className="mb-1">
              • {c.text}
            </div>
          ))}
        </div>
        <textarea
          className="w-full border p-1 text-sm"
          rows={2}
          value={text}
          onChange={e => setText(e.target.value)}
        />
        <button
          onClick={addComment}
          className="mt-2 bg-green-600 text-white px-3 py-1 rounded"
        >
          Add Comment
        </button>
      </div>
    </div>
  );
}
