import React, { useState } from "react";
import { motion } from "motion/react";
import { 
  User, 
  Mail, 
  GraduationCap, 
  Briefcase, 
  MapPin, 
  MessageCircle, 
  Linkedin, 
  Globe, 
  Save, 
  Zap,
  CheckCircle2,
  Plus
} from "lucide-react";

export default function Profile({ profile, onUpdate }: { profile: any, onUpdate: (p: any) => void }) {
  const [formData, setFormData] = useState(profile || {});
  const [isSaving, setIsSaving] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const [aiSummary, setAiSummary] = useState(profile?.aiSummary || "");
  const [isGenerating, setIsGenerating] = useState(false);

  const generateAIStory = async () => {
    setIsGenerating(true);
    try {
      const res = await fetch("/api/ai/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ profile: formData })
      });
      if (res.ok) {
        const data = await res.json();
        setAiSummary(data.summary);
        setFormData({ ...formData, aiSummary: data.summary });
      }
    } catch (e) {
      console.error("AI generation failed");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onUpdate(formData);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error("Error updating profile:", error);
    }
    setIsSaving(false);
  };

  const handleSkillAdd = (skill: string) => {
    if (!skill) return;
    const newSkills = [...(formData.skills || []), skill];
    setFormData({ ...formData, skills: newSkills });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-12">
      <div className="flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="flex items-center gap-8">
          <div className="relative group">
            <div className="w-32 h-32 rounded-3xl bg-zinc-800 border-2 border-zinc-700 flex items-center justify-center text-4xl font-bold overflow-hidden">
              {profile?.photoURL ? (
                <img src={profile.photoURL} alt="Profile" className="w-full h-full object-cover" />
              ) : (
                profile?.displayName?.[0]
              )}
            </div>
            <button className="absolute -bottom-2 -right-2 p-2 bg-white text-black rounded-xl shadow-xl hover:scale-110 transition-transform">
              <Plus className="w-4 h-4" />
            </button>
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight mb-2">{profile?.displayName}</h1>
            <p className="text-zinc-500 text-sm font-mono uppercase tracking-widest flex items-center gap-2">
              <GraduationCap className="w-4 h-4" /> BATCH {profile?.batch || "NOT SET"}
            </p>
          </div>
        </div>
        <div className="flex gap-4">
          <button 
            onClick={handleSave}
            disabled={isSaving}
            className="px-6 py-3 bg-white text-black font-bold rounded-xl flex items-center gap-2 hover:scale-105 transition-transform disabled:opacity-50"
          >
            {isSaving ? "SAVING..." : "SAVE PROFILE"} <Save className="w-4 h-4" />
          </button>
          <button className="px-6 py-3 bg-zinc-800 text-white font-bold rounded-xl border border-zinc-700 hover:bg-zinc-700 transition-colors flex items-center gap-2">
            SYNC LINKEDIN <Linkedin className="w-4 h-4" />
          </button>
        </div>
      </div>

      {showSuccess && (
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 bg-green-500/10 border border-green-500/20 rounded-xl text-green-500 text-sm flex items-center gap-3"
        >
          <CheckCircle2 className="w-5 h-5" /> Profile updated successfully.
        </motion.div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        {/* Academic & Professional */}
        <div className="space-y-8">
          <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest font-mono">Academic & Professional</h3>
          
          <div className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">SUST BATCH</label>
              <input 
                type="text" 
                placeholder="e.g. 2010-11"
                value={formData.batch}
                onChange={(e) => setFormData({ ...formData, batch: e.target.value })}
                className="w-full p-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">THESIS TOPIC</label>
              <input 
                type="text" 
                placeholder="e.g. Quantum Entanglement in 2D Systems"
                value={formData.thesisTopic}
                onChange={(e) => setFormData({ ...formData, thesisTopic: e.target.value })}
                className="w-full p-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">CURRENT INDUSTRY</label>
              <input 
                type="text" 
                placeholder="e.g. Data Science, Academia, Engineering"
                value={formData.currentIndustry}
                onChange={(e) => setFormData({ ...formData, currentIndustry: e.target.value })}
                className="w-full p-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">LOCATION</label>
              <input 
                type="text" 
                placeholder="e.g. Geneva, Switzerland"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                className="w-full p-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">CAREER ASPIRATIONS</label>
              <textarea 
                placeholder="Where do you see yourself in 5 years? What are you looking to achieve?"
                value={formData.aspirations}
                onChange={(e) => setFormData({ ...formData, aspirations: e.target.value })}
                className="w-full p-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors min-h-[100px] resize-none"
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">MENTORSHIP ROLE</label>
              <div className="flex gap-4">
                {["mentor", "mentee", "none"].map((role) => (
                  <button
                    key={role}
                    onClick={() => setFormData({ ...formData, mentorshipRole: role })}
                    className={`flex-1 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border transition-all ${
                      formData.mentorshipRole === role 
                        ? "bg-white text-black border-white" 
                        : "bg-zinc-900 text-zinc-500 border-zinc-800 hover:border-zinc-600"
                    }`}
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Contact & Social */}
        <div className="space-y-8">
          <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest font-mono">Contact & Social</h3>
          
          <div className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">WHATSAPP NUMBER</label>
              <div className="relative">
                <MessageCircle className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                <input 
                  type="text" 
                  placeholder="+880 1XXX XXXXXX"
                  value={formData.whatsapp}
                  onChange={(e) => setFormData({ ...formData, whatsapp: e.target.value })}
                  className="w-full pl-10 pr-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">LINKEDIN URL</label>
              <div className="relative">
                <Linkedin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                <input 
                  type="text" 
                  placeholder="linkedin.com/in/username"
                  value={formData.linkedIn}
                  onChange={(e) => setFormData({ ...formData, linkedIn: e.target.value })}
                  className="w-full pl-10 pr-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400">RESEARCHGATE URL</label>
              <div className="relative">
                <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                <input 
                  type="text" 
                  placeholder="researchgate.net/profile/username"
                  value={formData.researchGate}
                  onChange={(e) => setFormData({ ...formData, researchGate: e.target.value })}
                  className="w-full pl-10 pr-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
                />
              </div>
            </div>
          </div>

          <div className="pt-8">
            <h3 className="text-sm font-bold text-zinc-500 uppercase tracking-widest font-mono mb-4">Skill Cloud</h3>
            <div className="flex flex-wrap gap-2 mb-4">
              {(formData.skills || []).map((skill: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-zinc-800 border border-zinc-700 rounded-full text-[10px] text-zinc-400 flex items-center gap-2">
                  {skill}
                  <button onClick={() => {
                    const newSkills = formData.skills.filter((_: any, idx: number) => idx !== i);
                    setFormData({ ...formData, skills: newSkills });
                  }} className="hover:text-red-400">×</button>
                </span>
              ))}
            </div>
            <div className="flex gap-2">
              <input 
                type="text" 
                id="new-skill"
                placeholder="Add skill..."
                className="flex-1 p-2 bg-zinc-900 border border-zinc-800 rounded-lg text-xs focus:outline-none focus:border-zinc-600 transition-colors"
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSkillAdd((e.target as HTMLInputElement).value);
                    (e.target as HTMLInputElement).value = "";
                  }
                }}
              />
              <button 
                onClick={() => {
                  const input = document.getElementById("new-skill") as HTMLInputElement;
                  handleSkillAdd(input.value);
                  input.value = "";
                }}
                className="p-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* AI Summary Section */}
      <div className="p-8 rounded-3xl bg-zinc-900 border border-zinc-800 relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
          <Zap className="w-48 h-48 text-orange-500" />
        </div>
        <div className="relative z-10">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-orange-500" /> AI CAREER PATH NARRATIVE
          </h3>
          <p className="text-zinc-400 text-sm leading-relaxed max-w-2xl italic">
            {aiSummary || "Click below to generate your AI-powered career narrative based on your profile data."}
          </p>
          <button 
            onClick={generateAIStory}
            disabled={isGenerating}
            className="mt-6 text-xs font-bold text-orange-500 hover:text-orange-400 transition-colors uppercase tracking-widest disabled:opacity-50"
          >
            {isGenerating ? "GENERATING..." : "REGENERATE WITH GEMINI"}
          </button>
        </div>
      </div>
    </div>
  );
}
