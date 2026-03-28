import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  ShieldCheck, 
  Mail, 
  User, 
  Users, 
  ArrowRight, 
  Lock, 
  CheckCircle2,
  AlertCircle,
  Loader2,
  Phone,
  Smartphone,
  Linkedin
} from "lucide-react";

interface AuthProps {
  onLogin: (user: any) => void;
}

export default function Auth({ onLogin }: AuthProps) {
  const [mode, setMode] = useState<"login" | "signup" | "verify">("login");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [method, setMethod] = useState<"email" | "sms">("email");
  const [displayName, setDisplayName] = useState("");
  const [batch, setBatch] = useState("");
  const [referralUid, setReferralUid] = useState("");
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [referralName, setReferralName] = useState("");

  const handleReferralCheck = async (uid: string) => {
    setReferralUid(uid);
    if (uid.length > 5) {
      try {
        const res = await fetch(`/api/auth/referral-check/${uid}`);
        if (res.ok) {
          const data = await res.json();
          setReferralName(data.name);
        } else {
          setReferralName("");
        }
      } catch (e) {
        setReferralName("");
      }
    }
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, phone, displayName, batch, referralUid, method })
      });
      const data = await res.json();
      if (res.ok) {
        setMode("verify");
      } else {
        setError(data.error);
      }
    } catch (e) {
      setError("Signup failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, phone, otp, method })
      });
      const data = await res.json();
      if (res.ok) {
        onLogin(data.user);
      } else {
        setError(data.error);
      }
    } catch (e) {
      setError("Verification failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      if (res.ok) {
        onLogin(data.user);
      } else {
        setError(data.error);
      }
    } catch (e) {
      setError("Login failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleLinkedInLogin = async () => {
    try {
      const res = await fetch("/api/auth/linkedin/url");
      const { url } = await res.json();
      window.open(url, "linkedin_oauth", "width=600,height=600");
    } catch (e) {
      setError("Failed to initiate LinkedIn login");
    }
  };

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === 'OAUTH_AUTH_SUCCESS') {
        // Refresh session or fetch user
        fetch("/api/auth/session")
          .then(res => res.json())
          .then(data => {
            if (data.user) onLogin(data.user);
          });
      }
    };
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [onLogin]);

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-12">
          <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center mx-auto mb-6">
            <ShieldCheck className="w-8 h-8 text-black" />
          </div>
          <h1 className="text-3xl font-bold tracking-tighter text-white mb-2">SUST PHYSICS Auth</h1>
          <p className="text-zinc-500 text-sm">SUST Physics Alumni Verification System</p>
        </div>

        <motion.div 
          layout
          className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 shadow-2xl"
        >
          <AnimatePresence mode="wait">
            {mode === "login" && (
              <motion.form
                key="login"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                onSubmit={handleLogin}
                className="space-y-6"
              >
                <div className="grid grid-cols-3 gap-2">
                  <button 
                    type="button"
                    onClick={() => onLogin({ uid: "google-user", displayName: "Google User", email: "google@gmail.com", batch: "2020-21", currentIndustry: "Tech", location: "Global", skills: [], aspirations: "", mentorshipRole: "mentee", role: "alumni", isPublic: true, photoURL: "https://www.google.com/favicon.ico" })}
                    className="py-3 bg-zinc-800 text-white text-[10px] font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-zinc-700 transition-colors"
                  >
                    <img src="https://www.google.com/favicon.ico" className="w-3 h-3" alt="Google" /> GOOGLE
                  </button>
                  <button 
                    type="button"
                    onClick={() => onLogin({ uid: "fb-user", displayName: "FB User", email: "fb@facebook.com", batch: "2019-20", currentIndustry: "Social Media", location: "Global", skills: [], aspirations: "", mentorshipRole: "mentee", role: "alumni", isPublic: true, photoURL: "https://www.facebook.com/favicon.ico" })}
                    className="py-3 bg-zinc-800 text-white text-[10px] font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-zinc-700 transition-colors"
                  >
                    <img src="https://www.facebook.com/favicon.ico" className="w-3 h-3" alt="Facebook" /> FB
                  </button>
                  <button 
                    type="button"
                    onClick={handleLinkedInLogin}
                    className="py-3 bg-zinc-800 text-white text-[10px] font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-zinc-700 transition-colors"
                  >
                    <Linkedin className="w-3 h-3 text-[#0077B5]" /> LINKEDIN
                  </button>
                </div>

                <div className="relative py-4">
                  <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-zinc-800"></div></div>
                  <div className="relative flex justify-center text-[10px] uppercase font-bold tracking-widest"><span className="bg-zinc-900 px-2 text-zinc-600">Or continue with email</span></div>
                </div>

                <div>
                  <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Email Address</label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                    <input 
                      type="email" 
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="alumni@sust.edu"
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-3 pl-12 pr-4 text-sm text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                </div>
                {error && (
                  <div className="flex items-center gap-2 text-red-500 text-xs bg-red-500/10 p-3 rounded-xl border border-red-500/20">
                    <AlertCircle className="w-4 h-4" /> {error}
                  </div>
                )}
                <button 
                  disabled={loading}
                  className="w-full py-4 bg-white text-black font-bold rounded-xl flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50"
                >
                  {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Sign In"}
                </button>
                <p className="text-center text-xs text-zinc-500">
                  Don't have an account?{" "}
                  <button type="button" onClick={() => setMode("signup")} className="text-white font-bold hover:underline">Register</button>
                </p>
              </motion.form>
            )}

            {mode === "signup" && (
              <motion.form
                key="signup"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                onSubmit={handleSignup}
                className="space-y-4"
              >
                <div className="grid grid-cols-3 gap-2">
                  <button 
                    type="button"
                    onClick={() => onLogin({ uid: "google-user", displayName: "Google User", email: "google@gmail.com", batch: "2020-21", currentIndustry: "Tech", location: "Global", skills: [], aspirations: "", mentorshipRole: "mentee", role: "alumni", isPublic: true, photoURL: "https://www.google.com/favicon.ico" })}
                    className="py-3 bg-zinc-800 text-white text-[10px] font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-zinc-700 transition-colors"
                  >
                    <img src="https://www.google.com/favicon.ico" className="w-3 h-3" alt="Google" /> GOOGLE
                  </button>
                  <button 
                    type="button"
                    onClick={() => onLogin({ uid: "fb-user", displayName: "FB User", email: "fb@facebook.com", batch: "2019-20", currentIndustry: "Social Media", location: "Global", skills: [], aspirations: "", mentorshipRole: "mentee", role: "alumni", isPublic: true, photoURL: "https://www.facebook.com/favicon.ico" })}
                    className="py-3 bg-zinc-800 text-white text-[10px] font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-zinc-700 transition-colors"
                  >
                    <img src="https://www.facebook.com/favicon.ico" className="w-3 h-3" alt="Facebook" /> FB
                  </button>
                  <button 
                    type="button"
                    onClick={handleLinkedInLogin}
                    className="py-3 bg-zinc-800 text-white text-[10px] font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-zinc-700 transition-colors"
                  >
                    <Linkedin className="w-3 h-3 text-[#0077B5]" /> LINKEDIN
                  </button>
                </div>

                <div className="relative py-2">
                  <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-zinc-800"></div></div>
                  <div className="relative flex justify-center text-[10px] uppercase font-bold tracking-widest"><span className="bg-zinc-900 px-2 text-zinc-600">Or sign up with details</span></div>
                </div>

                <div>
                  <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                    <input 
                      type="text" 
                      required
                      value={displayName}
                      onChange={(e) => setDisplayName(e.target.value)}
                      placeholder="John Doe"
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-3 pl-12 pr-4 text-sm text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Email Address</label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                    <input 
                      type="email" 
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="alumni@sust.edu"
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-3 pl-12 pr-4 text-sm text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Phone Number</label>
                  <div className="relative">
                    <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
                    <input 
                      type="tel" 
                      required
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+880 1XXX XXXXXX"
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-3 pl-12 pr-4 text-sm text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Verification Method</label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => setMethod("email")}
                      className={`flex-1 py-3 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition-all ${method === "email" ? "bg-white text-black border-white" : "bg-zinc-900 text-zinc-500 border-zinc-800"}`}
                    >
                      <Mail className="w-4 h-4" /> EMAIL
                    </button>
                    <button
                      type="button"
                      onClick={() => setMethod("sms")}
                      className={`flex-1 py-3 rounded-xl border text-xs font-bold flex items-center justify-center gap-2 transition-all ${method === "sms" ? "bg-white text-black border-white" : "bg-zinc-900 text-zinc-500 border-zinc-800"}`}
                    >
                      <Smartphone className="w-4 h-4" /> SMS
                    </button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Batch</label>
                    <input 
                      type="text" 
                      required
                      value={batch}
                      onChange={(e) => setBatch(e.target.value)}
                      placeholder="2012-13"
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-3 px-4 text-sm text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Referral UID</label>
                    <input 
                      type="text" 
                      value={referralUid}
                      onChange={(e) => handleReferralCheck(e.target.value)}
                      placeholder="Optional"
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-3 px-4 text-sm text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                </div>
                {referralName && (
                  <div className="flex items-center gap-2 text-green-500 text-[10px] font-bold uppercase tracking-widest">
                    <CheckCircle2 className="w-3 h-3" /> Referred by: {referralName}
                  </div>
                )}
                {error && (
                  <div className="flex items-center gap-2 text-red-500 text-xs bg-red-500/10 p-3 rounded-xl border border-red-500/20">
                    <AlertCircle className="w-4 h-4" /> {error}
                  </div>
                )}
                <button 
                  disabled={loading}
                  className="w-full py-4 bg-white text-black font-bold rounded-xl flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50"
                >
                  {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Request Verification"}
                </button>
                <p className="text-center text-xs text-zinc-500">
                  Already verified?{" "}
                  <button type="button" onClick={() => setMode("login")} className="text-white font-bold hover:underline">Sign In</button>
                </p>
              </motion.form>
            )}

            {mode === "verify" && (
              <motion.form
                key="verify"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                onSubmit={handleVerify}
                className="space-y-6"
              >
                <div className="text-center">
                  <p className="text-sm text-zinc-400 mb-6">
                    We've sent a 6-digit verification code to your <span className="text-white font-bold">{method === "sms" ? "mobile via SMS" : "email"}</span>
                    <br />
                    <span className="text-xs text-zinc-500">({method === "sms" ? phone : email})</span>
                  </p>
                  <div className="flex justify-center gap-3">
                    <input 
                      type="text" 
                      required
                      maxLength={6}
                      value={otp}
                      onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
                      placeholder="000000"
                      className="w-48 bg-zinc-950 border border-zinc-800 rounded-xl py-4 text-center text-2xl font-bold tracking-[0.5em] text-white focus:border-white transition-colors outline-none"
                    />
                  </div>
                </div>
                {error && (
                  <div className="flex items-center gap-2 text-red-500 text-xs bg-red-500/10 p-3 rounded-xl border border-red-500/20">
                    <AlertCircle className="w-4 h-4" /> {error}
                  </div>
                )}
                <button 
                  disabled={loading}
                  className="w-full py-4 bg-white text-black font-bold rounded-xl flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50"
                >
                  {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify & Complete"}
                </button>
                <p className="text-center text-xs text-zinc-500">
                  Didn't get the code?{" "}
                  <button type="button" onClick={() => setMode("signup")} className="text-white font-bold hover:underline">Try Again</button>
                </p>
              </motion.form>
            )}
          </AnimatePresence>
        </motion.div>

        <div className="mt-8 flex items-center justify-center gap-8 opacity-30 grayscale">
          <img src="https://upload.wikimedia.org/wikipedia/en/2/23/Shahjalal_University_of_Science_and_Technology_logo.png" alt="SUST Logo" className="h-12" />
        </div>
      </div>
    </div>
  );
}
