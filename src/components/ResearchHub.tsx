import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  BookOpen, 
  Code, 
  Database, 
  FileText, 
  Search, 
  Users, 
  Zap, 
  ExternalLink, 
  Github, 
  Download,
  ChevronRight,
  Sparkles,
  Quote,
  UserPlus
} from "lucide-react";

interface ResearchItem {
  id: string;
  title: string;
  authors: string[];
  type: "Paper" | "Preprint" | "Code" | "Dataset";
  journal: string;
  year: number;
  abstract: string;
  tags: string[];
  link: string;
  codeLink?: string;
  datasetLink?: string;
}

export default function ResearchHub() {
  const [items, setItems] = useState<ResearchItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeSubTab, setActiveSubTab] = useState<"repository" | "citation" | "collaboration">("repository");
  const [filter, setFilter] = useState("all");
  const [selectedItem, setSelectedItem] = useState<ResearchItem | null>(null);
  const [similarWork, setSimilarWork] = useState<ResearchItem[]>([]);
  const [collaborators, setCollaborators] = useState<any[]>([]);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const res = await fetch("/api/research");
      if (res.ok) {
        const data = await res.json();
        setItems(data);
      }
    } catch (e) {
      console.error("Failed to fetch research items");
    } finally {
      setLoading(false);
    }
  };

  const fetchAiInsights = async (item: ResearchItem) => {
    setAiLoading(true);
    try {
      const [similarRes, collabRes] = await Promise.all([
        fetch(`/api/research/similar/${item.id}`),
        fetch(`/api/research/collaborators/${item.id}`)
      ]);
      
      if (similarRes.ok) setSimilarWork(await similarRes.json());
      if (collabRes.ok) setCollaborators(await collabRes.json());
    } catch (e) {
      console.error("AI insights failed");
    } finally {
      setAiLoading(false);
    }
  };

  const filteredItems = items.filter(item => 
    filter === "all" || item.type.toLowerCase() === filter.toLowerCase()
  );

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "Paper": return <FileText className="w-4 h-4" />;
      case "Preprint": return <BookOpen className="w-4 h-4" />;
      case "Code": return <Code className="w-4 h-4" />;
      case "Dataset": return <Database className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Research Hub</h1>
          <p className="text-zinc-500 text-sm">A collaborative repository for SUST Physics research, code, and data.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-zinc-800 text-white rounded-xl text-sm font-bold border border-zinc-700 hover:bg-zinc-700 transition-colors">
            Submit Work
          </button>
        </div>
      </div>

      {/* Sub-navigation */}
      <div className="flex border-b border-zinc-800">
        {[
          { id: "repository", label: "Repository", icon: BookOpen },
          { id: "citation", label: "Citation Support", icon: Quote },
          { id: "collaboration", label: "Collaborative Research / Co-Author / RA Requisition", icon: UserPlus },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveSubTab(tab.id as any)}
            className={`flex items-center gap-2 px-6 py-4 text-xs font-bold uppercase tracking-widest transition-all relative ${
              activeSubTab === tab.id ? "text-white" : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
            {activeSubTab === tab.id && (
              <motion.div layoutId="research-tab-indicator" className="absolute bottom-0 left-0 right-0 h-0.5 bg-white" />
            )}
          </button>
        ))}
      </div>

      {activeSubTab === "repository" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Repository */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex flex-wrap gap-2">
            {["all", "paper", "preprint", "code", "dataset"].map((t) => (
              <button
                key={t}
                onClick={() => setFilter(t)}
                className={`px-4 py-2 rounded-xl text-xs font-bold border transition-all uppercase tracking-widest ${
                  filter === t 
                    ? "bg-white text-black border-white" 
                    : "bg-zinc-900 text-zinc-500 border-zinc-800 hover:border-zinc-600 hover:text-white"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 gap-4">
            {filteredItems.map((item) => (
              <motion.div
                key={item.id}
                layoutId={item.id}
                onClick={() => {
                  setSelectedItem(item);
                  fetchAiInsights(item);
                }}
                className={`p-6 rounded-3xl border cursor-pointer transition-all ${
                  selectedItem?.id === item.id 
                    ? "bg-zinc-800 border-orange-500/50 shadow-lg shadow-orange-500/5" 
                    : "bg-zinc-900 border-zinc-800 hover:border-zinc-700"
                }`}
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-2 px-3 py-1 bg-zinc-800 rounded-full border border-zinc-700 text-[10px] font-bold text-zinc-400 uppercase tracking-tighter">
                    {getTypeIcon(item.type)} {item.type}
                  </div>
                  <span className="text-xs font-mono text-zinc-600">{item.year}</span>
                </div>
                <h3 className="text-lg font-bold mb-2 group-hover:text-orange-500 transition-colors">{item.title}</h3>
                <p className="text-sm text-zinc-500 mb-4 line-clamp-2">{item.abstract}</p>
                <div className="flex flex-wrap gap-2">
                  {item.tags.map(tag => (
                    <span key={tag} className="text-[10px] font-mono text-zinc-600">#{tag.toUpperCase()}</span>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* AI Insights Sidebar */}
        <div className="space-y-6">
          <AnimatePresence mode="wait">
            {selectedItem ? (
              <motion.div
                key="insights"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="p-8 rounded-3xl bg-zinc-900 border border-zinc-800 sticky top-8"
              >
                <div className="flex items-center gap-2 text-orange-500 mb-6">
                  <Sparkles className="w-5 h-5" />
                  <h2 className="text-sm font-bold uppercase tracking-widest">AI Research Insights</h2>
                </div>

                {aiLoading ? (
                  <div className="space-y-8 animate-pulse">
                    <div className="h-32 bg-zinc-800 rounded-2xl" />
                    <div className="h-32 bg-zinc-800 rounded-2xl" />
                  </div>
                ) : (
                  <div className="space-y-8">
                    {/* Similar Work */}
                    <section>
                      <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                        <Zap className="w-3 h-3" /> Similar Work
                      </h3>
                      <div className="space-y-3">
                        {similarWork.map(work => (
                          <div key={work.id} className="p-4 rounded-2xl bg-zinc-800/50 border border-zinc-700/50 hover:border-zinc-600 transition-colors cursor-pointer group">
                            <h4 className="text-sm font-bold mb-1 group-hover:text-orange-500 transition-colors">{work.title}</h4>
                            <p className="text-[10px] text-zinc-500">{work.journal} • {work.year}</p>
                          </div>
                        ))}
                      </div>
                    </section>

                    {/* Collaborator Discovery */}
                    <section>
                      <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                        <Users className="w-3 h-3" /> Potential Collaborators
                      </h3>
                      <div className="space-y-3">
                        {collaborators.map(user => (
                          <div key={user.uid} className="flex items-center gap-3 p-3 rounded-2xl bg-zinc-800/50 border border-zinc-700/50">
                            <img src={user.photoURL} className="w-10 h-10 rounded-xl object-cover" referrerPolicy="no-referrer" />
                            <div>
                              <h4 className="text-sm font-bold">{user.displayName}</h4>
                              <p className="text-[10px] text-zinc-500">{user.currentIndustry} • Batch {user.batch}</p>
                            </div>
                            <button className="ml-auto p-2 text-zinc-500 hover:text-white">
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </div>
                        ))}
                      </div>
                    </section>

                    {/* Actions */}
                    <div className="pt-4 grid grid-cols-2 gap-3">
                      <a href={selectedItem.link} className="flex items-center justify-center gap-2 px-4 py-3 bg-white text-black rounded-2xl text-xs font-bold hover:scale-105 transition-transform">
                        Read Paper <ExternalLink className="w-3 h-3" />
                      </a>
                      {selectedItem.codeLink && (
                        <a href={selectedItem.codeLink} className="flex items-center justify-center gap-2 px-4 py-3 bg-zinc-800 text-white rounded-2xl text-xs font-bold border border-zinc-700 hover:bg-zinc-700 transition-colors">
                          View Code <Github className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  </div>
                )}
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-[400px] flex flex-col items-center justify-center text-center p-8 rounded-3xl border border-dashed border-zinc-800 text-zinc-600"
              >
                <Sparkles className="w-12 h-12 mb-4 opacity-20" />
                <p className="text-sm">Select a research item to discover similar work and potential collaborators through AI.</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    )}

      {activeSubTab === "citation" && (
        <div className="max-w-4xl space-y-8">
          <div className="p-8 bg-zinc-900 border border-zinc-800 rounded-3xl">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Quote className="w-5 h-5 text-orange-500" /> AI Citation Assistant
            </h2>
            <p className="text-zinc-500 text-sm mb-6">Upload your draft or paste your references to get AI-powered citation formatting and cross-referencing support.</p>
            <div className="space-y-4">
              <textarea 
                placeholder="Paste your abstract or references here..."
                className="w-full h-48 bg-zinc-950 border border-zinc-800 rounded-2xl p-4 text-sm text-white focus:border-zinc-600 outline-none transition-colors"
              />
              <button className="w-full py-4 bg-white text-black font-bold rounded-2xl hover:scale-[1.02] transition-transform">
                Generate Citations
              </button>
            </div>
          </div>
        </div>
      )}

      {activeSubTab === "collaboration" && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-8 bg-zinc-900 border border-zinc-800 rounded-3xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <UserPlus className="w-5 h-5 text-blue-500" /> Post a Requisition
              </h2>
              <p className="text-zinc-500 text-sm mb-6">Looking for a Co-Author or Research Assistant? Post your requirements here.</p>
              <button className="w-full py-4 bg-zinc-800 text-white font-bold rounded-2xl border border-zinc-700 hover:bg-zinc-700 transition-colors">
                Create Posting
              </button>
            </div>
            <div className="p-8 bg-zinc-900 border border-zinc-800 rounded-3xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Users className="w-5 h-5 text-green-500" /> Active Opportunities
              </h2>
              <p className="text-zinc-500 text-sm mb-6">Browse active research collaborations and RA positions within the community.</p>
              <button className="w-full py-4 bg-white text-black font-bold rounded-2xl hover:scale-[1.02] transition-transform">
                Browse Postings
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
