'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import {
  Cpu, Activity, Wifi, Shield, Bot, Eye, Flame,
  RotateCcw, Zap, Database, Radio, ChevronRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';

/* ── Types ── */
interface CoreMetric {
  label: string;
  value: string;
  color: string;
}

interface AgentStatus {
  name: string;
  status: 'active' | 'busy' | 'error' | 'idle';
  progress: number;
}

interface LogEntry {
  time: string;
  msg: string;
  color: string;
}

/* ── Data ── */
const coreMetrics: CoreMetric[] = [
  { label: 'Neural Cores', value: '8/8 Active', color: 'text-cyber-cyan' },
  { label: 'Processing', value: '2.4 TFLOPS', color: 'text-cyber-cyan' },
  { label: 'Agent Sync', value: 'Connected', color: 'text-emerald-400' },
  { label: 'Memory', value: '14.2 / 32 GB', color: 'text-amber-400' },
  { label: 'Threat Level', value: 'LOW', color: 'text-emerald-400' },
  { label: 'Uptime', value: '47d 12h 33m', color: 'text-foreground' },
];

const agentStatuses: AgentStatus[] = [
  { name: 'Recon', status: 'active', progress: 73 },
  { name: 'Scanner', status: 'busy', progress: 45 },
  { name: 'Exploit', status: 'error', progress: 12 },
  { name: 'Monitor', status: 'active', progress: 100 },
  { name: 'Payload', status: 'busy', progress: 56 },
];

const initialLogs: LogEntry[] = [
  { time: '12:45:01', msg: 'Agent recon-001 completed subnet scan', color: 'text-emerald-400' },
  { time: '12:44:58', msg: 'Scanner agent found 23 open ports on target', color: 'text-cyber-cyan' },
  { time: '12:44:52', msg: 'Exploit agent failed CVE-2024-3094 — retrying', color: 'text-cyber-red' },
  { time: '12:44:47', msg: 'Memory cleanup: freed 2.1 GB of heap', color: 'text-amber-400' },
  { time: '12:44:41', msg: 'New threat signature database loaded (v4.2.1)', color: 'text-cyber-blue' },
  { time: '12:44:35', msg: 'Firewall rules updated: 3 new rules applied', color: 'text-cyber-cyan' },
  { time: '12:44:28', msg: 'TLS certificate for agent channel renewed', color: 'text-emerald-400' },
];

const dynamicLogMessages = [
  { msg: 'Heartbeat received from all active agents', color: 'text-emerald-400' },
  { msg: 'Network latency: avg 12ms across all channels', color: 'text-cyber-cyan' },
  { msg: 'Cache hit ratio: 94.2% — optimal', color: 'text-foreground' },
  { msg: 'GPU temperature: 62°C — within safe range', color: 'text-amber-400' },
  { msg: 'New connection established from 10.0.0.45', color: 'text-cyber-blue' },
  { msg: 'Encrypted channel verified: AES-256-GCM', color: 'text-emerald-400' },
  { msg: 'Scheduled task queued: full system scan in 30m', color: 'text-muted-foreground' },
  { msg: 'Alert: unusual outbound traffic on port 4444', color: 'text-cyber-red' },
  { msg: 'Agent payload-006 completed payload generation', color: 'text-cyber-cyan' },
  { msg: 'DNS resolution cache refreshed: 847 entries', color: 'text-foreground' },
];

/* ── Utility ── */
function getNow(): string {
  return new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function getStatusColor(status: AgentStatus['status']) {
  return status === 'active' ? 'bg-emerald-400' : status === 'busy' ? 'bg-amber-400' : status === 'error' ? 'bg-cyber-red' : 'bg-gray-400';
}

/* ═══════════════════════════════════════════════════════════
   MAIN DRAGON CORE COMPONENT
   ═══════════════════════════════════════════════════════════ */
export function DragonView() {
  /* ── 3D mouse tracking state ── */
  const containerRef = useRef<HTMLDivElement>(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  const [scale, setScale] = useState(1);
  const [isHovering, setIsHovering] = useState(false);
  const [glowIntensity, setGlowIntensity] = useState(0.3);

  /* ── Live data state ── */
  const [logs, setLogs] = useState<LogEntry[]>(initialLogs);
  const [cpuLoad, setCpuLoad] = useState(42);
  const [gpuLoad, setGpuLoad] = useState(67);
  const [uptime, setUptime] = useState(47 * 86400 + 12 * 3600 + 33 * 60);

  /* ── 3D mouse move handler ── */
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const deltaX = (e.clientX - centerX) / (rect.width / 2);
    const deltaY = (e.clientY - centerY) / (rect.height / 2);
    setRotateX(-deltaY * 15); // max ±15 deg
    setRotateY(deltaX * 15);
    setScale(1 + Math.abs(deltaX) * 0.03);
  }, []);

  const handleMouseEnter = useCallback(() => {
    setIsHovering(true);
    setGlowIntensity(0.6);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setIsHovering(false);
    setRotateX(0);
    setRotateY(0);
    setScale(1);
    setGlowIntensity(0.3);
  }, []);

  /* ── Live metrics updates ── */
  useEffect(() => {
    const cpuInterval = setInterval(() => {
      setCpuLoad((prev) => Math.max(15, Math.min(95, prev + (Math.random() - 0.5) * 8)));
    }, 3000);
    const gpuInterval = setInterval(() => {
      setGpuLoad((prev) => Math.max(20, Math.min(90, prev + (Math.random() - 0.5) * 6)));
    }, 4000);
    return () => { clearInterval(cpuInterval); clearInterval(gpuInterval); };
  }, []);

  /* ── Live log stream ── */
  useEffect(() => {
    const logInterval = setInterval(() => {
      const entry = dynamicLogMessages[Math.floor(Math.random() * dynamicLogMessages.length)];
      setLogs((prev) => [...prev.slice(-7), { time: getNow(), msg: entry.msg, color: entry.color }]);
    }, 5000);
    return () => clearInterval(logInterval);
  }, []);

  /* ── Uptime counter ── */
  useEffect(() => {
    const interval = setInterval(() => setUptime((prev) => prev + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  const formatUptime = useCallback((seconds: number) => {
    const d = Math.floor(seconds / 86400);
    const h = Math.floor((seconds % 86400) / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${d}d ${h}h ${m}m`;
  }, []);

  return (
    <div className="relative h-full w-full overflow-hidden" style={{ background: 'radial-gradient(ellipse at center, #111827 0%, #0a0a0f 60%, #050508 100%)' }}>

      {/* ── Ambient particles (pure CSS) ── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {Array.from({ length: 30 }).map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-cyber-cyan animate-float-particle"
            style={{
              width: `${1 + Math.random() * 2}px`,
              height: `${1 + Math.random() * 2}px`,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              opacity: 0.1 + Math.random() * 0.3,
              animationDuration: `${8 + Math.random() * 12}s`,
              animationDelay: `${Math.random() * 5}s`,
            }}
          />
        ))}
      </div>

      {/* ── Subtle grid background ── */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03]"
        style={{
          backgroundImage: 'linear-gradient(rgba(0,240,255,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0,240,255,0.3) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />

      {/* ═══ 3D INTERACTIVE DRAGON IMAGE ═══ */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div
          ref={containerRef}
          className="relative pointer-events-auto cursor-grab active:cursor-grabbing select-none"
          style={{ perspective: '1200px' }}
          onMouseMove={handleMouseMove}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          <div
            className="relative transition-transform duration-200 ease-out"
            style={{
              transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(${scale})`,
              transformStyle: 'preserve-3d',
            }}
          >
            {/* Outer glow layers */}
            <div
              className="absolute -inset-8 rounded-3xl blur-3xl transition-all duration-500"
              style={{
                background: `radial-gradient(circle, rgba(0,240,255,${glowIntensity * 0.15}) 0%, transparent 70%)`,
              }}
            />
            <div
              className="absolute -inset-4 rounded-2xl blur-xl transition-all duration-500"
              style={{
                background: `radial-gradient(circle, rgba(124,58,237,${glowIntensity * 0.1}) 0%, transparent 60%)`,
              }}
            />

            {/* Main image container */}
            <div
              className={cn(
                'relative rounded-xl overflow-hidden border transition-all duration-500',
                isHovering
                  ? 'border-cyber-cyan/40 shadow-[0_0_40px_rgba(0,240,255,0.15),0_0_80px_rgba(0,240,255,0.05)]'
                  : 'border-cyber-cyan/15 shadow-[0_0_20px_rgba(0,240,255,0.08)]'
              )}
              style={{ width: 'min(50vh, 380px)', height: 'min(50vh, 380px)', transform: 'translateZ(0px)' }}
            >
              <img
                src="/dragon-core-3d.png"
                alt="KaliGhost Core"
                className="w-full h-full object-cover"
                draggable={false}
                style={{ filter: isHovering ? 'drop-shadow(0 0 40px rgba(0,240,255,0.25))' : 'drop-shadow(0 0 20px rgba(0,240,255,0.1))' }}
              />

              {/* Scan line overlay */}
              <div className="absolute inset-0 pointer-events-none">
                <div className="absolute inset-0 animate-scan-line opacity-20"
                  style={{
                    background: 'linear-gradient(180deg, transparent 0%, rgba(0,240,255,0.15) 50%, transparent 100%)',
                    backgroundSize: '100% 200%',
                    animation: 'scanline 4s linear infinite',
                  }}
                />
              </div>

              {/* Corner accents */}
              <div className="absolute top-0 left-0 w-10 h-10 border-t-2 border-l-2 border-cyber-cyan/50 rounded-tl-xl" />
              <div className="absolute top-0 right-0 w-10 h-10 border-t-2 border-r-2 border-cyber-cyan/50 rounded-tr-xl" />
              <div className="absolute bottom-0 left-0 w-10 h-10 border-b-2 border-l-2 border-cyber-cyan/50 rounded-bl-xl" />
              <div className="absolute bottom-0 right-0 w-10 h-10 border-b-2 border-r-2 border-cyber-cyan/50 rounded-br-xl" />

              {/* Energy lines from corners */}
              <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-cyber-cyan/30 via-transparent to-transparent" />
              <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-transparent to-cyber-purple/30" />
            </div>

            {/* Depth shadow behind image */}
            <div
              className="absolute inset-0 rounded-xl"
              style={{
                transform: 'translateZ(-20px)',
                background: 'rgba(0,240,255,0.03)',
                filter: 'blur(30px)',
              }}
            />
          </div>
        </div>
      </div>

      {/* ═══ TOP-LEFT: Core Status Panel ═══ */}
      <div className="absolute top-5 left-5 z-10 pointer-events-auto">
        <div className="cyber-panel p-4 w-[250px] relative overflow-hidden">
          {/* Scan line */}
          <div className="absolute inset-0 pointer-events-none scan-line" />

          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-status-pulse" />
            <span className="text-xs font-mono text-emerald-400">ONLINE</span>
            <span className="text-[10px] text-muted-foreground ml-auto font-mono">v3.2.1</span>
          </div>
          <h3 className="text-sm font-bold text-foreground mb-1 text-glow-cyan">Dragon Core</h3>
          <p className="text-[11px] text-muted-foreground mb-3 leading-relaxed">Neural engine — optimal capacity</p>

          <div className="space-y-1.5">
            {coreMetrics.map((m) => (
              <div key={m.label} className="flex justify-between items-center">
                <span className="text-[10px] text-muted-foreground">{m.label}</span>
                <span className={`text-[10px] font-mono font-medium ${m.color}`}>{m.value}</span>
              </div>
            ))}
            <div className="flex justify-between items-center pt-1">
              <span className="text-[10px] text-muted-foreground">Uptime</span>
              <span className="text-[10px] font-mono font-medium text-foreground">{formatUptime(uptime)}</span>
            </div>
          </div>

          {/* Mini bars */}
          <div className="mt-3 pt-3 border-t border-border space-y-2">
            <div>
              <div className="flex justify-between text-[9px] mb-1">
                <span className="text-muted-foreground">CPU</span>
                <span className="text-cyber-cyan font-mono">{Math.round(cpuLoad)}%</span>
              </div>
              <div className="h-1 bg-surface-0 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-cyber-cyan to-cyber-blue rounded-full transition-all duration-1000"
                  style={{ width: `${cpuLoad}%` }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-[9px] mb-1">
                <span className="text-muted-foreground">GPU</span>
                <span className="text-cyber-purple font-mono">{Math.round(gpuLoad)}%</span>
              </div>
              <div className="h-1 bg-surface-0 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-cyber-purple to-cyber-red rounded-full transition-all duration-1000"
                  style={{ width: `${gpuLoad}%` }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ═══ TOP-RIGHT: Agent Status ═══ */}
      <div className="absolute top-5 right-5 z-10 pointer-events-auto">
        <div className="cyber-panel p-3 w-[190px]">
          <div className="flex items-center gap-2 mb-3">
            <Bot className="h-3.5 w-3.5 text-cyber-cyan" />
            <h4 className="text-[10px] font-mono text-muted-foreground tracking-wider uppercase">Active Agents</h4>
          </div>
          <div className="space-y-2">
            {agentStatuses.map((a) => (
              <div key={a.name} className="flex items-center gap-2 group">
                <div className={cn('w-1.5 h-1.5 rounded-full transition-colors', getStatusColor(a.status))} />
                <span className="text-[10px] text-foreground flex-1 group-hover:text-cyber-cyan transition-colors">{a.name}</span>
                <div className="w-12 h-1 bg-surface-0 rounded-full overflow-hidden">
                  <div className={cn('h-full rounded-full transition-all duration-1000',
                    a.status === 'active' ? 'bg-emerald-400' : a.status === 'busy' ? 'bg-amber-400' : 'bg-cyber-red'
                  )} style={{ width: `${a.progress}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ═══ BOTTOM-LEFT: System Log (live) ═══ */}
      <div className="absolute bottom-5 left-5 z-10 pointer-events-auto">
        <div className="cyber-panel p-3 w-[340px]">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Radio className="h-3 w-3 text-cyber-cyan animate-status-pulse" />
              <h4 className="text-[10px] font-mono text-muted-foreground tracking-wider uppercase">System Log</h4>
            </div>
            <span className="text-[9px] font-mono text-emerald-400">LIVE</span>
          </div>
          <div className="space-y-0.5 font-mono text-[9px] max-h-[120px] overflow-hidden">
            {logs.map((log, i) => (
              <div key={`${log.time}-${i}`} className="flex gap-2 leading-relaxed">
                <span className="text-muted-foreground/40 flex-shrink-0">{log.time}</span>
                <span className={log.color}>{log.msg}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ═══ BOTTOM-RIGHT: Quick Actions ═══ */}
      <div className="absolute bottom-5 right-5 z-10 pointer-events-auto">
        <div className="cyber-panel p-3 w-[180px]">
          <h4 className="text-[10px] font-mono text-muted-foreground tracking-wider uppercase mb-2">Quick Actions</h4>
          <div className="space-y-1">
            {[
              { icon: Zap, label: 'Run Diagnostics', color: 'text-cyber-cyan' },
              { icon: Shield, label: 'Security Scan', color: 'text-emerald-400' },
              { icon: Database, label: 'Export Memory', color: 'text-cyber-purple' },
              { icon: RotateCcw, label: 'Restart Core', color: 'text-amber-400' },
            ].map((action) => (
              <button key={action.label} className="w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-[10px] text-muted-foreground hover:text-foreground hover:bg-surface-2 transition-all group">
                <action.icon className={cn('h-3 w-3 group-hover:', action.color, ' transition-colors')} />
                <span>{action.label}</span>
                <ChevronRight className="h-2.5 w-2.5 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ═══ BOTTOM-CENTER: Hint ═══ */}
      <div className="absolute bottom-5 left-1/2 -translate-x-1/2 z-10">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-1/60 backdrop-blur-sm border border-border/50">
          <div className="w-1.5 h-1.5 rounded-full bg-cyber-cyan animate-status-pulse" />
          <span className="text-[9px] font-mono text-muted-foreground/60">
            MOVE MOUSE OVER DRAGON FOR 3D EFFECT
          </span>
        </div>
      </div>

      {/* ═══ CSS Keyframes (injected via style tag) ═══ */}
      <style jsx>{`
        @keyframes float-particle {
          0%, 100% { transform: translateY(0) translateX(0); opacity: 0.1; }
          25% { transform: translateY(-30px) translateX(10px); opacity: 0.3; }
          50% { transform: translateY(-60px) translateX(-5px); opacity: 0.15; }
          75% { transform: translateY(-30px) translateX(15px); opacity: 0.25; }
        }
        .animate-float-particle { animation: float-particle var(--duration, 10s) ease-in-out infinite; }
        @keyframes scanline {
          0% { background-position: 0% -100%; }
          100% { background-position: 0% 200%; }
        }
      `}</style>
    </div>
  );
}
