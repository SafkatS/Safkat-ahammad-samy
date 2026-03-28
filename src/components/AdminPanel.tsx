import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Shield, 
  Users, 
  Briefcase, 
  FileText, 
  Settings, 
  Activity, 
  Trash2, 
  CheckCircle, 
  XCircle,
  Search,
  MoreVertical,
  Mail,
  Calendar,
  AlertCircle
} from "lucide-react";

interface AdminStats {
  totalUsers: number;
  activeOpportunities: number;
  researchPapers: number;
  pendingVerifications: number;
  systemStatus: string;
  lastAiUpdate: string;
}

interface UserProfile {
  uid: string;
  displayName: string;
  email: string;
  batch: string;
  role: string;
  isPublic: boolean;
  photoURL: string;
}

export default function AdminPanel() {
  const [activeTab, setActiveTab] = useState<"dashboard" | "users" | "content" | "settings">("dashboard");
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const [statsRes, usersRes] = await Promise.all([
          fetch("/api/admin/stats"),
          fetch("/api/admin/users")
        ]);
        
        if (statsRes.ok && usersRes.ok) {
          const statsData = await statsRes.json();
          const usersData = await usersRes.json();
          setStats(statsData);
          setUsers(usersData);
        }
      } catch (error) {
        console.error("Failed to fetch admin data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAdminData();
  }, []);

  const handleDeleteUser = async (uid: string) => {
    if (!confirm("Are you sure you want to delete this user? This action cannot be undone.")) return;
    
    try {
      const res = await fetch(`/api/admin/users/${uid}`, { method: "DELETE" });
      if (res.ok) {
        setUsers(users.filter(u => u.uid !== uid));
      }
    } catch (error) {
      console.error("Failed to delete user:", error);
    }
  };

  const handleUpdateRole = async (uid: string, newRole: string) => {
    try {
      const res = await fetch(`/api/admin/users/${uid}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role: newRole })
      });
      if (res.ok) {
        setUsers(users.map(u => u.uid === uid ? { ...u, role: newRole } : u));
      }
    } catch (error) {
      console.error("Failed to update role:", error);
    }
  };

  const filteredUsers = users.filter(u => 
    u.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2 flex items-center gap-3">
            <Shield className="w-8 h-8 text-orange-500" />
            Admin Control Center
          </h1>
          <p className="text-zinc-500 text-sm font-mono uppercase tracking-widest">Platform Management & Governance</p>
        </div>
        <div className="flex bg-zinc-900 border border-zinc-800 rounded-xl p-1">
          {[
            { id: "dashboard", icon: Activity, label: "STATS" },
            { id: "users", icon: Users, label: "USERS" },
            { id: "content", icon: FileText, label: "CONTENT" },
            { id: "settings", icon: Settings, label: "CONFIG" }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-[10px] font-bold transition-all ${
                activeTab === tab.id ? "bg-white text-black" : "text-zinc-500 hover:text-white"
              }`}
            >
              <tab.icon className="w-3 h-3" />
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === "dashboard" && (
          <motion.div
            key="dashboard"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {[
              { label: "Total Members", value: stats?.totalUsers, icon: Users, color: "text-blue-500" },
              { label: "Active Opps", value: stats?.activeOpportunities, icon: Briefcase, color: "text-green-500" },
              { label: "Research Assets", value: stats?.researchPapers, icon: FileText, color: "text-purple-500" },
              { label: "System Health", value: stats?.systemStatus, icon: Activity, color: "text-orange-500" }
            ].map((item, i) => (
              <div key={i} className="p-6 bg-zinc-900 border border-zinc-800 rounded-2xl">
                <div className="flex items-center justify-between mb-4">
                  <item.icon className={`w-6 h-6 ${item.color}`} />
                  <span className="text-[10px] font-mono text-zinc-600 uppercase tracking-widest">Real-time</span>
                </div>
                <div className="space-y-1">
                  <p className="text-2xl font-bold text-white">{item.value}</p>
                  <p className="text-xs text-zinc-500">{item.label}</p>
                </div>
              </div>
            ))}

            <div className="md:col-span-2 p-6 bg-zinc-900 border border-zinc-800 rounded-2xl relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <Shield className="w-32 h-32" />
              </div>
              <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-orange-500" />
                System Overview
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-zinc-500">Last AI Agent Sync</span>
                  <span className="text-zinc-300 font-mono">{new Date(stats?.lastAiUpdate || "").toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-zinc-500">Database Engine</span>
                  <span className="text-zinc-300 font-mono">MockDB v1.0 (In-Memory)</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-zinc-500">Platform Version</span>
                  <span className="text-zinc-300 font-mono">v2.4.0-stable</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === "users" && (
          <motion.div
            key="users"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
              <input 
                type="text" 
                placeholder="Search users by name or email..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-sm focus:outline-none focus:border-zinc-600 transition-colors"
              />
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-zinc-800 bg-zinc-950/50">
                    <th className="px-6 py-4 text-[10px] font-mono text-zinc-500 uppercase tracking-widest">User</th>
                    <th className="px-6 py-4 text-[10px] font-mono text-zinc-500 uppercase tracking-widest">Batch</th>
                    <th className="px-6 py-4 text-[10px] font-mono text-zinc-500 uppercase tracking-widest">Role</th>
                    <th className="px-6 py-4 text-[10px] font-mono text-zinc-500 uppercase tracking-widest">Status</th>
                    <th className="px-6 py-4 text-[10px] font-mono text-zinc-500 uppercase tracking-widest text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr key={user.uid} className="border-b border-zinc-800 hover:bg-zinc-800/30 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <img src={user.photoURL} className="w-8 h-8 rounded-lg object-cover border border-zinc-700" alt="" />
                          <div>
                            <p className="text-sm font-bold text-white">{user.displayName}</p>
                            <p className="text-[10px] text-zinc-500">{user.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-xs text-zinc-400 font-mono">{user.batch}</td>
                      <td className="px-6 py-4">
                        <select 
                          value={user.role}
                          onChange={(e) => handleUpdateRole(user.uid, e.target.value)}
                          className="bg-zinc-800 border border-zinc-700 text-[10px] text-zinc-300 rounded-lg px-2 py-1 focus:outline-none"
                        >
                          <option value="alumni">Alumni</option>
                          <option value="student">Student</option>
                          <option value="admin">Admin</option>
                        </select>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full text-[8px] font-bold uppercase tracking-widest ${
                          user.isPublic ? "bg-green-500/10 text-green-500" : "bg-zinc-800 text-zinc-500"
                        }`}>
                          {user.isPublic ? "Visible" : "Hidden"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <button 
                            onClick={() => handleDeleteUser(user.uid)}
                            className="p-2 text-zinc-500 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                          <button className="p-2 text-zinc-500 hover:text-white hover:bg-zinc-800 rounded-lg transition-all">
                            <MoreVertical className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        )}

        {(activeTab === "content" || activeTab === "settings") && (
          <motion.div
            key="placeholder"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center h-[40vh] text-center space-y-4"
          >
            <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-full">
              <Settings className="w-8 h-8 text-zinc-700 animate-spin-slow" />
            </div>
            <div className="space-y-1">
              <p className="text-sm font-bold text-white">Module Under Construction</p>
              <p className="text-xs text-zinc-500">This management interface is being prepared for the next release.</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
