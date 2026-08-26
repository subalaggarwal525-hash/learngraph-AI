import React, { useState } from 'react';
import { Send } from 'lucide-react';

export const NetworkPacketSimulation: React.FC = () => {
  const [step, setStep] = useState<number>(0);
  const steps = [
    { name: 'Initial State', clientState: 'CLOSED', serverState: 'LISTEN', description: 'Server listens on port 80/443. Client prepares initial SYN packet.' },
    { name: 'Step 1: SYN', clientState: 'SYN_SENT', serverState: 'LISTEN', description: 'Client sends SYN (Seq=100) requesting connection.' },
    { name: 'Step 2: SYN-ACK', clientState: 'SYN_SENT', serverState: 'SYN_RCVD', description: 'Server acknowledges client Seq (Ack=101) and sends SYN (Seq=300).' },
    { name: 'Step 3: ACK', clientState: 'ESTABLISHED', serverState: 'ESTABLISHED', description: 'Client acknowledges server Seq (Ack=301). Connection is fully ESTABLISHED.' },
  ];

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Send className="h-5 w-5 text-indigo-400" />
            TCP 3-Way Handshake & Packet Transmission
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Visualize packet exchange, sequence numbers, and socket state machine.</p>
        </div>
        <button
          onClick={() => setStep((s) => (s < 3 ? s + 1 : 0))}
          className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-bold text-white shadow"
        >
          {step === 3 ? 'Reset Handshake' : 'Next Packet Step'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-950 p-6 rounded-xl border border-slate-800">
        <div className="p-4 rounded-xl bg-slate-900 border border-indigo-500/30 text-center space-y-2">
          <div className="text-xs font-bold text-indigo-400 uppercase">Client (192.168.1.50)</div>
          <div className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-indigo-950 text-indigo-300">
            {steps[step].clientState}
          </div>
        </div>
        <div className="p-4 rounded-xl bg-slate-900 border border-purple-500/30 text-center space-y-2">
          <div className="text-xs font-bold text-purple-400 uppercase">Server (142.250.190.46)</div>
          <div className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-purple-950 text-purple-300">
            {steps[step].serverState}
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center gap-4">
        <div className="h-10 w-10 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center font-bold text-base shrink-0">
          {step}
        </div>
        <div>
          <h4 className="text-xs font-bold text-slate-200">{steps[step].name}</h4>
          <p className="text-xs text-slate-400 mt-0.5">{steps[step].description}</p>
        </div>
      </div>
    </div>
  );
};
