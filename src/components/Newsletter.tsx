import React from "react";
import { motion } from "motion/react";
import { Mail, Send, CheckCircle2, ChevronRight, BookOpen, Newspaper } from "lucide-react";

const newsletters = [
  { id: 1, title: "SUST Physics News - March 2026", date: "2026-03-01", description: "A monthly update on departmental research and alumni achievements.", category: "Monthly" },
  { id: 2, title: "Special Edition: Quantum Computing", date: "2026-02-15", description: "Deep dive into the latest breakthroughs in quantum physics.", category: "Special" },
  { id: 3, title: "Alumni Spotlight: Dr. Sarah Ahmed", date: "2026-01-20", description: "Interview with our distinguished alumna on her journey to NASA.", category: "Spotlight" },
  { id: 4, title: "SUST Physics News - February 2026", date: "2026-02-01", description: "A monthly update on departmental research and alumni achievements.", category: "Monthly" },
];

export default function Newsletter() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Newsletter</h1>
          <p className="text-zinc-500 text-sm">Stay informed with our monthly updates and special editions.</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
            <input 
              type="email" 
              placeholder="Enter your email..." 
              className="bg-zinc-900 border border-zinc-800 rounded-2xl py-3 pl-12 pr-4 text-sm text-white focus:border-zinc-600 transition-colors outline-none w-64"
            />
          </div>
          <button className="px-6 py-3 bg-white text-black rounded-2xl text-xs font-bold hover:scale-105 transition-transform flex items-center gap-2 shadow-lg shadow-white/10">
            Subscribe <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {newsletters.map((newsletter) => (
          <motion.div
            key={newsletter.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-8 bg-zinc-900 border border-zinc-800 rounded-3xl hover:border-zinc-700 transition-all group cursor-pointer relative overflow-hidden"
          >
            <div className="flex items-start gap-6">
              <div className="w-16 h-16 rounded-2xl bg-zinc-800 flex items-center justify-center text-zinc-400 group-hover:bg-white group-hover:text-black transition-all shrink-0">
                <Newspaper className="w-8 h-8" />
              </div>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">{newsletter.category}</span>
                    <span className="w-1 h-1 bg-zinc-700 rounded-full" />
                    <span className="text-[10px] font-mono text-zinc-500">{newsletter.date}</span>
                  </div>
                  <h3 className="text-xl font-bold group-hover:text-white transition-colors">{newsletter.title}</h3>
                </div>
                <p className="text-sm text-zinc-500 line-clamp-2">{newsletter.description}</p>
                
                <button className="text-zinc-500 group-hover:text-white transition-colors flex items-center gap-2 text-xs font-bold pt-4">
                  Read Issue <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
