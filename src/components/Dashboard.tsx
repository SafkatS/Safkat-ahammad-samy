import React, { useState, useEffect } from "react";
import { motion } from "motion/react";
import { 
  Users, 
  Briefcase, 
  TrendingUp, 
  Zap, 
  ArrowUpRight, 
  MessageCircle,
  Globe,
  Award
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from "recharts";

const data = [
  { name: "2018", count: 400 },
  { name: "2019", count: 600 },
  { name: "2020", count: 800 },
  { name: "2021", count: 1200 },
  { name: "2022", count: 1500 },
  { name: "2023", count: 2100 },
  { name: "2024", count: 2800 },
];

export default function Dashboard({ profile }: { profile: any }) {
  const [stats, setStats] = useState<any>(null);
  const [suggestions, setSuggestions] = useState<any[]>([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsRes, suggRes] = await Promise.all([
          fetch("/api/stats"),
          fetch("/api/suggestions")
        ]);
        if (statsRes.ok) setStats(await statsRes.json());
        if (suggRes.ok) setSuggestions(await suggRes.json());
      } catch (e) {
        console.error("Failed to fetch dashboard data");
      }
    };
    fetchDashboardData();
  }, []);

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Hero Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div className="relative p-10 rounded-3xl bg-zinc-900 border border-zinc-800 overflow-hidden group">
            <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
              <Zap className="w-48 h-48 text-orange-500" />
            </div>
            <div className="relative z-10">
              <h1 className="text-4xl font-bold mb-4 tracking-tight">
                Welcome back, <span className="text-orange-500">{profile?.displayName?.split(" ")[0]}</span>.
              </h1>
              <p className="text-zinc-400 text-lg max-w-lg mb-8 leading-relaxed">
                SUST PHYSICS has identified <span className="text-white font-bold">3 new research collaborators</span> and <span className="text-white font-bold">2 career opportunities</span> matching your profile.
              </p>
              <div className="flex flex-wrap gap-4">
                <button className="px-6 py-3 bg-white text-black font-bold rounded-xl flex items-center gap-2 hover:scale-105 transition-transform">
                  View AI Matches <Zap className="w-4 h-4" />
                </button>
                <button className="px-6 py-3 bg-zinc-800 text-white font-bold rounded-xl border border-zinc-700 hover:bg-zinc-700 transition-colors">
                  Update Research Interests
                </button>
              </div>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-zinc-800">
              <div className="flex items-center justify-between mb-4">
                <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500">
                  <Users className="w-5 h-5" />
                </div>
                <span className="text-xs font-mono text-green-500">+12%</span>
              </div>
              <p className="text-zinc-500 text-xs uppercase tracking-widest font-mono mb-1">Network Size</p>
              <h3 className="text-2xl font-bold">{stats?.networkSize?.toLocaleString() || "4,281"}</h3>
            </div>
            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-zinc-800">
              <div className="flex items-center justify-between mb-4">
                <div className="p-2 bg-orange-500/10 rounded-lg text-orange-500">
                  <Briefcase className="w-5 h-5" />
                </div>
                <span className="text-xs font-mono text-green-500">+5</span>
              </div>
              <p className="text-zinc-500 text-xs uppercase tracking-widest font-mono mb-1">Active Jobs</p>
              <h3 className="text-2xl font-bold">{stats?.activeJobs || "142"}</h3>
            </div>
            <div className="p-6 rounded-2xl bg-zinc-900/50 border border-zinc-800">
              <div className="flex items-center justify-between mb-4">
                <div className="p-2 bg-purple-500/10 rounded-lg text-purple-500">
                  <Globe className="w-5 h-5" />
                </div>
                <span className="text-xs font-mono text-zinc-500">Global</span>
              </div>
              <p className="text-zinc-500 text-xs uppercase tracking-widest font-mono mb-1">Countries</p>
              <h3 className="text-2xl font-bold">{stats?.countries || "38"}</h3>
            </div>
          </div>
        </div>

        {/* AI Pulse Sidebar */}
        <div className="space-y-6">
          <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800">
            <h3 className="text-sm font-bold mb-6 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-orange-500" /> COMMUNITY PULSE
            </h3>
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <Area type="monotone" dataKey="count" stroke="#f97316" fillOpacity={1} fill="url(#colorCount)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 pt-4 border-t border-zinc-800 space-y-4">
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-500">Engagement Rate</span>
                <span className="font-bold">{stats?.engagementRate || 68}%</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-500">New Profiles (Weekly)</span>
                <span className="font-bold">+{stats?.newProfilesWeekly || 24}</span>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800">
            <h3 className="text-sm font-bold mb-4">QUICK ACTIONS</h3>
            <div className="space-y-3">
              <div className="p-4 bg-orange-500/5 border border-orange-500/20 rounded-xl mb-4">
                <p className="text-[10px] font-bold text-orange-500 uppercase tracking-widest mb-1">Your Referral UID</p>
                <div className="flex items-center justify-between">
                  <code className="text-sm font-mono text-white">{profile?.uid}</code>
                  <button 
                    onClick={() => navigator.clipboard.writeText(profile?.uid)}
                    className="text-[10px] text-zinc-500 hover:text-white transition-colors underline"
                  >
                    COPY
                  </button>
                </div>
                <p className="text-[8px] text-zinc-500 mt-2 italic">Share this with new alumni to verify their registration.</p>
              </div>
              <button className="w-full p-3 bg-zinc-800 hover:bg-zinc-700 rounded-xl text-xs font-bold flex items-center justify-between transition-colors">
                Post an Opportunity <ArrowUpRight className="w-4 h-4" />
              </button>
              <button className="w-full p-3 bg-zinc-800 hover:bg-zinc-700 rounded-xl text-xs font-bold flex items-center justify-between transition-colors">
                Share Research Preprint <ArrowUpRight className="w-4 h-4" />
              </button>
              <button className="w-full p-3 bg-zinc-800 hover:bg-zinc-700 rounded-xl text-xs font-bold flex items-center justify-between transition-colors">
                Sync LinkedIn Data <Zap className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Suggested Connections */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold tracking-tight">AI-SUGGESTED CONNECTIONS</h2>
          <button className="text-xs font-bold text-zinc-500 hover:text-white transition-colors">VIEW ALL</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {suggestions.map((person) => (
            <motion.div 
              key={person.uid}
              whileHover={{ y: -5 }}
              className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 group cursor-pointer"
            >
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-full bg-zinc-800 border border-zinc-700 flex items-center justify-center text-xl font-bold overflow-hidden">
                  {person.photoURL ? (
                    <img src={person.photoURL} alt={person.displayName} className="w-full h-full object-cover" />
                  ) : (
                    person.displayName[0]
                  )}
                </div>
                <div>
                  <h4 className="font-bold text-sm">{person.displayName}</h4>
                  <p className="text-[10px] text-zinc-500 font-mono">BATCH {person.batch}</p>
                </div>
              </div>
              <p className="text-xs text-zinc-400 mb-4 line-clamp-2">
                {person.currentIndustry} based in {person.location}.
              </p>
              <div className="flex items-center gap-2">
                <button className="flex-1 py-2 bg-zinc-800 hover:bg-white hover:text-black rounded-lg text-[10px] font-bold transition-all">
                  CONNECT
                </button>
                <button className="p-2 bg-zinc-800 hover:bg-[#25D366] hover:text-white rounded-lg transition-all">
                  <MessageCircle className="w-3 h-3" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
