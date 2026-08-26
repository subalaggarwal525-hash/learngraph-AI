import React, { useState } from 'react';
import { Play, RotateCcw, BarChart2 } from 'lucide-react';

export const SortingSimulation: React.FC = () => {
  const [array, setArray] = useState<number[]>([48, 15, 82, 34, 91, 23, 67, 5, 53, 76]);
  const [activeIndices, setActiveIndices] = useState<number[]>([]);
  const [isSorting, setIsSorting] = useState<boolean>(false);

  const reset = () => {
    setIsSorting(false);
    setActiveIndices([]);
    setArray([48, 15, 82, 34, 91, 23, 67, 5, 53, 76]);
  };

  const bubbleSort = async () => {
    setIsSorting(true);
    let arr = [...array];
    const n = arr.length;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        setActiveIndices([j, j + 1]);
        await new Promise((r) => setTimeout(r, 180));
        if (arr[j] > arr[j + 1]) {
          const temp = arr[j];
          arr[j] = arr[j + 1];
          arr[j + 1] = temp;
          setArray([...arr]);
        }
      }
    }
    setActiveIndices([]);
    setIsSorting(false);
  };

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <BarChart2 className="h-5 w-5 text-indigo-400" />
            Sorting Algorithm Visualizer
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Step-by-step comparative animation showing element comparisons and swaps.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={bubbleSort}
            disabled={isSorting}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-bold shadow"
          >
            <Play className="h-3.5 w-3.5" />
            {isSorting ? 'Sorting...' : 'Animate Bubble Sort'}
          </button>
          <button onClick={reset} disabled={isSorting} className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs">
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="h-48 bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-end justify-center gap-3">
        {array.map((val, idx) => {
          const isActive = activeIndices.includes(idx);
          return (
            <div key={idx} className="flex flex-col items-center gap-1 flex-1 max-w-[40px]">
              <span className="text-[10px] font-mono text-slate-400">{val}</span>
              <div
                className={`w-full rounded-t-lg transition-all duration-200 ${
                  isActive ? 'bg-amber-400 shadow-lg shadow-amber-400/40 scale-105' : 'bg-indigo-600'
                }`}
                style={{ height: `${val * 1.5}px` }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};
