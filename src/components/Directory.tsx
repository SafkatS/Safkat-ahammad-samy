import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import * as d3 from "d3";
import { 
  Map as MapIcon, 
  Search, 
  Filter, 
  Globe, 
  Users, 
  MessageCircle,
  Linkedin,
  GraduationCap,
  X,
  User
} from "lucide-react";

const WorldMap = ({ alumni }: { alumni: any[] }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedAlumni, setSelectedAlumni] = useState<any | null>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    svg.selectAll("*").remove();

    const projection = d3.geoMercator()
      .scale(width / 6.5)
      .translate([width / 2, height / 1.5]);

    const path = d3.geoPath().projection(projection);

    // Fetch world map data
    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then((data: any) => {
      svg.append("g")
        .selectAll("path")
        .data(data.features)
        .enter()
        .append("path")
        .attr("d", path as any)
        .attr("fill", "#18181b")
        .attr("stroke", "#27272a")
        .attr("stroke-width", 0.5);

      // Add markers
      const markers = svg.append("g")
        .selectAll("circle")
        .data(alumni.filter(a => a.lat && a.lng))
        .enter()
        .append("circle")
        .attr("cx", d => projection([d.lng, d.lat])![0])
        .attr("cy", d => projection([d.lng, d.lat])![1])
        .attr("r", 5)
        .attr("fill", "#f97316")
        .attr("stroke", "#ffffff")
        .attr("stroke-width", 1)
        .attr("class", "cursor-pointer hover:scale-150 transition-transform")
        .on("click", (event, d) => {
          setSelectedAlumni(d);
        });

      // Add pulse effect
      markers.each(function() {
        const marker = d3.select(this);
        const repeat = () => {
          marker.transition()
            .duration(1000)
            .attr("r", 8)
            .attr("opacity", 0.5)
            .transition()
            .duration(1000)
            .attr("r", 5)
            .attr("opacity", 1)
            .on("end", repeat);
        };
        repeat();
      });
    });
  }, [alumni]);

  return (
    <div className="relative w-full h-full">
      <svg ref={svgRef} className="w-full h-full" />
      
      <AnimatePresence>
        {selectedAlumni && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="absolute bottom-8 left-1/2 -translate-x-1/2 w-80 bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-2xl z-50"
          >
            <button 
              onClick={() => setSelectedAlumni(null)}
              className="absolute top-2 right-2 p-1 text-zinc-500 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
            <div className="flex items-center gap-4 mb-4">
              <img 
                src={selectedAlumni.photoURL} 
                alt={selectedAlumni.displayName} 
                className="w-12 h-12 rounded-xl object-cover border border-zinc-700"
              />
              <div>
                <h4 className="text-sm font-bold text-white">{selectedAlumni.displayName}</h4>
                <p className="text-[10px] text-zinc-500 font-mono uppercase tracking-widest">Batch {selectedAlumni.batch}</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-xs text-zinc-400">
                <Globe className="w-3 h-3 text-zinc-600" />
                <span>{selectedAlumni.location}</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-zinc-400">
                <Users className="w-3 h-3 text-zinc-600" />
                <span>{selectedAlumni.currentIndustry || "Alumni"}</span>
              </div>
            </div>
            <button className="w-full mt-4 py-2 bg-white text-black text-xs font-bold rounded-xl hover:scale-105 transition-transform">
              View Full Profile
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

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
        <div className="h-[60vh] w-full bg-zinc-950 border border-zinc-800 rounded-3xl relative overflow-hidden">
          <WorldMap alumni={filteredAlumni} />
        </div>
      )}
    </div>
  );
}
