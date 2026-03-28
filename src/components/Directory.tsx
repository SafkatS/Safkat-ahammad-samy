import React, { useState, useEffect } from "react";
import { motion } from "motion/react";
import { 
  Map as MapIcon, 
  Search, 
  Filter, 
  Globe, 
  Users, 
  MessageCircle,
  Linkedin,
  GraduationCap
} from "lucide-react";

const alumniData = [
  { id: 1, name: "Dr. S. Ahmed", batch: "2008-09", location: "Geneva, Switzerland", role: "Research Scientist at CERN", lat: 46.2044, lng: 6.1432 },
  { id: 2, name: "N. Sultana", batch: "2012-13", location: "Mountain View, USA", role: "Senior Data Scientist at Google", lat: 37.3861, lng: -122.0839 },
  { id: 3, name: "M. Rahman", batch: "2015-16", location: "Dhaka, Bangladesh", role: "Assistant Professor at SUST", lat: 23.8103, lng: 90.4125 },
  { id: 4, name: "A. Karim", batch: "2010-11", location: "London, UK", role: "Quantitative Analyst at Goldman Sachs", lat: 51.5074, lng: -0.1278 },
  { id: 5, name: "F. Begum", batch: "2018-19", location: "Tokyo, Japan", role: "PhD Candidate at University of Tokyo", lat: 35.6762, lng: 139.6503 },
];

export default function Directory() {
  const [searchTerm, setSearchTerm] = useState("");
  const [viewMode, setViewMode] = useState<"list" | "map">("list");
  const [alumni, setAlumni] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlumni = async () => {
      try {
        const res = await fetch("/api/directory");
        if (res.ok) {
          const data = await res.json();
          setAlumni(data);
        }
      } catch (e) {
        console.error("Failed to fetch directory");
      } finally {
        setLoading(false);
      }
    };
    fetchAlumni();
  }, []);

  const filteredAlumni = alumni.filter(person => 
    person.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    person.batch.includes(searchTerm) ||
    (person.currentIndustry || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Alumni Directory</h1>
          <p className="text-zinc-500 text-sm">Explore the global network of SUST Physics graduates.</p>
        </div>
        <div className="flex items-center gap-4 w-full md:w-auto">
          <div className="relative flex-1 md:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
            <input 
              type="text" 
              placeholder="Search by name, batch, or company..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
            />
          </div>
          <button className="p-3 bg-zinc-900 border border-zinc-800 rounded-xl hover:bg-zinc-800 transition-colors">
            <Filter className="w-5 h-5 text-zinc-400" />
          </button>
          <div className="flex bg-zinc-900 border border-zinc-800 rounded-xl p-1">
            <button 
              onClick={() => setViewMode("list")}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${viewMode === "list" ? "bg-white text-black" : "text-zinc-500 hover:text-white"}`}
            >
              LIST
            </button>
            <button 
              onClick={() => setViewMode("map")}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${viewMode === "map" ? "bg-white text-black" : "text-zinc-500 hover:text-white"}`}
            >
              MAP
            </button>
          </div>
        </div>
      </div>

      {viewMode === "list" ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAlumni.map((person) => (
            <motion.div 
              key={person.uid}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 hover:border-zinc-700 transition-all group"
            >
              <div className="flex items-start justify-between mb-6">
                <div className="w-16 h-16 rounded-2xl bg-zinc-800 border border-zinc-700 flex items-center justify-center text-2xl font-bold text-zinc-500 overflow-hidden">
                  {person.photoURL ? (
                    <img src={person.photoURL} alt={person.displayName} className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all" />
                  ) : (
                    person.displayName.split(" ").map((n: string) => n[0]).join("")
                  )}
                </div>
                <div className="flex gap-2">
                  <button className="p-2 bg-zinc-800 hover:bg-blue-600 hover:text-white rounded-lg transition-all">
                    <Linkedin className="w-4 h-4" />
                  </button>
                  <button className="p-2 bg-zinc-800 hover:bg-[#25D366] hover:text-white rounded-lg transition-all">
                    <MessageCircle className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <div className="space-y-1 mb-6">
                <h3 className="text-lg font-bold group-hover:text-orange-500 transition-colors">{person.displayName}</h3>
                <p className="text-xs text-zinc-500 font-mono flex items-center gap-2 uppercase tracking-widest">
                  <GraduationCap className="w-3 h-3" /> BATCH {person.batch}
                </p>
              </div>
              <div className="space-y-3 pt-4 border-t border-zinc-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-xs text-zinc-400">
                    <Users className="w-4 h-4 text-zinc-600" />
                    <span>{person.currentIndustry || "Alumni"}</span>
                  </div>
                  <div className="text-[8px] font-mono text-zinc-600 uppercase tracking-widest">
                    UID: {person.uid}
                  </div>
                </div>
                <div className="flex items-center gap-3 text-xs text-zinc-400">
                  <Globe className="w-4 h-4 text-zinc-600" />
                  <span>{person.location}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="h-[60vh] w-full bg-zinc-900 border border-zinc-800 rounded-3xl relative overflow-hidden flex items-center justify-center">
          <div className="absolute inset-0 opacity-20 pointer-events-none" 
               style={{ backgroundImage: 'radial-gradient(#ffffff 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
          <div className="text-center space-y-4">
            <Globe className="w-16 h-16 text-zinc-700 mx-auto animate-pulse" />
            <p className="text-zinc-500 font-mono text-xs uppercase tracking-widest">Interactive Alumni Map Initializing...</p>
            <div className="flex flex-wrap justify-center gap-2 max-w-md">
              {filteredAlumni.map(a => (
                <div key={a.uid} className="px-3 py-1 bg-zinc-800 border border-zinc-700 rounded-full text-[10px] text-zinc-400">
                  {a.location}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
