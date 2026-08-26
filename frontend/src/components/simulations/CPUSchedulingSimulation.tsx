import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Clock, Cpu } from 'lucide-react';

interface Process { id: string; name: string; arrival: number; burst: number; remaining: number; color: string; }

export const CPUSchedulingSimulation: React.FC = () => {
  const [algorithm, setAlgorithm] = useState<'RR' | 'FCFS' | 'SJF'>('RR');
  const [quantum, setQuantum] = useState<number>(2);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [ganttChart, setGanttChart] = useState<Array<{ pid: string; color: string; time: number }>>([]);

  const defaultProcesses: Process[] = [
    { id: 'P1', name: 'Process 1 (DB Query)', arrival: 0, burst: 5, remaining: 5, color: '#3b82f6' },
    { id: 'P2', name: 'Process 2 (Image Render)', arrival: 1, burst: 3, remaining: 3, color: '#10b981' },
    { id: 'P3', name: 'Process 3 (HTTP Handler)', arrival: 2, burst: 6, remaining: 6, color: '#f59e0b' },
    { id: 'P4', name: 'Process 4 (Audio Stream)', arrival: 4, burst: 2, remaining: 2, color: '#ec4899' },
  ];

  const [processes, setProcesses] = useState<Process[]>(defaultProcesses);

  const reset = () => {
    setIsRunning(false);
    setCurrentTime(0);
    setGanttChart([]);
    setProcesses(defaultProcesses.map((p) => ({ ...p })));
  };

  useEffect(() => {
    let timer: any;
    if (isRunning) {
      timer = setInterval(() => {
        setProcesses((prev) => {
          const available = prev.filter((p) => p.arrival <= currentTime && p.remaining > 0);
          if (available.length === 0) {
            const anyRemaining = prev.some((p) => p.remaining > 0);
            if (!anyRemaining) setIsRunning(false);
            else setCurrentTime((t) => t + 1);
            return prev;
          }

          let selected: Process = available[0];
          if (algorithm === 'SJF') selected = [...available].sort((a, b) => a.remaining - b.remaining)[0];
          else if (algorithm === 'RR') {
            const index = Math.floor(currentTime / quantum) % available.length;
            selected = available[index];
          }

          setGanttChart((g) => [...g, { pid: selected.id, color: selected.color, time: currentTime }]);
          setCurrentTime((t) => t + 1);

          return prev.map((p) => p.id === selected.id ? { ...p, remaining: Math.max(0, p.remaining - 1) } : p);
        });
      }, 600);
    }
    return () => clearInterval(timer);
  }, [isRunning, currentTime, algorithm, quantum]);

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="h-5 w-5 text-indigo-400" />
            Live CPU Scheduler & Gantt Chart
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Simulate Round Robin, First-Come First-Served, and Shortest Job First with real-time state dispatching.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800">
            {(['RR', 'FCFS', 'SJF'] as const).map((algo) => (
              <button
                key={algo}
                onClick={() => { setAlgorithm(algo); reset(); }}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                  algorithm === algo ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {algo === 'RR' ? 'Round Robin' : algo}
              </button>
            ))}
          </div>

          <button
            onClick={() => setIsRunning(!isRunning)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow"
          >
            {isRunning ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {isRunning ? 'Pause' : 'Start Simulation'}
          </button>
          <button onClick={reset} className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs">
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {processes.map((p) => {
          const pct = Math.round(((p.burst - p.remaining) / p.burst) * 100);
          const isDone = p.remaining === 0;
          return (
            <div key={p.id} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full" style={{ backgroundColor: p.color }} />
                  <span className="font-bold text-xs text-slate-200">{p.id}</span>
                </div>
                <span className="text-[10px] px-1.5 py-0.5 rounded font-semibold bg-indigo-950 text-indigo-300">
                  {isDone ? 'Done' : `Rem: ${p.remaining}s`}
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
                <div className="h-1.5 rounded-full transition-all duration-300" style={{ width: `${pct}%`, backgroundColor: p.color }} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
        <div className="text-xs text-slate-400 mb-3 flex items-center gap-1.5">
          <Clock className="h-4 w-4 text-indigo-400" />
          Execution Timeline (Time: {currentTime}s)
        </div>
        {ganttChart.length === 0 ? (
          <div className="h-14 flex items-center justify-center text-xs text-slate-500 border border-dashed border-slate-800 rounded-lg">
            Click 'Start Simulation' to watch CPU scheduling
          </div>
        ) : (
          <div className="flex overflow-x-auto gap-1 py-1">
            {ganttChart.map((block, idx) => (
              <div key={idx} className="flex-shrink-0 w-10 h-12 rounded-lg flex flex-col items-center justify-center text-xs font-bold text-white shadow-sm" style={{ backgroundColor: block.color }}>
                <span>{block.pid}</span>
                <span className="text-[9px] opacity-80">{block.time}s</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
