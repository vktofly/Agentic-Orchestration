import { useState, useEffect } from 'react';
import { FastForward, Rewind, Activity } from 'lucide-react';

interface ScrubBarProps {
  threadId: string;
}

export default function ScrubBar({ threadId }: ScrubBarProps) {
  const [history, setHistory] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (!threadId) return;
    const fetchHistory = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/history/${threadId}`);
        const data = await res.json();
        if (data.history && data.history.length > 0) {
          setHistory(data.history);
          // If we are currently at the last step, auto-advance to the newly fetched last step
          setCurrentIndex(prev => prev === history.length - 1 || prev === 0 ? data.history.length - 1 : prev);
        }
      } catch (err) {
        console.error(err);
      }
    };
    
    // Poll while the graph might be executing
    fetchHistory();
    const interval = setInterval(fetchHistory, 1500);
    return () => clearInterval(interval);
  }, [threadId]);

  if (history.length === 0) return null;

  const currentState = history[currentIndex]?.values || {};

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl mt-6 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Activity className="w-4 h-4 text-blue-400" />
          Time-Travel Scrub Bar (SQLite Tracing)
        </h3>
        <div className="text-xs text-slate-400 font-mono">Thread: {threadId.substring(0, 8)}...</div>
      </div>
      
      <div className="flex items-center gap-4 mb-6">
        <button 
          onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
          className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-slate-200"
          disabled={currentIndex === 0}
        >
          <Rewind className="w-4 h-4" />
        </button>
        
        <input 
          type="range" 
          min={0} 
          max={Math.max(0, history.length - 1)} 
          value={currentIndex}
          onChange={(e) => setCurrentIndex(Number(e.target.value))}
          className="flex-1 accent-blue-500"
        />
        
        <button 
          onClick={() => setCurrentIndex(Math.min(history.length - 1, currentIndex + 1))}
          className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-slate-200"
          disabled={currentIndex === history.length - 1}
        >
          <FastForward className="w-4 h-4" />
        </button>
      </div>
      
      <div className="bg-slate-900 rounded p-4 text-xs font-mono text-slate-300 overflow-x-auto border border-slate-700">
        <div className="mb-2 text-emerald-400">Step {currentIndex + 1} of {history.length}</div>
        <pre>{JSON.stringify(currentState, null, 2)}</pre>
      </div>
    </div>
  );
}
