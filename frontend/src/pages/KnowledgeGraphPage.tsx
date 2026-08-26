import React, { useState, useCallback, useMemo } from 'react';
import ReactFlow, { Background, Controls, MiniMap, NodeProps, Handle, Position, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';
import { useNavigate } from 'react-router-dom';
import { Lock, CheckCircle, Play, AlertTriangle, BookOpen, HelpCircle } from 'lucide-react';
import { useCourse } from '../context/CourseContext';

const CustomConceptNode: React.FC<NodeProps> = ({ data, selected }) => {
  const status = data.status || 'locked';
  const mastery = data.mastery_score || 0;

  const statusStyles = {
    locked: 'bg-slate-900/90 border-slate-800 text-slate-500 opacity-60',
    available: 'bg-indigo-950/80 border-indigo-500/80 text-slate-100 ring-2 ring-indigo-500/30',
    learning: 'bg-amber-950/80 border-amber-500 text-amber-200 ring-2 ring-amber-500/40',
    mastered: 'bg-emerald-950/80 border-emerald-500 text-emerald-100 ring-2 ring-emerald-500/40',
    needs_review: 'bg-rose-950/80 border-rose-500 text-rose-200 ring-2 ring-rose-500/40',
  };

  return (
    <div className={`px-4 py-3 rounded-2xl border shadow-xl min-w-[220px] max-w-[260px] cursor-pointer transition-all ${statusStyles[status as keyof typeof statusStyles] || statusStyles.locked} ${selected ? 'ring-4 ring-white/50 scale-105' : ''}`}>
      <Handle type="target" position={Position.Top} className="!bg-indigo-400 !w-2 !h-2" />
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[10px] font-bold uppercase">{status}</span>
        <span className="text-[10px] font-mono font-bold bg-black/40 px-1.5 py-0.5 rounded">{mastery}%</span>
      </div>
      <div className="text-xs font-extrabold line-clamp-2">{data.title}</div>
      <div className="mt-2 flex items-center justify-between text-[10px] opacity-75 border-t border-white/10 pt-1.5">
        <span>⏱️ {data.estimated_minutes || 20}m</span>
        <span>Diff: {'★'.repeat(data.difficulty || 2)}</span>
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-indigo-400 !w-2 !h-2" />
    </div>
  );
};

export const KnowledgeGraphPage: React.FC = () => {
  const navigate = useNavigate();
  const { activeCourse, setActiveConceptId } = useCourse();
  const nodeTypes = useMemo(() => ({ conceptNode: CustomConceptNode }), []);
  const [selectedNodeData, setSelectedNodeData] = useState<any>(null);

  const initialNodes = useMemo(() => activeCourse?.knowledge_graph?.nodes || [], [activeCourse]);
  const initialEdges = useMemo(() => (activeCourse?.knowledge_graph?.edges || []).map((e) => ({ ...e, style: { stroke: '#6366f1', strokeWidth: 2 } })), [activeCourse]);

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  const onNodeClick = useCallback((_: any, node: any) => {
    setSelectedNodeData(node.data);
    setActiveConceptId(node.id);
  }, [setActiveConceptId]);

  if (!activeCourse) return <div className="p-12 text-center text-slate-400">Please select a course first.</div>;

  return (
    <div className="relative h-[calc(100vh-4rem)] w-full flex flex-col">
      <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between z-10">
        <h2 className="text-base font-black text-white">{activeCourse.title} — Knowledge Graph</h2>
        <div className="flex gap-2 text-[10px]">
          <span className="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-800 text-emerald-300">✓ Mastered</span>
          <span className="px-2 py-0.5 rounded bg-indigo-950 border border-indigo-800 text-indigo-300">▶ Available</span>
          <span className="px-2 py-0.5 rounded bg-rose-950 border border-rose-800 text-rose-300">! Needs Review</span>
          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">🔒 Locked</span>
        </div>
      </div>

      <div className="flex-1 w-full h-full relative">
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onNodeClick={onNodeClick} nodeTypes={nodeTypes} fitView className="bg-slate-950">
          <Background color="#1e293b" gap={20} size={1} />
          <Controls className="!bg-slate-900 !border-slate-800 !text-white" />
          <MiniMap className="!bg-slate-900/90 !border-slate-800" />
        </ReactFlow>

        {selectedNodeData && (
          <div className="absolute top-4 right-4 z-20 w-80 bg-slate-900/95 border border-slate-800 rounded-2xl p-5 shadow-2xl backdrop-blur-md">
            <div className="flex justify-between mb-2">
              <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-950 text-indigo-300">{selectedNodeData.status}</span>
              <button onClick={() => setSelectedNodeData(null)} className="text-slate-400 text-xs">✕</button>
            </div>
            <h3 className="text-sm font-bold text-white mb-1">{selectedNodeData.title}</h3>
            <p className="text-xs text-slate-300 mb-4">{selectedNodeData.short_summary}</p>
            <div className="flex gap-2">
              <button onClick={() => { setActiveConceptId(selectedNodeData.id); navigate('/lesson'); }} className="flex-1 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold flex items-center justify-center gap-1.5">
                <BookOpen className="h-3.5 w-3.5" /> Open Lesson
              </button>
              <button onClick={() => { setActiveConceptId(selectedNodeData.id); navigate('/quiz'); }} className="flex-1 py-2 rounded-xl bg-slate-800 text-slate-200 text-xs font-bold flex items-center justify-center gap-1.5">
                <HelpCircle className="h-3.5 w-3.5" /> Quiz
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
