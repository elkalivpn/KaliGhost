'use client';

import { useState, useEffect, useCallback, useRef, memo } from 'react';
import {
  Bot, Pause, Play, Square, RotateCw, FileText,
  ArrowUpRight, ArrowDownRight, Cpu, MemoryStick, Network,
  Wifi, WifiOff,
} from 'lucide-react';
import { useAppStore } from '@/stores/app-store';
import { useToast } from '@/hooks/use-toast';
import type { Agent, SystemMetric } from '@/types';
import { cn } from '@/lib/utils';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip,
  ResponsiveContainer, Legend,
} from 'recharts';

/* ───────────── Constants ───────────── */
const statusColors: Record<string, string> = {
  online: 'bg-emerald-400',
  offline: 'bg-gray-500',
  busy: 'bg-amber-400',
  error: 'bg-cyber-red',
};

const statusGlow: Record<string, string> = {
  online: 'glow-green',
  busy: 'glow-yellow',
  error: 'glow-red',
  offline: '',
};

const statusLabel: Record<string, string> = {
  online: 'Online',
  offline: 'Offline',
  busy: 'Busy',
  error: 'Error',
};

const typeColors: Record<string, string> = {
  recon: 'text-cyber-cyan bg-cyber-cyan/10',
  scanner: 'text-amber-400 bg-amber-400/10',
  exploit: 'text-cyber-red bg-cyber-red/10',
  report: 'text-emerald-400 bg-emerald-400/10',
  monitor: 'text-cyber-blue bg-cyber-blue/10',
  custom: 'text-cyber-purple bg-cyber-purple/10',
};

const avatarColors: Record<string, string> = {
  recon: '#00f0ff',
  scanner: '#eab308',
  exploit: '#ef4444',
  report: '#22c55e',
  monitor: '#0ea5e9',
  custom: '#7c3aed',
};

/* ───────────── Chart Tooltip ───────────── */
function ChartTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}) {
  if (!active || !payload) return null;
  return (
    <div className="bg-surface-1 border border-border rounded-lg p-2 text-[10px] shadow-xl">
      <p className="text-muted-foreground mb-1 font-mono">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }} className="font-mono">
          {entry.name}: {entry.value.toFixed(1)}%
        </p>
      ))}
    </div>
  );
}

function NetworkTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}) {
  if (!active || !payload) return null;
  return (
    <div className="bg-surface-1 border border-border rounded-lg p-2 text-[10px] shadow-xl">
      <p className="text-muted-foreground mb-1 font-mono">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }} className="font-mono">
          {entry.name}: {entry.value.toFixed(0)} MB/s
        </p>
      ))}
    </div>
  );
}

/* ───────────── Metric Generators ───────────── */
function timeNow(): string {
  const d = new Date();
  return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
}

function genCpuPoint(prev: number): SystemMetric & { key: number } {
  const next = Math.max(10, Math.min(90, prev + (Math.random() * 16 - 8)));
  return { key: Date.now(), time: timeNow(), cpu: next, memory: 60, networkIn: 0, networkOut: 0 };
}

function genMemPoint(prev: number): SystemMetric & { key: number } {
  const next = Math.max(40, Math.min(85, prev + (Math.random() * 12 - 6)));
  return { key: Date.now(), time: timeNow(), cpu: 0, memory: next, networkIn: 0, networkOut: 0 };
}

function genNetworkPoint(): SystemMetric & { key: number } {
  return {
    key: Date.now(),
    time: timeNow(),
    cpu: 0,
    memory: 0,
    networkIn: 50 + Math.random() * 350,
    networkOut: 30 + Math.random() * 250,
  };
}

/* ───────────── Agent Card ───────────── */
const AgentCard = memo(function AgentCard({
  agent,
  onPauseResume,
  onStop,
  onRestart,
  onLogs,
}: {
  agent: Agent;
  onPauseResume: (id: string) => void;
  onStop: (id: string) => void;
  onRestart: (id: string) => void;
  onLogs: (id: string) => void;
}) {
  const isPaused = agent.status === 'idle';
  const isOffline = agent.status === 'offline';
  const color = avatarColors[agent.type] || '#94a3b8';
  const initial = agent.name.charAt(0).toUpperCase();

  return (
    <div
      className={cn(
        'cyber-panel p-4 transition-all duration-300',
        statusGlow[agent.status],
        isOffline && 'opacity-60'
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <div
            className="h-9 w-9 rounded-lg flex items-center justify-center text-sm font-bold shrink-0"
            style={{ backgroundColor: `${color}20`, color }}
          >
            {initial}
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-foreground truncate">{agent.name}</span>
              <div className={cn(
                'w-2 h-2 rounded-full flex-shrink-0',
                statusColors[agent.status],
                agent.status !== 'offline' && 'animate-status-pulse'
              )} />
            </div>
            <span className={cn('text-[10px] px-1.5 py-0.5 rounded-full inline-block mt-0.5', typeColors[agent.type])}>
              {agent.type}
            </span>
          </div>
        </div>
        <span className={cn(
          'text-[10px] font-mono px-2 py-0.5 rounded-full border flex-shrink-0',
          agent.status === 'online' && 'text-emerald-400 border-emerald-400/20 bg-emerald-400/5',
          agent.status === 'busy' && 'text-amber-400 border-amber-400/20 bg-amber-400/5',
          agent.status === 'error' && 'text-cyber-red border-cyber-red/20 bg-cyber-red/5',
          agent.status === 'offline' && 'text-gray-400 border-gray-400/20 bg-gray-400/5',
          agent.status === 'idle' && 'text-cyber-blue border-cyber-blue/20 bg-cyber-blue/5',
        )}>
          {agent.status === 'idle' ? 'Paused' : statusLabel[agent.status]}
        </span>
      </div>

      {/* Task */}
      <p className="text-[11px] text-muted-foreground mb-3 truncate" title={agent.task}>
        {agent.task}
      </p>

      {/* Progress Bar */}
      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] text-muted-foreground">Progress</span>
          <span className="text-[10px] text-cyber-cyan font-mono">{agent.progress}%</span>
        </div>
        <div className="h-1.5 bg-surface-0 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-cyber-cyan to-cyber-blue rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${agent.progress}%` }}
          />
        </div>
      </div>

      {/* CPU / RAM mini bars */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-[10px] text-muted-foreground">CPU</span>
            <span className="text-[10px] text-foreground font-mono">{agent.cpu}%</span>
          </div>
          <div className="h-1 bg-surface-0 rounded-full overflow-hidden">
            <div
              className={cn(
                'h-full rounded-full transition-all duration-1000',
                agent.cpu > 70 ? 'bg-cyber-red' : agent.cpu > 40 ? 'bg-amber-400' : 'bg-emerald-400'
              )}
              style={{ width: `${agent.cpu}%` }}
            />
          </div>
        </div>
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-[10px] text-muted-foreground">MEM</span>
            <span className="text-[10px] text-foreground font-mono">{agent.memory}%</span>
          </div>
          <div className="h-1 bg-surface-0 rounded-full overflow-hidden">
            <div
              className={cn(
                'h-full rounded-full transition-all duration-1000',
                agent.memory > 70 ? 'bg-cyber-red' : agent.memory > 40 ? 'bg-amber-400' : 'bg-emerald-400'
              )}
              style={{ width: `${agent.memory}%` }}
            />
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center justify-between pt-2 border-t border-border">
        <span className="text-[10px] text-muted-foreground font-mono flex items-center gap-1">
          {agent.status !== 'offline' ? <Wifi className="h-2.5 w-2.5 text-emerald-400" /> : <WifiOff className="h-2.5 w-2.5 text-gray-500" />}
          {agent.uptime}
        </span>
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={() => onPauseResume(agent.id)}
            disabled={isOffline}
            className="p-1.5 rounded hover:bg-surface-2 text-muted-foreground hover:text-cyber-cyan transition-colors disabled:opacity-30 disabled:pointer-events-none cursor-pointer"
            title={isPaused ? 'Resume' : 'Pause'}
          >
            {isPaused ? <Play className="h-3 w-3" /> : <Pause className="h-3 w-3" />}
          </button>
          <button
            type="button"
            onClick={() => onStop(agent.id)}
            disabled={isOffline}
            className="p-1.5 rounded hover:bg-surface-2 text-muted-foreground hover:text-cyber-red transition-colors disabled:opacity-30 disabled:pointer-events-none cursor-pointer"
            title="Stop"
          >
            <Square className="h-3 w-3" />
          </button>
          <button
            type="button"
            onClick={() => onRestart(agent.id)}
            className="p-1.5 rounded hover:bg-surface-2 text-muted-foreground hover:text-amber-400 transition-colors cursor-pointer"
            title="Restart"
          >
            <RotateCw className="h-3 w-3" />
          </button>
          <button
            type="button"
            onClick={() => onLogs(agent.id)}
            className="p-1.5 rounded hover:bg-surface-2 text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
            title="View Logs"
          >
            <FileText className="h-3 w-3" />
          </button>
        </div>
      </div>
    </div>
  );
});

/* ───────────── Agent Monitor ───────────── */
export function AgentMonitor() {
  const { agents, updateAgent, setActiveView } = useAppStore();
  const { toast } = useToast();

  /* ── Chart data states ── */
  const [cpuData, setCpuData] = useState<(SystemMetric & { key: number })[]>(() => {
    let v = 40 + Math.random() * 20;
    return Array.from({ length: 30 }, () => {
      const p = genCpuPoint(v);
      v = p.cpu;
      return p;
    });
  });

  const [memData, setMemData] = useState<(SystemMetric & { key: number })[]>(() => {
    let v = 55 + Math.random() * 15;
    return Array.from({ length: 30 }, () => {
      const p = genMemPoint(v);
      v = p.memory;
      return p;
    });
  });

  const [netData, setNetData] = useState<(SystemMetric & { key: number })[]>(() =>
    Array.from({ length: 15 }, () => genNetworkPoint())
  );

  /* ── Update CPU chart every 2s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      setCpuData((prev) => {
        const lastCpu = prev[prev.length - 1].cpu;
        const next = genCpuPoint(lastCpu);
        return [...prev.slice(-29), next];
      });
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  /* ── Update Memory chart every 2s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      setMemData((prev) => {
        const lastMem = prev[prev.length - 1].memory;
        const next = genMemPoint(lastMem);
        return [...prev.slice(-29), next];
      });
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  /* ── Update Network chart every 2s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      setNetData((prev) => [...prev.slice(-14), genNetworkPoint()]);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  /* ── Agent progress auto-increment for busy agents ── */
  useEffect(() => {
    const interval = setInterval(() => {
      agents.forEach((agent) => {
        if (agent.status === 'busy' && agent.progress < 100) {
          const increment = Math.random() * 2 + 0.5;
          updateAgent(agent.id, { progress: Math.min(100, Math.round((agent.progress + increment) * 10) / 10) });
        }
      });
    }, 3000);
    return () => clearInterval(interval);
  }, [agents, updateAgent]);

  /* ── Agent CPU/RAM fluctuation every 4s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      agents.forEach((agent) => {
        if (agent.status === 'offline') return;
        const cpuDelta = Math.floor(Math.random() * 11) - 5;
        const memDelta = Math.floor(Math.random() * 7) - 3;
        const newCpu = Math.max(3, Math.min(95, agent.cpu + cpuDelta));
        const newMem = Math.max(5, Math.min(90, agent.memory + memDelta));
        updateAgent(agent.id, { cpu: newCpu, memory: newMem });
      });
    }, 4000);
    return () => clearInterval(interval);
  }, [agents, updateAgent]);

  /* ── Action handlers ── */
  const handlePauseResume = useCallback((id: string) => {
    const agent = agents.find((a) => a.id === id);
    if (!agent) return;
    if (agent.status === 'idle') {
      updateAgent(id, { status: 'online' });
      toast({ title: 'Agent Resumed', description: `${agent.name} is now online` });
    } else {
      updateAgent(id, { status: 'idle' });
      toast({ title: 'Agent Paused', description: `${agent.name} has been paused` });
    }
  }, [agents, updateAgent, toast]);

  const handleStop = useCallback((id: string) => {
    const agent = agents.find((a) => a.id === id);
    if (!agent) return;
    updateAgent(id, { status: 'offline', cpu: 0, memory: 0 });
    toast({ title: 'Agent Stopped', description: `${agent.name} is now offline`, variant: 'destructive' });
  }, [agents, updateAgent, toast]);

  const handleRestart = useCallback((id: string) => {
    const agent = agents.find((a) => a.id === id);
    if (!agent) return;
    updateAgent(id, { status: 'online', progress: 0, cpu: Math.floor(Math.random() * 20 + 15), memory: Math.floor(Math.random() * 15 + 20) });
    toast({ title: 'Agent Restarted', description: `${agent.name} has been restarted` });
  }, [agents, updateAgent, toast]);

  const handleLogs = useCallback((id: string) => {
    const agent = agents.find((a) => a.id === id);
    if (!agent) return;
    setActiveView('memory');
    toast({ title: 'Agent Logs', description: `Showing logs for ${agent.name}` });
  }, [agents, setActiveView, toast]);

  const activeCount = agents.filter((a) => a.status === 'online' || a.status === 'busy').length;

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4 grid-bg">
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bot className="h-4 w-4 text-cyber-cyan" />
          <h3 className="text-sm font-semibold text-foreground">Agent Fleet</h3>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
            </span>
            <span className="text-[10px] text-emerald-400 font-mono">{activeCount}/{agents.length} ACTIVE</span>
          </div>
        </div>
      </div>

      {/* ── Agent Cards Grid ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onPauseResume={handlePauseResume}
            onStop={handleStop}
            onRestart={handleRestart}
            onLogs={handleLogs}
          />
        ))}
      </div>

      {/* ── System Metrics Charts ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* CPU Usage */}
        <div className="cyber-panel p-4">
          <div className="flex items-center gap-2 mb-4">
            <Cpu className="h-4 w-4 text-cyber-cyan" />
            <h4 className="text-sm font-semibold text-foreground">CPU Usage</h4>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={cpuData} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#334155" tick={{ fontSize: 9 }} interval="preserveStartEnd" />
              <YAxis stroke="#334155" tick={{ fontSize: 9 }} domain={[0, 100]} />
              <RechartsTooltip content={<ChartTooltip />} />
              <Line
                type="monotone"
                dataKey="cpu"
                name="CPU"
                stroke="#00f0ff"
                strokeWidth={2}
                dot={false}
                animationDuration={400}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Memory Usage */}
        <div className="cyber-panel p-4">
          <div className="flex items-center gap-2 mb-4">
            <MemoryStick className="h-4 w-4 text-cyber-purple" />
            <h4 className="text-sm font-semibold text-foreground">Memory Usage</h4>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={memData} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
              <defs>
                <linearGradient id="memGradMonitor" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#7c3aed" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#7c3aed" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#334155" tick={{ fontSize: 9 }} interval="preserveStartEnd" />
              <YAxis stroke="#334155" tick={{ fontSize: 9 }} domain={[0, 100]} />
              <RechartsTooltip content={<ChartTooltip />} />
              <Area
                type="monotone"
                dataKey="memory"
                name="Memory"
                stroke="#7c3aed"
                strokeWidth={2}
                fill="url(#memGradMonitor)"
                animationDuration={400}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Network I/O */}
        <div className="cyber-panel p-4">
          <div className="flex items-center gap-2 mb-4">
            <Network className="h-4 w-4 text-cyber-blue" />
            <h4 className="text-sm font-semibold text-foreground">Network I/O</h4>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={netData} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#334155" tick={{ fontSize: 9 }} interval="preserveStartEnd" />
              <YAxis stroke="#334155" tick={{ fontSize: 9 }} />
              <RechartsTooltip content={<NetworkTooltip />} />
              <Legend
                iconType="circle"
                iconSize={6}
                wrapperStyle={{ fontSize: 10, color: '#94a3b8' }}
              />
              <Bar dataKey="networkIn" name="Upload" fill="#00f0ff" radius={[2, 2, 0, 0]} animationDuration={400} />
              <Bar dataKey="networkOut" name="Download" fill="#0ea5e9" radius={[2, 2, 0, 0]} animationDuration={400} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
