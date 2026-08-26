import React, { useState } from 'react';
import { Cpu, Layers, HardDrive, CheckCircle2, AlertTriangle } from 'lucide-react';

export const MemoryPagingSimulation: React.FC = () => {
  const [virtualAddress, setVirtualAddress] = useState<string>('0x00403010');
  const [tlbEnabled, setTlbEnabled] = useState<boolean>(true);

  const cleanHex = virtualAddress.startsWith('0x') ? virtualAddress.slice(2) : virtualAddress;
  const intVal = parseInt(cleanHex, 16) || 0;
  const offset = intVal & 0xFFF;
  const vpn = (intVal >> 12) & 0xFFFFF;

  const vpnHex = '0x' + vpn.toString(16).toUpperCase().padStart(5, '0');
  const offsetHex = '0x' + offset.toString(16).toUpperCase().padStart(3, '0');

  const pageTableMapping: Record<string, { frame: string; valid: boolean; dirty: boolean }> = {
    '0x00403': { frame: '0x0812', valid: true, dirty: false },
    '0x00A05': { frame: '0x0234', valid: true, dirty: true },
    '0x00100': { frame: '0x0000', valid: false, dirty: false },
  };

  const tlbCache: Record<string, string> = { '0x00403': '0x0812' };
  const isTlbHit = tlbEnabled && !!tlbCache[vpnHex];
  const tableEntry = pageTableMapping[vpnHex];
  const isValid = tableEntry?.valid ?? false;
  const frameNumber = isTlbHit ? tlbCache[vpnHex] : tableEntry ? tableEntry.frame : '0x0999';
  const physicalAddress = isValid
    ? '0x' + ((parseInt(frameNumber.slice(2), 16) << 12) | offset).toString(16).toUpperCase().padStart(7, '0')
    : 'PAGE_FAULT';

  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Layers className="h-5 w-5 text-indigo-400" />
            Interactive MMU & Paging Simulation
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Test real-time 32-bit virtual address bit-splitting, TLB lookups, page tables, and physical RAM frame translation.
          </p>
        </div>
        <button
          onClick={() => setTlbEnabled(!tlbEnabled)}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
            tlbEnabled ? 'bg-indigo-600/30 text-indigo-300 border-indigo-500/50' : 'bg-slate-800 text-slate-400 border-slate-700'
          }`}
        >
          TLB Cache: {tlbEnabled ? 'ON' : 'OFF'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800/80">
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1.5">Virtual Memory Address</label>
          <input
            type="text"
            value={virtualAddress}
            onChange={(e) => setVirtualAddress(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1.5">Quick Presets</label>
          <div className="flex gap-2">
            {['0x00403010', '0x00A05024', '0x00100004'].map((addr) => (
              <button key={addr} onClick={() => setVirtualAddress(addr)} className="px-2.5 py-2 rounded-lg bg-slate-900 border border-slate-800 hover:border-indigo-500 text-xs font-mono text-slate-300">
                {addr}
              </button>
            ))}
          </div>
        </div>
        <div className="flex flex-col justify-center">
          <span className="text-[11px] text-slate-400">Page Configuration</span>
          <span className="text-xs font-semibold text-slate-200">Page Size: 4 KB (2¹² B) | Offset: 12b | VPN: 20b</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-950/80 border border-indigo-500/30 flex flex-col justify-between">
          <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Cpu className="h-4 w-4" /> 1. CPU Virtual Address
          </div>
          <div className="font-mono text-base font-extrabold text-white">{virtualAddress}</div>
          <div className="mt-3 pt-3 border-t border-slate-800 grid grid-cols-2 gap-2 text-xs font-mono">
            <div className="bg-indigo-950/50 p-2 rounded border border-indigo-800/40">
              <span className="text-[10px] text-slate-400 block">VPN (20b)</span>
              <span className="text-indigo-300 font-bold">{vpnHex}</span>
            </div>
            <div className="bg-purple-950/50 p-2 rounded border border-purple-800/40">
              <span className="text-[10px] text-slate-400 block">Offset (12b)</span>
              <span className="text-purple-300 font-bold">{offsetHex}</span>
            </div>
          </div>
        </div>

        <div className={`p-4 rounded-xl bg-slate-950/80 border flex flex-col justify-between ${
          isTlbHit ? 'border-emerald-500/50 bg-emerald-950/10' : 'border-slate-800'
        }`}>
          <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>2. TLB Cache</span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${isTlbHit ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'}`}>
              {isTlbHit ? 'HIT (0.5 ns)' : 'MISS'}
            </span>
          </div>
          <div className="text-xs text-slate-400">{isTlbHit ? `Translation VPN ${vpnHex} -> Frame ${frameNumber}` : 'TLB miss occurred. Accessing Page Table in RAM...'}</div>
        </div>

        <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col justify-between">
          <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">3. Page Table Entry</div>
          {tableEntry ? (
            <div className="space-y-1.5 text-xs font-mono">
              <div className="flex justify-between"><span className="text-slate-400">Frame:</span><span className="text-emerald-400 font-bold">{tableEntry.frame}</span></div>
              <div className="flex justify-between"><span className="text-slate-400">Valid:</span><span className={tableEntry.valid ? 'text-emerald-400' : 'text-rose-400 font-bold'}>{tableEntry.valid ? '1' : '0 (Fault)'}</span></div>
            </div>
          ) : (
            <div className="text-xs text-slate-400">Simulated Frame: <span className="font-mono text-emerald-400">0x0999</span></div>
          )}
        </div>

        <div className={`p-4 rounded-xl border flex flex-col justify-between ${
          isValid ? 'bg-gradient-to-br from-emerald-950/30 to-slate-950 border-emerald-500/40' : 'bg-gradient-to-br from-rose-950/30 to-slate-950 border-rose-500/40'
        }`}>
          <div className="text-xs font-bold text-slate-200 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <HardDrive className="h-4 w-4 text-emerald-400" /> 4. Physical RAM
          </div>
          {isValid ? (
            <div>
              <span className="text-[11px] text-slate-400 block">Physical Address:</span>
              <div className="font-mono text-lg font-black text-emerald-300">{physicalAddress}</div>
              <div className="mt-2 text-[11px] text-emerald-400/90 flex items-center gap-1">
                <CheckCircle2 className="h-3.5 w-3.5" /> Frame {frameNumber} + Offset {offsetHex}
              </div>
            </div>
          ) : (
            <div>
              <div className="font-mono text-base font-black text-rose-400 flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4" /> PAGE FAULT
              </div>
              <p className="mt-1 text-[11px] text-rose-300">Interrupts OS to load page from swap.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
