const icons = ["🏠", "📊", "📞", "👥", "📁", "⚙️"];

export default function Sidebar() {
  return (
    <div className="w-14 bg-[#163a5f] flex flex-col items-center py-4 gap-6 text-white">
      {icons.map((i, idx) => (
        <div
          key={idx}
          className="w-9 h-9 flex items-center justify-center rounded hover:bg-white/10 cursor-pointer"
        >
          {i}
        </div>
      ))}
    </div>
  );
}
