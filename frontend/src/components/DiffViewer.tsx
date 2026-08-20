import { useState, useEffect } from 'react';
import { GitCompare, Loader2, Database } from 'lucide-react';

export default function DiffViewer() {
  const [diffData, setDiffData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/prompt-diff')
      .then(res => res.json())
      .then(data => {
        setDiffData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center p-8"><Loader2 className="animate-spin text-slate-400" /></div>;
  }

  if (!diffData || !diffData.optimized) {
    return (
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 text-center text-slate-400 mt-6">
        <Database className="w-8 h-8 mx-auto mb-3 opacity-50" />
        <p>No optimized DSPy prompts found.</p>
        <p className="text-sm mt-1 opacity-75">Run the CLI compilation script to generate optimized weights.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden mt-6">
      <div className="bg-slate-900/60 px-4 py-3 border-b border-slate-700/50 flex items-center gap-2">
        <GitCompare className="w-4 h-4 text-emerald-400" />
        <h3 className="text-sm font-semibold text-slate-200">DSPy Prompt Diff Viewer</h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-700">
        <div className="p-4">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Base Signature</h4>
          <div className="space-y-4">
            <div className="bg-slate-900 rounded p-3 text-sm text-slate-300 font-mono">
              {diffData.base.instruction}
            </div>
            <div className="text-xs text-slate-500">No few-shot demonstrations.</div>
          </div>
        </div>
        <div className="p-4 bg-emerald-900/10">
          <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-4">Compiled Weights</h4>
          <div className="space-y-4">
            <div className="bg-emerald-900/20 border border-emerald-800/50 rounded p-3 text-sm text-slate-200 font-mono">
              {diffData.optimized.instruction}
            </div>
            <div>
              <h5 className="text-xs text-slate-400 mb-2">Bootstrapped Demos ({diffData.optimized.demos.length})</h5>
              <div className="space-y-2">
                {diffData.optimized.demos.map((demo: any, i: number) => (
                  <div key={i} className="bg-slate-900/80 rounded p-2 text-xs border border-slate-700">
                    <div className="text-emerald-400 truncate" title={demo.question}><span className="text-slate-500">Q:</span> {demo.question}</div>
                    <div className="text-blue-400 truncate mt-1" title={demo.answer}><span className="text-slate-500">A:</span> {demo.answer}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
