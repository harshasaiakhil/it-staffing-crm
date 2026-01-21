export default function TopBar() {
  return (
    <div className="h-14 bg-[#1f4e79] text-white flex items-center px-4 justify-between">
      <div className="font-semibold text-lg">CRM</div>

      <input
        className="w-96 px-3 py-1 rounded bg-[#2e5f8a] placeholder-white/70 outline-none"
        placeholder="Find people, documents, and more"
      />

      <div className="flex items-center gap-4 text-sm">
        <span>5:56 PM</span>
        <span className="bg-green-500 px-2 py-1 rounded text-xs">WORKING</span>
        <span className="font-medium">Akhil</span>
      </div>
    </div>
  );
}
