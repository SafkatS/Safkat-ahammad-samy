import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import axios from "axios";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

import { summarizeProfile, matchOpportunity, fetchNewOpportunities, matchMentorship } from "./src/services/geminiService";

// Mock Database
let users: Record<string, any> = {
  "demo-user": {
    uid: "demo-user",
    displayName: "Demo Alumni",
    email: "alumni@sust.edu",
    batch: "2012-13",
    thesisTopic: "Nonlinear Optics",
    currentIndustry: "Data Science",
    location: "Mountain View, USA",
    lat: 37.3861,
    lng: -122.0839,
    whatsapp: "+1234567890",
    skills: ["Python", "Physics", "Machine Learning"],
    aspirations: "Transitioning into Quantum Machine Learning and seeking leadership roles in tech.",
    mentorshipRole: "mentee",
    role: "admin",
    isPublic: true,
    photoURL: "https://picsum.photos/seed/alumni/200",
  },
  "alumni-2": {
    uid: "alumni-2",
    displayName: "Dr. Sarah Ahmed",
    email: "sarah@cern.ch",
    batch: "2008-09",
    thesisTopic: "Higgs Boson Decay",
    currentIndustry: "Research",
    location: "Geneva, Switzerland",
    lat: 46.2044,
    lng: 6.1432,
    whatsapp: "+411234567",
    skills: ["Particle Physics", "C++", "Data Analysis", "Mentoring"],
    aspirations: "Contributing to large-scale international research collaborations and mentoring young physicists.",
    mentorshipRole: "mentor",
    role: "alumni",
    isPublic: true,
    photoURL: "https://picsum.photos/seed/sarah/200"
  },
  "alumni-3": {
    uid: "alumni-3",
    displayName: "Tanvir Rahman",
    email: "tanvir@intel.com",
    batch: "2010-11",
    thesisTopic: "Semiconductor Physics",
    currentIndustry: "Hardware Engineering",
    location: "Hillsboro, USA",
    lat: 45.5231,
    lng: -122.9898,
    whatsapp: "+1503987654",
    skills: ["VLSI", "Photonics", "Team Leadership"],
    aspirations: "Leading hardware innovation at Intel and helping juniors navigate the semiconductor industry.",
    mentorshipRole: "mentor",
    role: "alumni",
    isPublic: true,
    photoURL: "https://picsum.photos/seed/tanvir/200"
  },
  "alumni-4": {
    uid: "alumni-4",
    displayName: "Nusrat Jahan",
    email: "nusrat@phd.ethz.ch",
    batch: "2018-19",
    thesisTopic: "Quantum Computing",
    currentIndustry: "Academia",
    location: "Zurich, Switzerland",
    lat: 47.3769,
    lng: 8.5417,
    whatsapp: "+4178123456",
    skills: ["Quantum Algorithms", "Qiskit", "Research"],
    aspirations: "Completing PhD and moving into industrial quantum research. Looking for guidance on industry transitions.",
    mentorshipRole: "mentee",
    role: "alumni",
    isPublic: true,
    photoURL: "https://picsum.photos/seed/nusrat/200"
  },
  "alumni-5": {
    uid: "alumni-5",
    displayName: "Fahim Shahriar",
    email: "fahim@google.com",
    batch: "2014-15",
    thesisTopic: "Computational Physics",
    currentIndustry: "Software Engineering",
    location: "London, UK",
    lat: 51.5074,
    lng: -0.1278,
    whatsapp: "+44771234567",
    skills: ["Go", "Distributed Systems", "Cloud Computing"],
    aspirations: "Scaling global infrastructure at Google. Interested in mentoring those switching from physics to software.",
    mentorshipRole: "mentor",
    role: "alumni",
    isPublic: true,
    photoURL: "https://picsum.photos/seed/fahim/200"
  },
  "alumni-6": {
    uid: "alumni-6",
    displayName: "M. Rahman",
    email: "rahman@sust.edu",
    batch: "2015-16",
    thesisTopic: "Atmospheric Physics",
    currentIndustry: "Academia",
    location: "Sylhet, Bangladesh",
    lat: 24.8949,
    lng: 91.8687,
    whatsapp: "+8801712345678",
    skills: ["Meteorology", "Data Analysis", "Teaching"],
    aspirations: "Advancing atmospheric research in Bangladesh and improving weather prediction models.",
    mentorshipRole: "mentor",
    role: "alumni",
    isPublic: true,
    photoURL: "https://picsum.photos/seed/rahman/200"
  }
};

let lastAiUpdate = new Date().toISOString();
let aiAgentStatus = "Idle";

let pendingUsers: Record<string, any> = {};
let otps: Record<string, string> = {};

let opportunities = [
  // 20 Research Options from Real World
  {
    id: "res-1",
    title: "Postdoctoral Researcher in Quantum Information",
    company: "University of Waterloo",
    location: "Waterloo, Canada",
    type: "Research",
    matchScore: 92,
    postedAt: "2 days ago",
    description: "Work on quantum error correction and fault-tolerant quantum computing.",
    tags: ["Quantum", "PostDoc", "Physics"]
  },
  {
    id: "res-2",
    title: "Research Scientist: Condensed Matter",
    company: "Max Planck Institute",
    location: "Stuttgart, Germany",
    type: "Research",
    matchScore: 88,
    postedAt: "5 days ago",
    description: "Investigate topological insulators and superconducting materials.",
    tags: ["Condensed Matter", "Materials", "Research"]
  },
  {
    id: "res-3",
    title: "Astrophysics Research Fellow",
    company: "CFA Harvard & Smithsonian",
    location: "Cambridge, MA",
    type: "Research",
    matchScore: 85,
    postedAt: "1 week ago",
    description: "Analyze data from the James Webb Space Telescope for early galaxy formation.",
    tags: ["Astrophysics", "JWST", "Data Analysis"]
  },
  {
    id: "res-4",
    title: "Nuclear Physics Research Associate",
    company: "CERN",
    location: "Geneva, Switzerland",
    type: "Research",
    matchScore: 90,
    postedAt: "3 days ago",
    description: "Participate in heavy-ion collision experiments at the ALICE detector.",
    tags: ["Nuclear Physics", "CERN", "High Energy"]
  },
  {
    id: "res-5",
    title: "Medical Physics Researcher",
    company: "Mayo Clinic",
    location: "Rochester, MN",
    type: "Research",
    matchScore: 82,
    postedAt: "4 days ago",
    description: "Develop new imaging techniques for proton beam therapy optimization.",
    tags: ["Medical Physics", "Imaging", "Healthcare"]
  },
  {
    id: "res-6",
    title: "Photonics Research Lead",
    company: "IMEC",
    location: "Leuven, Belgium",
    type: "Research",
    matchScore: 87,
    postedAt: "6 days ago",
    description: "Lead research in silicon photonics for next-gen optical interconnects.",
    tags: ["Photonics", "Silicon", "Optics"]
  },
  {
    id: "res-7",
    title: "Climate Physics Scientist",
    company: "NOAA",
    location: "Boulder, CO",
    type: "Research",
    matchScore: 79,
    postedAt: "1 week ago",
    description: "Model atmospheric dynamics to predict extreme weather patterns.",
    tags: ["Climate", "Atmospheric", "Modeling"]
  },
  {
    id: "res-8",
    title: "Biophysics Postdoc",
    company: "Stanford University",
    location: "Stanford, CA",
    type: "Research",
    matchScore: 84,
    postedAt: "2 days ago",
    description: "Study protein folding using single-molecule fluorescence spectroscopy.",
    tags: ["Biophysics", "Spectroscopy", "Biology"]
  },
  {
    id: "res-9",
    title: "Plasma Physics Research Engineer",
    company: "ITER",
    location: "Saint-Paul-lez-Durance, France",
    type: "Research",
    matchScore: 91,
    postedAt: "5 days ago",
    description: "Contribute to the development of tokamak diagnostic systems.",
    tags: ["Plasma", "Fusion", "Engineering"]
  },
  {
    id: "res-10",
    title: "Theoretical Physics Fellow",
    company: "Perimeter Institute",
    location: "Waterloo, Canada",
    type: "Research",
    matchScore: 86,
    postedAt: "1 week ago",
    description: "Independent research in string theory or quantum gravity.",
    tags: ["Theory", "String Theory", "Gravity"]
  },
  {
    id: "res-11",
    title: "Research Scientist: Quantum Materials",
    company: "Oak Ridge National Laboratory",
    location: "Oak Ridge, TN",
    type: "Research",
    matchScore: 89,
    postedAt: "4 days ago",
    description: "Explore quantum phenomena in novel materials using neutron scattering.",
    tags: ["Quantum Materials", "Neutron Scattering", "ORNL"]
  },
  {
    id: "res-12",
    title: "Computational Fluid Dynamics Researcher",
    company: "NASA Ames Research Center",
    location: "Mountain View, CA",
    type: "Research",
    matchScore: 93,
    postedAt: "2 days ago",
    description: "Develop CFD models for hypersonic flight and planetary entry.",
    tags: ["CFD", "NASA", "Aerospace"]
  },
  {
    id: "res-13",
    title: "High Energy Physics Researcher",
    company: "Fermilab",
    location: "Batavia, IL",
    type: "Research",
    matchScore: 87,
    postedAt: "1 week ago",
    description: "Analyze neutrino oscillation data from the DUNE experiment.",
    tags: ["HEP", "Fermilab", "Neutrinos"]
  },
  {
    id: "res-14",
    title: "Solar Physics Research Scientist",
    company: "NASA Goddard Space Flight Center",
    location: "Greenbelt, MD",
    type: "Research",
    matchScore: 85,
    postedAt: "3 days ago",
    description: "Study solar flares and coronal mass ejections using SDO data.",
    tags: ["Solar Physics", "NASA", "Space Weather"]
  },
  {
    id: "res-15",
    title: "Quantum Optics Postdoc",
    company: "University of Oxford",
    location: "Oxford, UK",
    type: "Research",
    matchScore: 90,
    postedAt: "5 days ago",
    description: "Research in cavity quantum electrodynamics and photon-atom interactions.",
    tags: ["Quantum Optics", "Oxford", "Physics"]
  },
  {
    id: "res-16",
    title: "Materials Science Research Fellow",
    company: "MIT",
    location: "Cambridge, MA",
    type: "Research",
    matchScore: 88,
    postedAt: "6 days ago",
    description: "Design and synthesize new materials for high-efficiency batteries.",
    tags: ["Materials Science", "MIT", "Energy Storage"]
  },
  {
    id: "res-17",
    title: "Astrobiology Research Associate",
    company: "SETI Institute",
    location: "Mountain View, CA",
    type: "Research",
    matchScore: 82,
    postedAt: "1 week ago",
    description: "Investigate biosignatures in planetary atmospheres and extreme environments.",
    tags: ["Astrobiology", "SETI", "Planetary Science"]
  },
  {
    id: "res-18",
    title: "Accelerator Physics Scientist",
    company: "SLAC National Accelerator Laboratory",
    location: "Menlo Park, CA",
    type: "Research",
    matchScore: 86,
    postedAt: "4 days ago",
    description: "Optimize beam dynamics for the LCLS-II X-ray free-electron laser.",
    tags: ["Accelerator Physics", "SLAC", "X-ray"]
  },
  {
    id: "res-19",
    title: "Cryogenic Engineering Researcher",
    company: "Bluefors",
    location: "Helsinki, Finland",
    type: "Research",
    matchScore: 84,
    postedAt: "2 days ago",
    description: "Develop ultra-low temperature cooling systems for quantum processors.",
    tags: ["Cryogenics", "Quantum", "Engineering"]
  },
  {
    id: "res-20",
    title: "Geophysics Research Lead",
    company: "Schlumberger",
    location: "Houston, TX",
    type: "Research",
    matchScore: 80,
    postedAt: "1 week ago",
    description: "Lead research in seismic imaging and subsurface characterization.",
    tags: ["Geophysics", "Seismic", "Energy"]
  },
  // 20 Opportunities (Industry, PhD, Internship, etc.)
  {
    id: "opp-1",
    title: "Senior Data Scientist",
    company: "NVIDIA",
    location: "Remote",
    type: "Industry",
    matchScore: 85,
    postedAt: "1 week ago",
    description: "Apply your physics intuition to solve complex optimization problems.",
    tags: ["Data Science", "AI", "NVIDIA"]
  },
  {
    id: "opp-2",
    title: "PhD Position: Quantum Computing",
    company: "ETH Zurich",
    location: "Zurich, Switzerland",
    type: "PhD",
    matchScore: 94,
    postedAt: "3 days ago",
    description: "Fully funded PhD position in superconducting qubit development.",
    tags: ["PhD", "Quantum", "ETH"]
  },
  {
    id: "opp-3",
    title: "Optical Engineer",
    company: "ASML",
    location: "Veldhoven, Netherlands",
    type: "Industry",
    matchScore: 89,
    postedAt: "4 days ago",
    description: "Design high-precision lithography systems for semiconductor manufacturing.",
    tags: ["Optics", "Engineering", "ASML"]
  },
  {
    id: "opp-4",
    title: "Quantum Software Internship",
    company: "IBM Research",
    location: "Yorktown Heights, NY",
    type: "Internship",
    matchScore: 90,
    postedAt: "2 days ago",
    description: "Develop algorithms for Qiskit and test on IBM Quantum systems.",
    tags: ["Internship", "Quantum", "IBM"]
  },
  {
    id: "opp-5",
    title: "Quantitative Researcher",
    company: "Jane Street",
    location: "London, UK",
    type: "Industry",
    matchScore: 82,
    postedAt: "1 week ago",
    description: "Build mathematical models for high-frequency trading strategies.",
    tags: ["Finance", "Math", "Quant"]
  },
  {
    id: "opp-6",
    title: "PhD: Renewable Energy Systems",
    company: "TU Delft",
    location: "Delft, Netherlands",
    type: "PhD",
    matchScore: 81,
    postedAt: "5 days ago",
    description: "Research in next-generation solar cell efficiency.",
    tags: ["PhD", "Energy", "Solar"]
  },
  {
    id: "opp-7",
    title: "Machine Learning Engineer",
    company: "DeepMind",
    location: "London, UK",
    type: "Industry",
    matchScore: 87,
    postedAt: "3 days ago",
    description: "Apply ML to scientific discovery in biology and materials science.",
    tags: ["AI", "Science", "DeepMind"]
  },
  {
    id: "opp-8",
    title: "Radiation Safety Officer",
    company: "Siemens Healthineers",
    location: "Erlangen, Germany",
    type: "Industry",
    matchScore: 75,
    postedAt: "1 week ago",
    description: "Ensure compliance with radiation safety standards for medical devices.",
    tags: ["Safety", "Medical", "Siemens"]
  },
  {
    id: "opp-9",
    title: "Summer Internship: Space Systems",
    company: "SpaceX",
    location: "Hawthorne, CA",
    type: "Internship",
    matchScore: 88,
    postedAt: "4 days ago",
    description: "Work on Starship structural analysis and thermal protection systems.",
    tags: ["Internship", "Space", "SpaceX"]
  },
  {
    id: "opp-10",
    title: "Algorithm Developer",
    company: "Google Quantum AI",
    location: "Santa Barbara, CA",
    type: "Industry",
    matchScore: 93,
    postedAt: "2 days ago",
    description: "Design quantum algorithms for chemistry and materials simulation.",
    tags: ["Quantum", "Google", "Algorithms"]
  },
  {
    id: "opp-11",
    title: "PhD Scholarship: Particle Physics",
    company: "University of Oxford",
    location: "Oxford, UK",
    type: "Scholarship",
    matchScore: 86,
    postedAt: "1 week ago",
    description: "Fully funded scholarship for research at the LHC.",
    tags: ["Scholarship", "PhD", "Oxford"]
  },
  {
    id: "opp-12",
    title: "Hardware Engineer: Photonics",
    company: "Intel",
    location: "Hillsboro, OR",
    type: "Industry",
    matchScore: 84,
    postedAt: "5 days ago",
    description: "Develop silicon photonics components for high-speed data centers.",
    tags: ["Hardware", "Photonics", "Intel"]
  },
  {
    id: "opp-13",
    title: "Data Analyst: Energy Markets",
    company: "Shell",
    location: "Houston, TX",
    type: "Industry",
    matchScore: 78,
    postedAt: "6 days ago",
    description: "Analyze energy consumption patterns and renewable integration.",
    tags: ["Data", "Energy", "Shell"]
  },
  {
    id: "opp-14",
    title: "Research Internship: AI for Physics",
    company: "Microsoft Research",
    location: "Redmond, WA",
    type: "Internship",
    matchScore: 89,
    postedAt: "3 days ago",
    description: "Use deep learning to accelerate physical simulations.",
    tags: ["Internship", "AI", "Microsoft"]
  },
  {
    id: "opp-15",
    title: "Systems Engineer",
    company: "Northrop Grumman",
    location: "Linthicum, MD",
    type: "Industry",
    matchScore: 80,
    postedAt: "1 week ago",
    description: "Design and test advanced radar and sensor systems.",
    tags: ["Engineering", "Defense", "Systems"]
  },
  {
    id: "opp-16",
    title: "PhD: Computational Biophysics",
    company: "University of Cambridge",
    location: "Cambridge, UK",
    type: "PhD",
    matchScore: 83,
    postedAt: "4 days ago",
    description: "Simulate molecular dynamics of cellular membranes.",
    tags: ["PhD", "Biophysics", "Cambridge"]
  },
  {
    id: "opp-17",
    title: "Acoustics Engineer",
    company: "Bose",
    location: "Framingham, MA",
    type: "Industry",
    matchScore: 77,
    postedAt: "1 week ago",
    description: "Optimize noise cancellation algorithms for consumer audio.",
    tags: ["Acoustics", "Audio", "Bose"]
  },
  {
    id: "opp-18",
    title: "Graduate Trainee: Nuclear Energy",
    company: "EDF Energy",
    location: "Bristol, UK",
    type: "Industry",
    matchScore: 76,
    postedAt: "5 days ago",
    description: "Join the nuclear operations and safety graduate program.",
    tags: ["Graduate", "Nuclear", "Energy"]
  },
  {
    id: "opp-19",
    title: "PhD: Nanotechnology",
    company: "Nanyang Technological University",
    location: "Singapore",
    type: "PhD",
    matchScore: 82,
    postedAt: "3 days ago",
    description: "Research in 2D materials for nanoelectronic devices.",
    tags: ["PhD", "Nano", "NTU"]
  },
  {
    id: "opp-20",
    title: "Technical Consultant",
    company: "McKinsey & Company",
    location: "New York, NY",
    type: "Industry",
    matchScore: 74,
    postedAt: "1 week ago",
    description: "Advise clients on emerging technologies and digital transformation.",
    tags: ["Consulting", "Tech", "McKinsey"]
  }
];

let researchItems = [
  {
    id: "pub-1",
    title: "Nonlinear Dynamics in Fiber-Optic Communications",
    authors: ["Dr. Sarah Ahmed", "John Doe"],
    type: "Paper",
    journal: "Physical Review Letters",
    year: 2024,
    abstract: "We investigate the impact of nonlinear phase noise on high-speed coherent optical systems.",
    tags: ["Optics", "Communications", "Nonlinear Dynamics"],
    link: "#",
    codeLink: "https://github.com/demo/nonlinear-optics",
    datasetLink: "https://zenodo.org/record/12345"
  },
  {
    id: "pre-1",
    title: "Quantum Error Correction with Topological Insulators",
    authors: ["Demo Alumni", "Alice Smith"],
    type: "Preprint",
    journal: "arXiv:2501.12345",
    year: 2025,
    abstract: "A novel approach to fault-tolerant quantum computing using surface states of topological insulators.",
    tags: ["Quantum", "Topological Insulators", "Error Correction"],
    link: "#"
  },
  {
    id: "code-1",
    title: "PyPhysicsSim: A High-Performance Particle Simulator",
    authors: ["Demo Alumni"],
    type: "Code",
    journal: "Open Source",
    year: 2023,
    abstract: "A Python-based library for simulating large-scale particle interactions using GPU acceleration.",
    tags: ["Simulation", "Python", "GPU"],
    link: "https://github.com/demo/pyphysicssim"
  },
  {
    id: "data-1",
    title: "SUST Campus Solar Radiation Dataset (2020-2025)",
    authors: ["Physics Dept, SUST"],
    type: "Dataset",
    journal: "Open Data",
    year: 2025,
    abstract: "High-resolution solar irradiance data collected from the SUST campus weather station.",
    tags: ["Solar", "Renewable Energy", "Dataset"],
    link: "#"
  }
];

let currentUser: string | null = null;

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Auth Routes
  app.get("/api/auth/session", (req, res) => {
    if (currentUser && users[currentUser]) {
      res.json({ user: users[currentUser], profile: users[currentUser] });
    } else {
      res.status(401).json({ error: "No session" });
    }
  });

  app.post("/api/auth/login", (req, res) => {
    const { email } = req.body;
    const user = Object.values(users).find(u => u.email === email);
    if (user) {
      currentUser = user.uid;
      res.json({ user, profile: user });
    } else {
      res.status(401).json({ error: "User not found" });
    }
  });

  app.post("/api/auth/signup", (req, res) => {
    const { email, phone, displayName, batch, referralUid, method } = req.body;
    
    // Check if user already exists
    if (Object.values(users).some(u => u.email === email)) {
      return res.status(400).json({ error: "Email already registered" });
    }

    // Generate 6-digit OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const identifier = method === "sms" ? phone : email;
    otps[identifier] = otp;
    pendingUsers[identifier] = { ...req.body, uid: `user-${Date.now()}` };

    if (method === "sms") {
      console.log(`[AUTH] SMS OTP for ${phone}: ${otp}`); // Log to console for user to see
      res.json({ success: true, message: "OTP sent to your mobile via SMS" });
    } else {
      console.log(`[AUTH] Email OTP for ${email}: ${otp}`); // Log to console for user to see
      res.json({ success: true, message: "OTP sent to your email" });
    }
  });

  app.post("/api/auth/verify-otp", (req, res) => {
    const { email, phone, otp, method } = req.body;
    const identifier = method === "sms" ? phone : email;

    if (otps[identifier] === otp) {
      const newUser = pendingUsers[identifier];
      users[newUser.uid] = {
        ...newUser,
        role: "alumni",
        isPublic: true,
        photoURL: `https://picsum.photos/seed/${newUser.uid}/200`,
        skills: [],
        aspirations: "",
        mentorshipRole: "mentee",
        batch: newUser.batch || "N/A"
      };
      currentUser = newUser.uid;
      delete otps[identifier];
      delete pendingUsers[identifier];
      res.json({ user: users[currentUser], profile: users[currentUser] });
    } else {
      res.status(400).json({ error: "Invalid OTP" });
    }
  });

  // LinkedIn OAuth Routes
  app.get("/api/auth/linkedin/url", (req, res) => {
    const redirectUri = `${process.env.APP_URL}/api/auth/linkedin/callback`;
    const params = new URLSearchParams({
      response_type: "code",
      client_id: process.env.LINKEDIN_CLIENT_ID!,
      redirect_uri: redirectUri,
      scope: "openid profile email",
    });
    const authUrl = `https://www.linkedin.com/oauth/v2/authorization?${params.toString()}`;
    res.json({ url: authUrl });
  });

  app.get("/api/auth/linkedin/callback", async (req, res) => {
    const { code } = req.query;
    if (!code) return res.status(400).send("No code provided");

    try {
      const redirectUri = `${process.env.APP_URL}/api/auth/linkedin/callback`;
      
      // Exchange code for token
      const tokenRes = await axios.post("https://www.linkedin.com/oauth/v2/accessToken", 
        new URLSearchParams({
          grant_type: "authorization_code",
          code: code as string,
          client_id: process.env.LINKEDIN_CLIENT_ID!,
          client_secret: process.env.LINKEDIN_CLIENT_SECRET!,
          redirect_uri: redirectUri,
        }).toString(),
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );

      const accessToken = tokenRes.data.access_token;

      // Get user profile
      const profileRes = await axios.get("https://api.linkedin.com/v2/userinfo", {
        headers: { Authorization: `Bearer ${accessToken}` }
      });

      const profileData = profileRes.data;
      const email = profileData.email;
      const name = profileData.name;
      const photo = profileData.picture;

      // Check if user exists, if not create
      let user = Object.values(users).find(u => u.email === email);
      if (!user) {
        const uid = `linkedin-${profileData.sub}`;
        user = {
          uid,
          displayName: name,
          email,
          photoURL: photo,
          batch: "N/A",
          role: "alumni",
          mentorshipRole: "mentee",
          isPublic: true,
          skills: [],
          aspirations: ""
        };
        users[uid] = user;
      }

      currentUser = user.uid;

      res.send(`
        <html>
          <body>
            <script>
              if (window.opener) {
                window.opener.postMessage({ type: 'OAUTH_AUTH_SUCCESS' }, '*');
                window.close();
              } else {
                window.location.href = '/';
              }
            </script>
            <p>Authentication successful. This window should close automatically.</p>
          </body>
        </html>
      `);
    } catch (error: any) {
      console.error("LinkedIn OAuth error:", error.response?.data || error.message);
      res.status(500).send("Authentication failed");
    }
  });

  app.get("/api/auth/referral-check/:uid", (req, res) => {
    const referrer = users[req.params.uid];
    if (referrer) {
      res.json({ success: true, name: referrer.displayName });
    } else {
      res.status(404).json({ error: "Referral ID not found" });
    }
  });

  app.post("/api/auth/logout", (req, res) => {
    currentUser = null;
    res.json({ success: true });
  });

  // Admin Routes
  app.get("/api/admin/stats", (req, res) => {
    if (!currentUser || users[currentUser]?.role !== "admin") {
      return res.status(403).json({ error: "Unauthorized" });
    }
    res.json({
      totalUsers: Object.keys(users).length,
      activeOpportunities: opportunities.length,
      researchPapers: researchItems.length,
      pendingVerifications: 0, // Mocked for now
      systemStatus: "Healthy",
      lastAiUpdate
    });
  });

  app.get("/api/admin/users", (req, res) => {
    if (!currentUser || users[currentUser]?.role !== "admin") {
      return res.status(403).json({ error: "Unauthorized" });
    }
    res.json(Object.values(users));
  });

  app.put("/api/admin/users/:uid", (req, res) => {
    if (!currentUser || users[currentUser]?.role !== "admin") {
      return res.status(403).json({ error: "Unauthorized" });
    }
    const { uid } = req.params;
    if (users[uid]) {
      users[uid] = { ...users[uid], ...req.body };
      res.json(users[uid]);
    } else {
      res.status(404).json({ error: "User not found" });
    }
  });

  app.delete("/api/admin/users/:uid", (req, res) => {
    if (!currentUser || users[currentUser]?.role !== "admin") {
      return res.status(403).json({ error: "Unauthorized" });
    }
    const { uid } = req.params;
    if (users[uid]) {
      delete users[uid];
      res.json({ success: true });
    } else {
      res.status(404).json({ error: "User not found" });
    }
  });

  // Profile Routes
  app.get("/api/profile/:uid", (req, res) => {
    const profile = users[req.params.uid];
    if (profile) res.json(profile);
    else res.status(404).json({ error: "Not found" });
  });

  app.put("/api/profile", (req, res) => {
    if (!currentUser) return res.status(401).json({ error: "Unauthorized" });
    users[currentUser] = { ...users[currentUser], ...req.body };
    res.json(users[currentUser]);
  });

  // Directory Routes
  app.get("/api/directory", (req, res) => {
    res.json(Object.values(users).filter(u => u.isPublic));
  });

  // Opportunity Routes
  app.get("/api/opportunities", (req, res) => {
    res.json(opportunities);
  });

  // Research Routes
  app.get("/api/research", (req, res) => {
    res.json(researchItems);
  });

  app.get("/api/research/similar/:id", (req, res) => {
    const item = researchItems.find(i => i.id === req.params.id);
    if (!item) return res.status(404).json({ error: "Not found" });
    
    // Mock AI similarity: find items with overlapping tags
    const similar = researchItems
      .filter(i => i.id !== item.id && i.tags.some(t => item.tags.includes(t)))
      .slice(0, 3);
    res.json(similar);
  });

  app.get("/api/research/collaborators/:id", (req, res) => {
    const item = researchItems.find(i => i.id === req.params.id);
    if (!item) return res.status(404).json({ error: "Not found" });
    
    // Mock AI collaborator discovery: find alumni with skills matching item tags
    const collaborators = Object.values(users)
      .filter(u => u.skills.some(s => item.tags.includes(s)))
      .slice(0, 3);
    res.json(collaborators);
  });

  // Stats & Suggestions
  app.get("/api/stats", (req, res) => {
    res.json({
      networkSize: Object.keys(users).length * 1000 + 281, // Mocking growth
      activeJobs: opportunities.length + 140,
      countries: 38,
      engagementRate: 68,
      newProfilesWeekly: 24
    });
  });

  app.get("/api/suggestions", (req, res) => {
    // Return all users except current as suggestions
    const suggestions = Object.values(users)
      .filter(u => u.uid !== currentUser)
      .map(u => ({
        uid: u.uid,
        displayName: u.displayName,
        batch: u.batch,
        currentIndustry: u.currentIndustry,
        location: u.location,
        photoURL: u.photoURL
      }));
    res.json(suggestions);
  });

  // Mentorship Routes
  app.get("/api/mentorship/suggestions", async (req, res) => {
    if (!currentUser) return res.status(401).json({ error: "Unauthorized" });
    
    const userProfile = users[currentUser];
    const targetRole = userProfile.mentorshipRole === 'mentor' ? 'mentee' : 'mentor';
    
    // Filter potential matches
    const potentialMatches = Object.values(users)
      .filter(u => u.uid !== currentUser && u.mentorshipRole === targetRole);
    
    try {
      const suggestions = await matchMentorship(userProfile, potentialMatches);
      
      // Merge AI suggestions with actual user data
      const enrichedSuggestions = suggestions.map((s: any) => ({
        ...s,
        user: users[s.uid]
      })).filter((s: any) => s.user); // Ensure user still exists
      
      res.json(enrichedSuggestions);
    } catch (e) {
      console.error("Mentorship matching failed:", e);
      res.status(500).json({ error: "AI matching failed" });
    }
  });

  // AI Routes
  app.post("/api/ai/summarize", async (req, res) => {
    try {
      const summary = await summarizeProfile(req.body.profile);
      res.json({ summary });
    } catch (e) {
      res.status(500).json({ error: "AI failed" });
    }
  });

  app.post("/api/ai/match", async (req, res) => {
    try {
      const match = await matchOpportunity(req.body.opportunity, req.body.profile);
      res.json(match);
    } catch (e) {
      res.status(500).json({ error: "AI failed" });
    }
  });

  // API Routes
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", message: "SUST Physics Alumni Hub API is active" });
  });

  // AI Agent: Opportunity Broker (Simulated)
  app.get("/api/ai/agent/status", (req, res) => {
    res.json({
      status: aiAgentStatus,
      lastUpdate: lastAiUpdate,
      agentName: "SUST PHYSICS Opportunity Scout"
    });
  });

  app.post("/api/ai/agent/trigger", async (req, res) => {
    aiAgentStatus = "Searching Worldwide...";
    try {
      const newOpps = await fetchNewOpportunities();
      if (newOpps && newOpps.length > 0) {
        // Add metadata to new opportunities
        const processedOpps = newOpps.map((opp: any) => ({
          ...opp,
          postedAt: "Just now",
          matchScore: Math.floor(Math.random() * 30) + 70, // Random score between 70-100
          isAiGenerated: true
        }));
        
        // Prepend to opportunities list
        opportunities = [...processedOpps, ...opportunities];
        lastAiUpdate = new Date().toISOString();
        aiAgentStatus = "Idle";
        res.json({ success: true, count: newOpps.length, opportunities: processedOpps });
      } else {
        aiAgentStatus = "Idle";
        res.json({ success: false, message: "No new opportunities found" });
      }
    } catch (e) {
      aiAgentStatus = "Error";
      console.error("AI Agent failed:", e);
      res.status(500).json({ error: "AI Agent failed to fetch opportunities" });
    }
  });

  app.post("/api/ai/match-opportunity", async (req, res) => {
    const { opportunity, userProfile } = req.body;
    // In a real app, we'd use Gemini to compare embeddings or text
    res.json({
      matchScore: 0.85,
      reason: "Your background in Quantum Mechanics matches this PostDoc position perfectly.",
      nudge: `Hi ${userProfile.displayName}, a new PostDoc in Quantum Computing just opened up. Based on your thesis on 'Entanglement', you're a top candidate!`
    });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
