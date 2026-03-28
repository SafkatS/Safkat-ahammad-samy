import React from "react";
import { motion } from "motion/react";
import { Bell, Calendar, ChevronRight, Pin } from "lucide-react";

const notices = [
  { id: 1, title: "Annual Alumni Meetup 2026", date: "2026-04-15", category: "Event", priority: "High" },
  { id: 2, title: "New Research Grant for Physics Graduates", date: "2026-03-25", category: "Academic", priority: "Medium" },
  { id: 3, title: "Departmental Seminar: Quantum Computing", date: "2026-04-02", category: "Seminar", priority: "Low" },
  { id: 4, title: "Alumni Membership Renewal Deadline", date: "2026-03-31", category: "Admin", priority: "High" },
];

export default function Notice() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Notice Board</h1>
        <p className="text-zinc-500 text-sm">Stay updated with the latest announcements from the department and alumni association.</p>
      </div>

      <div className="space-y-4">
        {notices.map((notice) => (
          <motion.div
            key={notice.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-6 bg-zinc-900 border border-zinc-800 rounded-3xl hover:border-zinc-700 transition-all group cursor-pointer"
          >
            <div className="flex items-start justify-between">
              <div className="flex gap-4">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 ${
                  notice.priority === "High" ? "bg-red-500/10 text-red-500" : 
                  notice.priority === "Medium" ? "bg-orange-500/10 text-orange-500" : 
                  "bg-blue-500/10 text-blue-500"
                }`}>
                  <Pin className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">{notice.category}</span>
                    <span className="w-1 h-1 bg-zinc-700 rounded-full" />
                    <span className="text-[10px] font-mono text-zinc-500">{notice.date}</span>
                  </div>
                  <h3 className="text-lg font-bold group-hover:text-white transition-colors">{notice.title}</h3>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-zinc-700 group-hover:text-white transition-colors" />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
