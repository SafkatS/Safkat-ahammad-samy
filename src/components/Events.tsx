import React from "react";
import { motion } from "motion/react";
import { Calendar, MapPin, Users, Clock, ChevronRight } from "lucide-react";

const events = [
  { id: 1, title: "Alumni Reunion 2026", date: "2026-05-10", time: "10:00 AM", location: "SUST Campus", attendees: 150, category: "Reunion" },
  { id: 2, title: "Workshop on Quantum Mechanics", date: "2026-04-15", time: "02:00 PM", location: "Online", attendees: 80, category: "Workshop" },
  { id: 3, title: "Career Path for Physics Graduates", date: "2026-04-20", time: "03:00 PM", location: "Auditorium", attendees: 120, category: "Seminar" },
  { id: 4, title: "Physics Alumni Networking Dinner", date: "2026-05-25", time: "07:00 PM", location: "Dhaka", attendees: 60, category: "Networking" },
];

export default function Events() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Upcoming Events</h1>
        <p className="text-zinc-500 text-sm">Join our community events, workshops, and seminars.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {events.map((event) => (
          <motion.div
            key={event.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="p-8 bg-zinc-900 border border-zinc-800 rounded-3xl hover:border-zinc-700 transition-all group cursor-pointer relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 p-6">
              <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 bg-zinc-800 px-3 py-1 rounded-full border border-zinc-700">
                {event.category}
              </span>
            </div>
            
            <div className="space-y-6">
              <h3 className="text-xl font-bold group-hover:text-white transition-colors">{event.title}</h3>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-3 text-zinc-500 text-sm">
                  <Calendar className="w-4 h-4" />
                  <span>{event.date}</span>
                </div>
                <div className="flex items-center gap-3 text-zinc-500 text-sm">
                  <Clock className="w-4 h-4" />
                  <span>{event.time}</span>
                </div>
                <div className="flex items-center gap-3 text-zinc-500 text-sm">
                  <MapPin className="w-4 h-4" />
                  <span>{event.location}</span>
                </div>
                <div className="flex items-center gap-3 text-zinc-500 text-sm">
                  <Users className="w-4 h-4" />
                  <span>{event.attendees} Attending</span>
                </div>
              </div>
              
              <button className="w-full py-3 bg-zinc-800 text-white rounded-2xl text-xs font-bold border border-zinc-700 hover:bg-white hover:text-black transition-all flex items-center justify-center gap-2">
                Register Now <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
