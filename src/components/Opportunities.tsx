import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Briefcase, 
  MapPin, 
  Clock, 
  ExternalLink, 
  Zap, 
  Filter, 
  Search,
  Bookmark,
  Share2,
  Sparkles,
  RefreshCw,
  Globe
} from "lucide-react";

export default function Opportunities() {
  const [activeFilter, setActiveFilter] = useState("all");
  const [opps, setOpps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [agentStatus, setAgentStatus] = useState<any>(null);
  const [isTriggering, setIsTriggering] = useState(false);

  useEffect(() => {
    fetchOpps();
    fetchAgentStatus();
  }, []);

  const fetchOpps = async () => {
    try {
      const res = await fetch("/api/opportunities");
      if (res.ok) {
        const data = await res.json();
        setOpps(data);
      }
    } catch (e) {
      console.error("Failed to fetch opportunities");
    } finally {
      setLoading(false);
    }
  };

  const fetchAgentStatus = async () => {
    try {
      const res = await fetch("/api/ai/agent/status");
      if (res.ok) {
        const data = await res.json();
        setAgentStatus(data);
      }
    } catch (e) {
      console.error("Failed to fetch agent status");
    }
  };

  const triggerAgent = async () => {
    setIsTriggering(true);
    try {
      const res = await fetch("/api/ai/agent/trigger", { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        if (data.success) {
          setOpps(prev => [...data.opportunities, ...prev]);
          fetchAgentStatus();
        }
      }
    } catch (e) {
      console.error("Failed to trigger agent");
    } finally {
      setIsTriggering(false);
    }
  };

  const filteredOpps = opps.filter(opp => {
    if (activeFilter === "all") return true;
    if (activeFilter === "industry" && opp.type.toLowerCase() === "industry") return true;
    return opp.type.toLowerCase() === activeFilter.toLowerCase();
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Opportunity Hub</h1>
          <p className="text-zinc-500 text-sm">Global career and research positions curated for SUST Physics Alumni.</p>
        </div>
        <div className="flex items-center gap-4">
          <button className="px-6 py-3 bg-zinc-900 text-white border border-zinc-800 font-bold rounded-xl flex items-center gap-2 hover:bg-zinc-800 transition-colors">
            Post Opportunity <Briefcase className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* AI Agent Section */}
      <div className="p-8 rounded-3xl bg-gradient-to-br from-zinc-900 to-zinc-950 border border-zinc-800 relative overflow-hidden group">
        <div className="absolute inset-0 bg-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
        <div className="flex flex-col md:flex-row items-center justify-between gap-8 relative z-10">
          <div className="flex items-center gap-6">
            <div className="w-16 h-16 rounded-2xl bg-orange-500/10 flex items-center justify-center text-orange-500 shrink-0 border border-orange-500/20">
              <Sparkles className={`w-8 h-8 ${isTriggering ? 'animate-pulse' : ''}`} />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <h2 className="text-lg font-bold">SUST PHYSICS Opportunity Scout</h2>
                <span className="px-2 py-0.5 bg-orange-500/10 text-orange-500 rounded-full text-[10px] font-bold uppercase tracking-widest border border-orange-500/20">AI Agent</span>
              </div>
              <p className="text-zinc-400 text-sm max-w-md">
                Scanning worldwide physics journals, job boards, and university portals for high-impact roles.
              </p>
              {agentStatus && (
                <div className="flex items-center gap-4 mt-3 text-[10px] font-mono text-zinc-500 uppercase tracking-tighter">
                  <span className="flex items-center gap-1"><Globe className="w-3 h-3" /> Status: {agentStatus.status}</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> Last Scan: {new Date(agentStatus.lastUpdate).toLocaleTimeString()}</span>
                </div>
              )}
            </div>
          </div>
          <button 
            onClick={triggerAgent}
            disabled={isTriggering}
            className={`px-6 py-3 rounded-xl font-bold text-sm flex items-center gap-2 transition-all ${
              isTriggering 
                ? "bg-zinc-800 text-zinc-500 cursor-not-allowed" 
                : "bg-white text-black hover:scale-105 active:scale-95"
            }`}
          >
            {isTriggering ? (
              <>Scanning Global Databases... <RefreshCw className="w-4 h-4 animate-spin" /></>
            ) : (
              <>Trigger Global Search <RefreshCw className="w-4 h-4" /></>
            )}
          </button>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        {["all", "industry", "research", "phd", "internship", "scholarship"].map((filter) => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter)}
            className={`px-4 py-2 rounded-xl text-xs font-bold border transition-all uppercase tracking-widest ${
              activeFilter === filter 
                ? "bg-zinc-100 text-black border-white" 
                : "bg-zinc-900 text-zinc-500 border-zinc-800 hover:border-zinc-600 hover:text-white"
            }`}
          >
            {filter}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6">
        <AnimatePresence mode="popLayout">
          {filteredOpps.map((job) => (
            <motion.div 
              key={job.id}
              layout
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className={`p-8 rounded-3xl bg-zinc-900 border transition-all group relative overflow-hidden ${
                job.isAiGenerated ? 'border-orange-500/30 bg-zinc-900/50' : 'border-zinc-800 hover:border-zinc-700'
              }`}
            >
              {/* AI Badge */}
              {job.isAiGenerated && (
                <div className="absolute top-0 left-0 px-4 py-1 bg-orange-500 text-black text-[10px] font-bold uppercase tracking-widest rounded-br-xl">
                  New AI Finding
                </div>
              )}

              {/* Match Score Badge */}
              <div className="absolute top-0 right-0 p-6">
                <div className="flex flex-col items-end">
                  <div className="flex items-center gap-2 px-3 py-1 bg-orange-500/10 text-orange-500 rounded-full border border-orange-500/20 text-[10px] font-bold mb-1">
                    <Zap className="w-3 h-3" /> {Math.round(job.matchScore)}% AI MATCH
                  </div>
                  <p className="text-[10px] text-zinc-500 font-mono uppercase tracking-tighter">Based on your research profile</p>
                </div>
              </div>

              <div className="flex flex-col md:flex-row gap-8 items-start mt-4 md:mt-0">
                <div className="w-16 h-16 rounded-2xl bg-zinc-800 border border-zinc-700 flex items-center justify-center text-2xl font-bold text-zinc-600 shrink-0">
                  {job.company[0]}
                </div>
                <div className="flex-1 space-y-4">
                  <div>
                    <h3 className="text-xl font-bold group-hover:text-orange-500 transition-colors mb-1">{job.title}</h3>
                    <div className="flex flex-wrap items-center gap-4 text-sm text-zinc-400">
                      <span className="flex items-center gap-1.5"><Briefcase className="w-4 h-4" /> {job.company}</span>
                      <span className="flex items-center gap-1.5"><MapPin className="w-4 h-4" /> {job.location}</span>
                      <span className="flex items-center gap-1.5"><Clock className="w-4 h-4" /> {job.postedAt}</span>
                    </div>
                  </div>
                  
                  <p className="text-zinc-400 text-sm leading-relaxed max-w-3xl">
                    {job.description}
                  </p>

                  <div className="flex flex-wrap gap-2">
                    {(job.tags || []).map((tag: string) => (
                      <span key={tag} className="px-3 py-1 bg-zinc-800 border border-zinc-700 rounded-lg text-[10px] font-mono text-zinc-500">
                        #{tag.toUpperCase()}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center gap-4 pt-4">
                    <button className="px-6 py-2 bg-white text-black font-bold rounded-xl text-sm hover:scale-105 transition-transform flex items-center gap-2">
                      Apply Now <ExternalLink className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-zinc-400 hover:text-white transition-colors">
                      <Bookmark className="w-5 h-5" />
                    </button>
                    <button className="p-2 text-zinc-400 hover:text-white transition-colors">
                      <Share2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
