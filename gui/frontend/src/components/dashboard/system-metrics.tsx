'use client';

import { useState, useEffect } from 'react';
import type { SystemMetric } from '@/types';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip as RechartsTooltip, ResponsiveContainer,
} from 'recharts';

function ChartTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ name: string; value: number; color: string }>; label?: string }) {
  if (!active || !payload) return null;
  return (
    <div className="bg-surface-1 border border-border rounded-lg p-2.5 text-[10px] shadow-lg">
      <p className="text-muted-foreground mb-1.5 font-mono">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-foreground">{entry.name}:</span>
          <span className="font-mono" style={{ color: entry.color }}>{entry.value.toFixed(1)}{entry.name.includes('CPU') || entry.name.includes('Memory') ? '%' : ' MB/s'}</span>
        </p>
      ))}
    </div>
  );
}

async function fetchMetric(): Promise<SystemMetric> {
  try {
    const response = await fetch('/dashboard_data.json');
    const data = await response.json();
    const now = new Date();
    return {
      time: `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`,
      cpu: data.cpu?.percent || 0,
      memory: data.memory?.percent || 0,
      networkIn: 100 + Math.random() * 900,
      networkOut: 50 + Math.random() * 700,
    };
  } catch (error) {
    const now = new Date();
    return {
      time: `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`,
      cpu: 0,
      memory: 0,
      networkIn: 0,
      networkOut: 0,
    };
  }
}

export function SystemMetrics() {
  const [metrics, setMetrics] = useState<SystemMetric[]>([]);

  useEffect(() => {
    const initMetrics = async () => {
      const metric = await fetchMetric();
      setMetrics([metric]);
    };
    
    initMetrics();
    
    const interval = setInterval(async () => {
      const metric = await fetchMetric();
      setMetrics((prev) => [...prev.slice(-59), metric]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const currentCpu = metrics[metrics.length - 1]?.cpu ?? 0;
  const currentMemory = metrics[metrics.length - 1]?.memory ?? 0;
  const currentNetIn = metrics[metrics.length - 1]?.networkIn ?? 0;
  const currentNetOut = metrics[metrics.length - 1]?.networkOut ?? 0;

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4 grid-bg">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="cyber-panel p-3">
          <p className="text-[10px] text-muted-foreground mb-1">CPU Usage</p>
          <p className="text-lg font-mono font-bold text-cyber-cyan">{currentCpu.toFixed(1)}%</p>
        </div>
        <div className="cyber-panel p-3">
          <p className="text-[10px] text-muted-foreground mb-1">Memory Usage</p>
          <p className="text-lg font-mono font-bold text-cyber-purple">{currentMemory.toFixed(1)}%</p>
        </div>
        <div className="cyber-panel p-3">
          <p className="text-[10px] text-muted-foreground mb-1">Network In</p>
          <p className="text-lg font-mono font-bold text-emerald-400">{currentNetIn.toFixed(0)} MB/s</p>
        </div>
        <div className="cyber-panel p-3">
          <p className="text-[10px] text-muted-foreground mb-1">Network Out</p>
          <p className="text-lg font-mono font-bold text-amber-400">{currentNetOut.toFixed(0)} MB/s</p>
        </div>
      </div>

      {/* CPU Chart */}
      <div className="cyber-panel p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-foreground">CPU Usage</h3>
          <span className="text-[10px] text-muted-foreground font-mono">Last 60 samples</span>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={metrics} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="time" stroke="#334155" tick={{ fontSize: 9 }} interval="preserveStartEnd" />
            <YAxis stroke="#334155" tick={{ fontSize: 9 }} domain={[0, 100]} />
            <RechartsTooltip content={<ChartTooltip />} />
            <Line
              type="monotone"
              dataKey="cpu"
              name="CPU Usage"
              stroke="#00f0ff"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#00f0ff', stroke: '#0a0a0f', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Memory Chart */}
      <div className="cyber-panel p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-foreground">Memory Usage</h3>
          <span className="text-[10px] text-muted-foreground font-mono">Last 60 samples</span>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={metrics} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
            <defs>
              <linearGradient id="memGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#7c3aed" stopOpacity={0.4} />
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
              name="Memory Usage"
              stroke="#7c3aed"
              strokeWidth={2}
              fill="url(#memGrad)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Network Chart */}
      <div className="cyber-panel p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-foreground">Network I/O</h3>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-0.5 rounded bg-emerald-400" />
              <span className="text-[10px] text-muted-foreground">Inbound</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-0.5 rounded bg-amber-400" />
              <span className="text-[10px] text-muted-foreground">Outbound</span>
            </div>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={metrics.slice(-30)} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="time" stroke="#334155" tick={{ fontSize: 9 }} interval="preserveStartEnd" />
            <YAxis stroke="#334155" tick={{ fontSize: 9 }} />
            <RechartsTooltip content={<ChartTooltip />} />
            <Bar dataKey="networkIn" name="Network In" fill="#22c55e" radius={[2, 2, 0, 0]} opacity={0.8} />
            <Bar dataKey="networkOut" name="Network Out" fill="#eab308" radius={[2, 2, 0, 0]} opacity={0.8} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
