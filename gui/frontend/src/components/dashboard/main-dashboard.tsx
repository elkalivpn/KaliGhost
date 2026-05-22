'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  Bot, Cpu, MemoryStick, Network,
  Plus, Rocket, Scan, FileBarChart,
  ArrowUpRight, ArrowDownRight, Clock,
  Info, CheckCircle2, AlertTriangle, AlertCircle,
  Activity, Zap,
} from 'lucide-react';
import { memo } from 'react';
import { useAppStore } from '@/stores/app-store';
import { useToast } from '@/hooks/use-toast';
import type { SystemMetric, ActivityEvent } from '@/types';
import { cn } from '@/lib/utils';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip as RechartsTooltip, ResponsiveContainer,
} from 'recharts';

/* ───────────── Animated Counter ───────────── */
function AnimatedCounter({ target, suffix = '' }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);
  const prevTarget = useRef(target);

  useEffect(() => {
    const start = prevTarget.current;
    const end = target;
    const duration = 800;
    const startTime = performance.now();

    function animate(now: number) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCount(Math.round(start + (end - start) * eased));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }
    requestAnimationFrame(animate);
    prevTarget.current = target;
  }, [target]);

  return <span className="font-mono font-bold">{Math.floor(count)}{suffix}</span>;
}

/* ───────────── Mini Sparkline ───────────── */
function MiniSparkline({ data, color }: { data: number[]; color: string }) {
  if (data.length < 2) return null;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const w = 48;
  const h = 20;
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg width={w} height={h} className="opacity-60">
      <polyline fill="none" stroke={color} strokeWidth="1.5" points={points} />
    </svg>
  );
}

/* ───────────── Stat Card ───────────── */
const StatCard = memo(function StatCard({
  icon,
  label,
  value,
  suffix,
  change,
  changeType,
  sparkData,
  sparkColor,
  iconBg,
  glowColor,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  suffix?: string;
  change?: string;
  changeType?: 'up' | 'down';
  sparkData: number[];
  sparkColor: string;
  iconBg: string;
  glowColor: string;
}) {
  return (
    <div
      className={cn(
        'cyber-panel p-4 group transition-all duration-300',
        'hover:border-opacity-50',
        glowColor
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <div
          className="h-9 w-9 rounded-lg flex items-center justify-center transition-all duration-300"
          style={{ backgroundColor: iconBg }}
        >
          {icon}
        </div>
        {change && (
          <div className="flex flex-col items-end gap-1">
            <div
              className={cn(
                'flex items-center gap-0.5 text-[10px] font-mono',
                changeType === 'up' ? 'text-emerald-400' : 'text-cyber-red'
              )}
            >
              {changeType === 'up' ? (
                <ArrowUpRight className="h-3 w-3" />
              ) : (
                <ArrowDownRight className="h-3 w-3" />
              )}
              {change}
            </div>
            <MiniSparkline data={sparkData} color={sparkColor} />
          </div>
        )}
      </div>
      <p className="text-[11px] text-muted-foreground mb-1">{label}</p>
      <p className="text-xl text-foreground">
        <AnimatedCounter target={value} suffix={suffix} />
      </p>
    </div>
  );
});

/* ───────────── Event Type Helpers ───────────── */
const eventTypeColors: Record<string, string> = {
  info: 'text-cyber-blue',
  success: 'text-emerald-400',
  warning: 'text-amber-400',
  error: 'text-cyber-red',
};

const eventTypeDots: Record<string, string> = {
  info: 'bg-cyber-blue',
  success: 'bg-emerald-400',
  warning: 'bg-amber-400',
  error: 'bg-cyber-red',
};

const eventTypeIcons: Record<string, React.ReactNode> = {
  info: <Info className="h-3 w-3" />,
  success: <CheckCircle2 className="h-3 w-3" />,
  warning: <AlertTriangle className="h-3 w-3" />,
  error: <AlertCircle className="h-3 w-3" />,
};

/* ───────────── Recharts Tooltip ───────────── */
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

/* ───────────── Metric Generator ───────────── */
function generateMetric(): SystemMetric {
  const now = new Date();
  return {
    time: `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`,
    cpu: 25 + Math.random() * 45,
    memory: 55 + Math.random() * 20,
    networkIn: 200 + Math.random() * 800,
    networkOut: 100 + Math.random() * 600,
  };
}

/* ───────────── Activity Event Generator ───────────── */
const eventTemplates = [
  { action: 'Discovered {count} new hosts on subnet', target: '192.168.1.0/24', type: 'success' as const },
  { action: 'Open port detected', target: '10.0.0.{port}:{service}', type: 'info' as const },
  { action: 'Vulnerability confirmed', target: 'CVE-2024-{cve}', type: 'warning' as const },
  { action: 'IDS alert triggered', target: 'Snort: ET SCAN', type: 'error' as const },
  { action: 'DNS enumeration complete for', target: 'target-{n}.local', type: 'success' as const },
  { action: 'Payload compiled successfully', target: 'reverse_tcp staged', type: 'info' as const },
  { action: 'Executive report generated', target: 'Pentest-2024-Q{n}', type: 'success' as const },
  { action: 'Service fingerprint match', target: '{service} {version}', type: 'info' as const },
  { action: 'Credentials harvested', target: '{user}:{pass}@target', type: 'warning' as const },
  { action: 'Firewall rule bypassed', target: 'iptables chain OUTPUT', type: 'success' as const },
  { action: 'Web shell uploaded to', target: '/var/www/html/uploads/', type: 'warning' as const },
  { action: 'Database dump in progress', target: 'mysql://{host}:3306', type: 'info' as const },
  { action: 'Privilege escalation successful on', target: '10.0.0.{ip}', type: 'success' as const },
  { action: 'Connection timeout to', target: '192.168.1.{ip}:443', type: 'error' as const },
  { action: 'SSL certificate extracted from', target: '*.target.com', type: 'info' as const },
  { action: 'Wireless network discovered', target: 'WLAN-{ssid} (WPA2)', type: 'success' as const },
  { action: 'Exploit failed on target', target: '10.0.0.{ip} - EAGAIN', type: 'error' as const },
  { action: 'Reverse shell established on', target: '10.0.0.{ip}:4444', type: 'success' as const },
];

function fillTemplate(template: string): string {
  return template
    .replace('{count}', String(Math.floor(Math.random() * 20 + 3)))
    .replace('{port}', String(Math.floor(Math.random() * 9000 + 1000)))
    .replace('{service}', ['Apache 2.4.52', 'nginx 1.18', 'OpenSSH 8.9', 'MySQL 8.0', 'Redis 7.0'][Math.floor(Math.random() * 5)])
    .replace('{version}', `${Math.floor(Math.random() * 3)}.${Math.floor(Math.random() * 10)}.${Math.floor(Math.random() * 30)}`)
    .replace('{cve}', String(Math.floor(Math.random() * 9000 + 1000)))
    .replace('{n}', String(Math.floor(Math.random() * 50 + 1)))
    .replace('{user}', ['admin', 'root', 'www-data', 'postgres', 'jenkins'][Math.floor(Math.random() * 5)])
    .replace('{pass}', '••••••••')
    .replace('{host}', `10.0.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254 + 1)}`)
    .replace('{ip}', String(Math.floor(Math.random() * 254 + 1)))
    .replace('{ssid}', `CORP-${String.fromCharCode(65 + Math.floor(Math.random() * 26))}${Math.floor(Math.random() * 99)}`);
}

function timeAgo(seconds: number): string {
  if (seconds < 60) return `${seconds}s ago`;
  const m = Math.floor(seconds / 60);
  if (m < 60) return `${m}m ago`;
  return `${Math.floor(m / 60)}h ago`;
}

/* ───────────── Main Dashboard ───────────── */
export function MainDashboard() {
  const {
    agents, activeView, setActiveView,
      
  } = useAppStore();
  const { toast } = useToast();

  const activeAgentsCount = agents.filter((a) => a.status === 'online' || a.status === 'busy').length;

  /* ── Stats state ── */
  const [processes, setProcesses] = useState(23);
  const [memUsage, setMemUsage] = useState(67);
  const [netIO, setNetIO] = useState(1.2);

  /* ── Sparkline history ── */
  const [agentSpark] = useState(() => Array.from({ length: 10 }, () => activeAgentsCount));
  const [processSpark, setProcessSpark] = useState(() => Array.from({ length: 10 }, () => 23));
  const [memSpark, setMemSpark] = useState(() => Array.from({ length: 10 }, () => 67));
  const [netSpark, setNetSpark] = useState(() => Array.from({ length: 10 }, () => 1.2));

  /* ── Process count update every 5s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      setProcesses((prev) => {
        const next = Math.max(10, Math.min(80, prev + Math.floor(Math.random() * 11) - 5));
        setProcessSpark((s) => [...s.slice(-9), next]);
        return next;
      });
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  /* ── Memory update every 3s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      setMemUsage((prev) => {
        const next = Math.max(55, Math.min(75, prev + (Math.random() * 10 - 5)));
        const rounded = Math.round(next);
        setMemSpark((s) => [...s.slice(-9), rounded]);
        return rounded;
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  /* ── Network IO update every 4s ── */
  useEffect(() => {
    const interval = setInterval(() => {
      setNetIO((prev) => {
        const next = Math.max(0.3, Math.min(3.5, prev + (Math.random() * 1.0 - 0.5)));
        const rounded = Math.round(next * 10) / 10;
        setNetSpark((s) => [...s.slice(-9), rounded]);
        return rounded;
      });
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  /* ── Performance chart data ── */
  const [metrics, setMetrics] = useState<SystemMetric[]>(() =>
    Array.from({ length: 30 }, () => generateMetric())
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics((prev) => [...prev.slice(-29), generateMetric()]);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  /* ── Activity timeline ── */
  const agentNames = agents.map((a) => a.name);
  const [events, setEvents] = useState<ActivityEvent[]>(() => {
    const initial: ActivityEvent[] = [];
    for (let i = 0; i < 8; i++) {
      const tpl = eventTemplates[Math.floor(Math.random() * eventTemplates.length)];
      initial.push({
        id: `init-${i}`,
        agent: agentNames[Math.floor(Math.random() * agentNames.length)],
        action: tpl.action,
        target: fillTemplate(tpl.target),
        timestamp: timeAgo(i * 12 + Math.floor(Math.random() * 10)),
        type: tpl.type,
      });
    }
    return initial;
  });

  const eventIdRef = useRef(0);
  const addEvent = useCallback(() => {
    const tpl = eventTemplates[Math.floor(Math.random() * eventTemplates.length)];
    const newEvent: ActivityEvent = {
      id: `evt-${++eventIdRef.current}`,
      agent: agentNames[Math.floor(Math.random() * agentNames.length)],
      action: tpl.action,
      target: fillTemplate(tpl.target),
      timestamp: 'just now',
      type: tpl.type,
    };
    setEvents((prev) => [newEvent, ...prev].slice(0, 20));
  }, [agentNames]);

  useEffect(() => {
    const delay = 8000 + Math.random() * 2000;
    const addFirst = setTimeout(() => {
      addEvent();
      const interval = setInterval(() => {
        addEvent();
      }, 8000 + Math.random() * 2000);
      return () => clearInterval(interval);
    }, delay);
    return () => clearTimeout(addFirst);
  }, [addEvent]);

  /* ── Age timestamps periodically ── */
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => setTick((t) => t + 1), 5000);
    return () => clearInterval(interval);
  }, []);

  const displayEvents = events.map((e, i) => ({
    ...e,
    timestamp: i === 0 ? 'just now' : timeAgo((i + 1) * 12),
  }));

  /* ── Quick actions ── */
  const handleNewAgent = () => {
    setActiveView('orchestration');
    toast({ title: 'Navigating', description: 'Opening orchestration view to create a new agent' });
  };
  const handleDeploy = () => {
    toast({ title: 'Deployment Initiated', description: 'Agents are being deployed to target infrastructure...' });
  };
  const handleScan = () => {
    toast({ title: 'Network Scan Started', description: 'Scanning 192.168.1.0/24 — this may take a moment' });
  };
  const handleReport = () => {
    setActiveView('memory');
    toast({ title: 'Report View', description: 'Switching to memory view for full activity report' });
  };

  /* ── Event click ── */
  const handleEventClick = (event: ActivityEvent) => {
    toast({
      title: `${event.agent}`,
      description: `${event.action} → ${event.target}`,
    });
  };

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4 grid-bg">
      {/* ── Stats Grid ── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={<Bot className="h-5 w-5 text-cyber-cyan" />}
          label="Active Agents"
          value={activeAgentsCount}
          change="+2"
          changeType="up"
          sparkData={agentSpark}
          sparkColor="#00f0ff"
          iconBg="rgba(0,240,255,0.1)"
          glowColor="hover:glow-cyan"
        />
        <StatCard
          icon={<Cpu className="h-5 w-5 text-cyber-blue" />}
          label="Running Processes"
          value={processes}
          change="+5"
          changeType="up"
          sparkData={processSpark}
          sparkColor="#0ea5e9"
          iconBg="rgba(14,165,233,0.1)"
          glowColor="hover:glow-cyan"
        />
        <StatCard
          icon={<MemoryStick className="h-5 w-5 text-cyber-purple" />}
          label="Memory Usage"
          value={memUsage}
          suffix="%"
          change="-3%"
          changeType="down"
          sparkData={memSpark}
          sparkColor="#7c3aed"
          iconBg="rgba(124,58,237,0.1)"
          glowColor="hover:glow-cyan"
        />
        <StatCard
          icon={<Network className="h-5 w-5 text-cyber-red" />}
          label="Network I/O"
          value={netIO}
          suffix=" GB/s"
          change="+0.3"
          changeType="up"
          sparkData={netSpark}
          sparkColor="#ef4444"
          iconBg="rgba(239,68,68,0.1)"
          glowColor="hover:glow-cyan"
        />
      </div>

      {/* ── Two Column Layout ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Activity Timeline */}
        <div className="cyber-panel p-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-cyber-cyan" />
              <h3 className="text-sm font-semibold text-foreground">Agent Activity</h3>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
              </span>
              <span className="text-[10px] text-emerald-400 font-mono font-medium">LIVE</span>
            </div>
          </div>
          <div className="space-y-1 max-h-80 overflow-y-auto pr-1 custom-scrollbar">
            {displayEvents.map((event) => (
              <button
                key={event.id}
                type="button"
                className="w-full flex items-start gap-3 p-2 rounded-md hover:bg-surface-2/50 transition-colors text-left cursor-pointer"
                onClick={() => handleEventClick(event)}
              >
                <div className={cn(
                  'mt-0.5 flex-shrink-0 w-5 h-5 rounded flex items-center justify-center',
                  eventTypeColors[event.type],
                  'bg-opacity-10'
                )}
                  style={{ backgroundColor: `${event.type === 'info' ? '#0ea5e9' : event.type === 'success' ? '#22c55e' : event.type === 'warning' ? '#eab308' : '#ef4444'}15` }}
                >
                  {eventTypeIcons[event.type]}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-medium text-foreground truncate">{event.agent}</span>
                  </div>
                  <p className={cn('text-[10px] leading-relaxed truncate', eventTypeColors[event.type])}>
                    {event.action} <span className="text-muted-foreground font-mono">{event.target}</span>
                  </p>
                  <span className="text-[9px] text-muted-foreground/60 flex items-center gap-0.5 mt-0.5">
                    <Clock className="h-2.5 w-2.5" />
                    {event.timestamp}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* System Performance Chart */}
        <div className="cyber-panel p-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Zap className="h-4 w-4 text-cyber-cyan" />
              <h3 className="text-sm font-semibold text-foreground">System Performance</h3>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-0.5 rounded bg-cyber-cyan" />
                <span className="text-[10px] text-muted-foreground">CPU</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-0.5 rounded bg-cyber-purple" />
                <span className="text-[10px] text-muted-foreground">RAM</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={metrics} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
              <defs>
                <linearGradient id="cpuGradDash" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#00f0ff" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#00f0ff" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="ramGradDash" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#7c3aed" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#7c3aed" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#334155" tick={{ fontSize: 10 }} interval="preserveStartEnd" />
              <YAxis stroke="#334155" tick={{ fontSize: 10 }} domain={[0, 100]} />
              <RechartsTooltip content={<ChartTooltip />} />
              <Area
                type="monotone"
                dataKey="cpu"
                name="CPU"
                stroke="#00f0ff"
                strokeWidth={2}
                fill="url(#cpuGradDash)"
                animationDuration={500}
              />
              <Area
                type="monotone"
                dataKey="memory"
                name="Memory"
                stroke="#7c3aed"
                strokeWidth={2}
                fill="url(#ramGradDash)"
                animationDuration={500}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Quick Actions ── */}
      <div className="cyber-panel p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">Quick Actions</h3>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={handleNewAgent}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-surface-2 border border-border hover:border-cyber-cyan/40 hover:bg-cyber-cyan/5 hover:glow-cyan transition-all duration-200 group cursor-pointer"
          >
            <Plus className="h-4 w-4 text-cyber-cyan group-hover:scale-110 transition-transform" />
            <span className="text-xs text-muted-foreground group-hover:text-cyber-cyan transition-colors">New Agent</span>
          </button>
          <button
            type="button"
            onClick={handleDeploy}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-surface-2 border border-border hover:border-emerald-400/40 hover:bg-emerald-400/5 transition-all duration-200 group cursor-pointer"
          >
            <Rocket className="h-4 w-4 text-emerald-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs text-muted-foreground group-hover:text-emerald-400 transition-colors">Deploy</span>
          </button>
          <button
            type="button"
            onClick={handleScan}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-surface-2 border border-border hover:border-amber-400/40 hover:bg-amber-400/5 transition-all duration-200 group cursor-pointer"
          >
            <Scan className="h-4 w-4 text-amber-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs text-muted-foreground group-hover:text-amber-400 transition-colors">Scan Network</span>
          </button>
          <button
            type="button"
            onClick={handleReport}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-surface-2 border border-border hover:border-cyber-purple/40 hover:bg-cyber-purple/5 transition-all duration-200 group cursor-pointer"
          >
            <FileBarChart className="h-4 w-4 text-cyber-purple group-hover:scale-110 transition-transform" />
            <span className="text-xs text-muted-foreground group-hover:text-cyber-purple transition-colors">Report</span>
          </button>
        </div>
      </div>
    </div>
  );
}
