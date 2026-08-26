import React, { useState } from 'react';
import { Cpu, Layers, BarChart2, Send } from 'lucide-react';
import { MemoryPagingSimulation } from '../components/simulations/MemoryPagingSimulation';
import { CPUSchedulingSimulation } from '../components/simulations/CPUSchedulingSimulation';
import { SortingSimulation } from '../components/simulations/SortingSimulation';
import { NetworkPacketSimulation } from '../components/simulations/NetworkPacketSimulation';

export const SimulationsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'paging' | 'cpu' | 'sorting' | 'network'>('paging');

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-black text-white flex items-center gap-2">
          <Cpu className="h-6 w-6 text-indigo-400" />
          Interactive Simulations Lab
        </h1>
        <p className="text-xs text-slate-400 mt-1">Explore hands-on mental model visualizations.</p>
      </div>

      <div className="flex gap-2 border-b border-slate-800 pb-3 overflow-x-auto no-scrollbar">
        {[
          { id: 'paging', label: 'Virtual Memory & Paging MMU', icon: Layers },
          { id: 'cpu', label: 'CPU Scheduler & Gantt Chart', icon: Cpu },
          { id: 'sorting', label: 'Sorting Algorithms', icon: BarChart2 },
          { id: 'network', label: 'TCP 3-Way Handshake', icon: Send },
        ].map((t) => {
          const Icon = t.icon;
          const isSelected = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id as any)}
              className={`px-4 py-2 rounded-xl border text-xs font-bold flex items-center gap-2 ${
                isSelected ? 'bg-indigo-600 text-white border-indigo-500 shadow' : 'bg-slate-900 border-slate-800 text-slate-400'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      <div>
        {activeTab === 'paging' && <MemoryPagingSimulation />}
        {activeTab === 'cpu' && <CPUSchedulingSimulation />}
        {activeTab === 'sorting' && <SortingSimulation />}
        {activeTab === 'network' && <NetworkPacketSimulation />}
      </div>
    </div>
  );
};
