import React from "react";
import { motion } from "motion/react";
import { DollarSign, Search, Users, Globe, ChevronRight, BadgeCheck } from "lucide-react";

const sponsors = [
  { id: 1, name: "TechNova Solutions", industry: "Technology", location: "Dhaka", sponsorshipType: "Corporate", status: "Active" },
  { id: 2, name: "Green Energy Corp", industry: "Renewable Energy", location: "Sylhet", sponsorshipType: "Project", status: "Active" },
  { id: 3, name: "Physics Research Foundation", industry: "Academic", location: "Global", sponsorshipType: "Research", status: "Active" },
  { id: 4, name: "Alumni Venture Capital", industry: "Finance", location: "Chittagong", sponsorshipType: "Venture", status: "Inactive" },
];

export default function Sponsor() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Find a Sponsor</h1>
          <p className="text-zinc-500 text-sm">Connect with corporate and individual sponsors for your research and projects.</p>
        </div>
        <button className="px-6 py-3 bg-white text-black rounded-2xl text-xs font-bold hover:scale-105 transition-transform flex items-center gap-2 shadow-lg shadow-white/10">
          Become a Sponsor <BadgeCheck className="w-4 h-4" />
        </button>
      </div>

      <div className="relative mb-8">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
        <input 
          type="text" 
          placeholder="Search sponsors by name, industry, or location..." 
          className="w-full bg-zinc-900 border border-zinc-800 rounded-2xl py-4 pl-12 pr-4 text-sm text-white focus:border-zinc-600 transition-colors outline-none"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sponsors.map((sponsor) => (
          <motion.div
            key={sponsor.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-8 bg-zinc-900 border border-zinc-800 rounded-3xl hover:border-zinc-700 transition-all group cursor-pointer relative overflow-hidden"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 rounded-2xl bg-zinc-800 flex items-center justify-center text-zinc-400 group-hover:bg-white group-hover:text-black transition-all">
                <DollarSign className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold group-hover:text-white transition-colors">{sponsor.name}</h3>
                <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">{sponsor.industry}</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center gap-3 text-zinc-500 text-sm">
                <Globe className="w-4 h-4" />
                <span>{sponsor.location}</span>
              </div>
              <div className="flex items-center gap-3 text-zinc-500 text-sm">
                <Users className="w-4 h-4" />
                <span>{sponsor.sponsorshipType} Sponsorship</span>
              </div>
            </div>
            
            <div className="mt-8 pt-6 border-t border-zinc-800 flex items-center justify-between">
              <span className={`text-[10px] font-bold uppercase tracking-widest ${sponsor.status === "Active" ? "text-green-500" : "text-zinc-600"}`}>
                {sponsor.status}
              </span>
              <button className="text-zinc-500 group-hover:text-white transition-colors flex items-center gap-2 text-xs font-bold">
                View Details <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
