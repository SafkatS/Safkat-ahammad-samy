import React, { useState, useEffect } from "react";
import { 
  LayoutDashboard, 
  Users, 
  Briefcase, 
  BookOpen, 
  GraduationCap, 
  Settings, 
  LogOut, 
  Bell,
  MessageCircle,
  Calendar,
  Map as MapIcon,
  Search,
  Menu,
  X,
  ChevronRight,
  Shield
} from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import Dashboard from "./components/Dashboard";
import Directory from "./components/Directory";
import Opportunities from "./components/Opportunities";
import Profile from "./components/Profile";
import ResearchHub from "./components/ResearchHub";
import Mentorship from "./components/Mentorship";
import Auth from "./components/Auth";
import Notice from "./components/Notice";
import Events from "./components/Events";
import Sponsor from "./components/Sponsor";
import Newsletter from "./components/Newsletter";
import AdminPanel from "./components/AdminPanel";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function App() {
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const checkSession = async () => {
      try {
        const res = await fetch("/api/auth/session");
        if (res.ok) {
          const data = await res.json();
          setUser(data.user);
          setProfile(data.profile);
        }
      } catch (e) {
        console.error("Session check failed");
      } finally {
        setLoading(false);
      }
    };
    checkSession();
  }, []);

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    setUser(null);
    setProfile(null);
  };

  const updateProfile = async (newProfile: any) => {
    const res = await fetch("/api/profile", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newProfile)
    });
    if (res.ok) {
      setProfile(newProfile);
    }
  };

  if (loading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-zinc-950 text-white font-mono">
        <motion.div 
          animate={{ opacity: [0.4, 1, 0.4] }} 
          transition={{ duration: 1.5, repeat: Infinity }}
          className="text-xl tracking-widest"
        >
          INITIALIZING SUST_PHYSICS_AGENT...
        </motion.div>
      </div>
    );
  }

  if (!user) {
    return <Auth onLogin={(u) => { setUser(u); setProfile(u); }} />;
  }

  const navItems = [
    { id: "dashboard", label: "Pulse", icon: LayoutDashboard },
    { id: "directory", label: "Directory", icon: MapIcon },
    { id: "opportunities", label: "Opportunities", icon: Briefcase },
    { id: "research", label: "Research", icon: BookOpen },
    { id: "mentorship", label: "Mentorship", icon: GraduationCap },
    { id: "notice", label: "Notice", icon: Bell },
    { id: "events", label: "Events", icon: Calendar },
    { id: "sponsor", label: "Find a Sponsor", icon: MapIcon },
    { id: "newsletter", label: "Newsletter", icon: MessageCircle },
    { id: "profile", label: "Profile", icon: Settings },
  ];

  if (profile?.role === "admin") {
    navItems.splice(navItems.length - 1, 0, { id: "admin", label: "Admin", icon: Shield });
  }

  return (
    <div className="h-screen w-full flex bg-zinc-950 text-zinc-100 overflow-hidden">
      {/* Sidebar */}
      <motion.aside 
        animate={{ width: isSidebarOpen ? 280 : 80 }}
        className="border-r border-zinc-800 bg-zinc-900/30 flex flex-col z-30"
      >
        <div className="p-6 flex items-center justify-between">
          {isSidebarOpen && (
            <span className="font-bold tracking-tighter text-xl">SUST PHYSICS</span>
          )}
          <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="p-1 hover:bg-zinc-800 rounded">
            {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        <nav className="flex-1 px-4 space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center gap-4 p-3 rounded-xl transition-all group",
                activeTab === item.id 
                  ? "bg-white text-black" 
                  : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
              )}
            >
              <item.icon className="w-5 h-5 shrink-0" />
              {isSidebarOpen && <span className="font-medium">{item.label}</span>}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-zinc-800">
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-4 p-3 text-zinc-400 hover:text-red-400 transition-colors"
          >
            <LogOut className="w-5 h-5 shrink-0" />
            {isSidebarOpen && <span className="font-medium">Sign Out</span>}
          </button>
          {isSidebarOpen && (
            <div className="mt-4 px-3 text-[10px] text-zinc-600 font-mono uppercase tracking-tighter">
              Copy right, developed by Honestime Inc.
            </div>
          )}
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        {/* Header */}
        <header className="h-16 border-bottom border-zinc-800 flex items-center justify-between px-8 bg-zinc-950/50 backdrop-blur-md z-20">
          <div className="flex items-center gap-4">
            <h2 className="text-sm font-mono text-zinc-500 uppercase tracking-widest">
              {navItems.find(n => n.id === activeTab)?.label}
            </h2>
          </div>
          <div className="flex items-center gap-6">
            <div className="relative hidden md:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
              <input 
                type="text" 
                placeholder="Search alumni, papers, jobs..." 
                className="pl-10 pr-4 py-2 bg-zinc-900 border border-zinc-800 rounded-full text-sm focus:outline-none focus:border-zinc-600 transition-colors w-64"
              />
            </div>
            <button className="relative p-2 text-zinc-400 hover:text-white transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-2 right-2 w-2 h-2 bg-orange-500 rounded-full border-2 border-zinc-950" />
            </button>
            <div className="flex items-center gap-3 pl-4 border-l border-zinc-800">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-bold">{user.displayName}</p>
                <p className="text-[10px] text-zinc-500 font-mono uppercase tracking-tighter">{profile?.role || "ALUMNI"}</p>
              </div>
              <img 
                src={user.photoURL} 
                alt="Profile" 
                className="w-8 h-8 rounded-full border border-zinc-700" 
                referrerPolicy="no-referrer"
              />
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {activeTab === "dashboard" && <Dashboard profile={profile} />}
              {activeTab === "directory" && <Directory />}
              {activeTab === "opportunities" && <Opportunities />}
              {activeTab === "profile" && <Profile profile={profile} onUpdate={updateProfile} />}
              {activeTab === "research" && <ResearchHub />}
              {activeTab === "mentorship" && <Mentorship profile={profile} />}
              {activeTab === "notice" && <Notice />}
              {activeTab === "events" && <Events />}
              {activeTab === "sponsor" && <Sponsor />}
              {activeTab === "newsletter" && <Newsletter />}
              {activeTab === "admin" && <AdminPanel />}
            </motion.div>
          </AnimatePresence>
          <footer className="mt-12 pt-8 border-t border-zinc-900 text-center pb-8">
            <p className="text-[10px] text-zinc-600 font-mono uppercase tracking-widest">
              Copy right, developed by Honestime Inc.
            </p>
          </footer>
        </div>

        {/* Floating WhatsApp Action */}
        <button className="fixed bottom-8 right-8 w-14 h-14 bg-[#25D366] text-white rounded-full flex items-center justify-center shadow-2xl hover:scale-110 transition-transform z-50 group">
          <MessageCircle className="w-6 h-6" />
          <span className="absolute right-full mr-4 px-3 py-1 bg-zinc-900 border border-zinc-800 text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
            SUST PHYSICS WhatsApp Bot
          </span>
        </button>
      </main>
    </div>
  );
}
