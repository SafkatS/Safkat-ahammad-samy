import { GoogleGenAI, Type } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

export async function summarizeProfile(profileData: any) {
  const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: `Summarize this SUST Physics Alumni profile into a professional "Career Path Narrative" and a "Skill Cloud" (comma-separated list). Profile: ${JSON.stringify(profileData)}`,
    config: {
      responseMimeType: "application/json",
    }
  });
  return JSON.parse(response.text);
}

export async function matchOpportunity(opportunity: any, userProfile: any) {
  const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: `Analyze the match between this job opportunity and user profile. Provide a match score (0-1), a reason, and a personalized WhatsApp nudge.
    Opportunity: ${JSON.stringify(opportunity)}
    User: ${JSON.stringify(userProfile)}`,
    config: {
      responseMimeType: "application/json",
    }
  });
  return JSON.parse(response.text);
}

export async function matchMentorship(userProfile: any, potentialMatches: any[]) {
  const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: `Analyze the mentorship compatibility between the user and a list of potential alumni. 
    The user is looking for a ${userProfile.mentorshipRole === 'mentor' ? 'mentee' : 'mentor'}.
    
    User Profile: ${JSON.stringify(userProfile)}
    Potential Matches: ${JSON.stringify(potentialMatches)}
    
    For each potential match, provide:
    1. Compatibility score (0-100)
    2. A detailed reason for the match based on skills, thesis topics, and career aspirations.
    3. A suggested "Icebreaker" message.
    
    Return the results as a JSON array of objects with fields: uid, score, reason, icebreaker.`,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            uid: { type: Type.STRING },
            score: { type: Type.NUMBER },
            reason: { type: Type.STRING },
            icebreaker: { type: Type.STRING }
          },
          required: ["uid", "score", "reason", "icebreaker"]
        }
      }
    }
  });
  
  try {
    return JSON.parse(response.text);
  } catch (e) {
    console.error("Failed to parse mentorship matches:", response.text);
    return [];
  }
}

export async function fetchNewOpportunities() {
  const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: "Find 5 current and real-world worldwide physics opportunities including jobs, PhD positions, scholarships, and industry offers. Focus on high-impact roles at institutions like CERN, NASA, Max Planck, or tech companies like NVIDIA/IBM. Return them as a JSON array of objects with fields: id (unique string starting with 'ai-'), title, company, location, type (Industry, Research, PhD, Internship, or Scholarship), description, and tags (array of strings).",
    config: {
      tools: [{ googleSearch: {} }],
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            id: { type: Type.STRING },
            title: { type: Type.STRING },
            company: { type: Type.STRING },
            location: { type: Type.STRING },
            type: { type: Type.STRING },
            description: { type: Type.STRING },
            tags: {
              type: Type.ARRAY,
              items: { type: Type.STRING }
            }
          },
          required: ["id", "title", "company", "location", "type", "description", "tags"]
        }
      }
    }
  });
  
  try {
    return JSON.parse(response.text);
  } catch (e) {
    console.error("Failed to parse AI opportunities:", response.text);
    return [];
  }
}
