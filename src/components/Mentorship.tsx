import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Users, 
  Zap, 
  MessageCircle, 
  ArrowRight, 
  Sparkles,
  GraduationCap,
  Target,
  Award,
  ChevronRight
} from "lucide-react";

interface MentorshipSuggestion {
  uid: string;
  score: number;
  reason: string;
  icebreaker: string;
  user: {
    displayName: string;
    currentIndustry: string;
    location: string;
    photoURL: string;
    skills: string[];
    batch: string;
    mentorshipRole: string;
  };
}

export default function Mentorship({ profile }: { profile: any }) {
  const [suggestions, setSuggestions] = useState<MentorshipSuggestion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const res = await fetch("/api/mentorship/suggestions");
        if (res.ok) {
          const data = await res.json();
          setSuggestions(data);
        }
      } catch (e) {
        console.error("Failed to fetch mentorship suggestions");
      } finally {
        setLoading(false);
      }
    };
    fetchSuggestions();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-4">
        <div className="w-12 h-12 border-4 border-orange-500/20 border-t-orange-500 rounded-full animate-spin" />
        <p className="font-mono text-xs uppercase tracking-widest text-zinc-500">SUST PHYSICS AI is matching mentors...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Mentorship Engine</h1>
          <p className="text-zinc-500 text-sm">AI-driven matching based on your skills, thesis, and career aspirations.</p>
        </div>
        <div className="flex items-center gap-3 px-4 py-2 bg-zinc-900 border border-zinc-800 rounded-xl">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs font-mono text-zinc-400 uppercase tracking-widest">
            You are a <span className="text-white font-bold">{profile?.mentorshipRole?.toUpperCase() || 'ALUMNI'}</span>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Matching Section */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-orange-500" />
            <h2 className="text-xl font-bold">Top SUST PHYSICS Matches</h2>
          </div>

          <AnimatePresence>
            {suggestions.map((match, idx) => (
              <motion.div
                key={match.uid}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="p-8 rounded-3xl bg-zinc-900 border border-zinc-800 hover:border-orange-500/30 transition-all group relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 p-6">
                  <div className="flex flex-col items-end">
                    <div className="flex items-center gap-2 px-3 py-1 bg-orange-500/10 text-orange-500 rounded-full border border-orange-500/20 text-[10px] font-bold mb-1">
                      <Zap className="w-3 h-3" /> {match.score}% COMPATIBILITY
                    </div>
                  </div>
                </div>

                <div className="flex flex-col md:flex-row gap-8">
                  <div className="shrink-0">
                    <img 
                      src={match.user.photoURL} 
                      alt={match.user.displayName}
                      className="w-20 h-20 rounded-2xl object-cover border-2 border-zinc-800 group-hover:border-orange-500/50 transition-colors"
                    />
                  </div>
                  
                  <div className="flex-1 space-y-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-xl font-bold">{match.user.displayName}</h3>
                        <span className="text-xs text-zinc-500 font-mono">Batch {match.user.batch}</span>
                      </div>
                      <p className="text-zinc-400 text-sm">{match.user.currentIndustry} • {match.user.location}</p>
                    </div>

                    <div className="p-4 rounded-2xl bg-zinc-950 border border-zinc-800/50">
                      <p className="text-sm text-zinc-300 leading-relaxed italic">
                        "{match.reason}"
                      </p>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {match.user.skills.slice(0, 3).map(skill => (
                        <span key={skill} className="px-3 py-1 bg-zinc-800 rounded-lg text-[10px] font-mono text-zinc-400">
                          {skill.toUpperCase()}
                        </span>
                      ))}
                    </div>

                    <div className="pt-4 flex flex-col sm:flex-row items-center gap-4">
                      <button className="w-full sm:w-auto px-6 py-3 bg-white text-black font-bold rounded-xl text-sm flex items-center justify-center gap-2 hover:scale-105 transition-transform">
                        Connect on WhatsApp <MessageCircle className="w-4 h-4" />
                      </button>
                      <button className="w-full sm:w-auto px-6 py-3 bg-zinc-800 text-white font-bold rounded-xl text-sm flex items-center justify-center gap-2 hover:bg-zinc-700 transition-colors">
                        View Profile <ArrowRight className="w-4 h-4" />
                      </button>
                    </div>

                    <div className="mt-4 pt-4 border-t border-zinc-800/50">
                      <p className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold mb-2">Suggested Icebreaker</p>
                      <p className="text-xs text-zinc-400 bg-zinc-800/30 p-3 rounded-lg border border-zinc-800/50">
                        {match.icebreaker}
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-6">
          <div className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-orange-500" />
              Your Mentorship Goal
            </h3>
            <p className="text-sm text-zinc-400 leading-relaxed mb-6">
              {profile?.aspirations || "Update your profile aspirations to get more accurate AI matches."}
            </p>
            <button className="w-full py-3 bg-zinc-800 text-white text-xs font-bold rounded-xl hover:bg-zinc-700 transition-colors uppercase tracking-widest">
              Edit Aspirations
            </button>
          </div>

          <div className="p-6 rounded-3xl bg-gradient-to-br from-orange-500/10 to-transparent border border-orange-500/20">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Award className="w-5 h-5 text-orange-500" />
              SUST PHYSICS Insights
            </h3>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-orange-500/20 flex items-center justify-center shrink-0">
                  <ChevronRight className="w-4 h-4 text-orange-500" />
                </div>
                <p className="text-xs text-zinc-400">Alumni in <span className="text-white">Quantum Computing</span> are currently the most active mentors.</p>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-orange-500/20 flex items-center justify-center shrink-0">
                  <ChevronRight className="w-4 h-4 text-orange-500" />
                </div>
                <p className="text-xs text-zinc-400">Your <span className="text-white">Nonlinear Optics</span> background is highly sought after by 4 mentees.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
