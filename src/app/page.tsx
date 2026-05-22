'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { useWebSocketConnection } from '@/hooks/useWebSocketConnection';
import { useAppStore } from '@/stores/app-store';
import { Sidebar } from '@/components/layout/sidebar';
import { TopBar } from '@/components/layout/top-bar';

// Dynamic imports for heavy components (no SSR)
const DragonView = dynamic(
  () => import('@/components/dragon/dragon-scene').then((mod) => ({ default: mod.DragonView })),
  { ssr: false, loading: () => <DragonLoader /> }
);

const MainDashboard = dynamic(
  () => import('@/components/dashboard/main-dashboard').then((mod) => ({ default: mod.MainDashboard })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const AgentMonitor = dynamic(
  () => import('@/components/dashboard/agent-monitor').then((mod) => ({ default: mod.AgentMonitor })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const SystemMetrics = dynamic(
  () => import('@/components/dashboard/system-metrics').then((mod) => ({ default: mod.SystemMetrics })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const WorkflowCanvas = dynamic(
  () => import('@/components/orchestration/workflow-canvas').then((mod) => ({ default: mod.WorkflowCanvas })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const TerminalPanel = dynamic(
  () => import('@/components/terminal/terminal-panel').then((mod) => ({ default: mod.TerminalPanel })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const CodeEditor = dynamic(
  () => import('@/components/editor/code-editor').then((mod) => ({ default: mod.CodeEditor })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const MemoryBrowser = dynamic(
  () => import('@/components/memory/memory-browser').then((mod) => ({ default: mod.MemoryBrowser })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const ConfigPanel = dynamic(
  () => import('@/components/config/config-panel').then((mod) => ({ default: mod.ConfigPanel })),
  { ssr: false, loading: () => <PanelLoader /> }
);

const DevLab = dynamic(
  () => import('@/components/devlab/dev-lab').then((mod) => ({ default: mod.DevLab })),
  { ssr: false, loading: () => <PanelLoader /> }
);

function PanelLoader() {
  return (
    <div className="h-full w-full flex items-center justify-center bg-surface-0">
      <div className="flex flex-col items-center gap-3">
        <div className="h-8 w-8 border-2 border-cyber-cyan/20 border-t-cyber-cyan rounded-full animate-spin" />
        <span className="text-[10px] text-muted-foreground font-mono">Loading module...</span>
      </div>
    </div>
  );
}

function DragonLoader() {
  return (
    <div className="h-full w-full flex items-center justify-center bg-surface-0 relative overflow-hidden">
      <div className="absolute inset-0 grid-bg" />
      <div className="relative flex flex-col items-center gap-4">
        <div className="relative">
          <div className="h-16 w-16 border-2 border-cyber-cyan/20 border-t-cyber-cyan rounded-full animate-spin" />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-6 w-6 rounded-full bg-cyber-cyan/10 glow-cyan animate-pulse" />
          </div>
        </div>
        <div className="text-center">
          <p className="text-sm text-foreground font-medium mb-1">Initializing Dragon Core</p>
          <p className="text-[10px] text-muted-foreground font-mono animate-cyber-pulse">Loading 3D engine...</p>
        </div>
      </div>
    </div>
  );
}

function StatusBar() {
  const [time, setTime] = useState('');
  const { activeAgentsCount, memoryUsage } = useAppStore();

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(now.toLocaleTimeString('en-US', { hour12: false }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center justify-between h-6 px-3 bg-surface-1 border-t border-border text-[9px] font-mono text-muted-foreground shrink-0 select-none">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-status-pulse" />
          <span className="text-emerald-400">CONNECTED</span>
        </div>
        <span className="text-muted-foreground/60">|</span>
        <span>Agents: <span className="text-cyber-cyan">{activeAgentsCount}</span> active</span>
        <span className="text-muted-foreground/60">|</span>
        <span>Memory: <span className="text-cyber-purple">{memoryUsage}%</span></span>
        <span className="text-muted-foreground/60">|</span>
        <span>Dragon Core: <span className="text-emerald-400">ONLINE</span></span>
      </div>
      <div className="flex items-center gap-4">
        <span>{time}</span>
        <span className="text-muted-foreground/60">|</span>
        <span>v3.2.1</span>
      </div>
    </div>
  );
}

function ActiveViewRenderer() {
  const { activeView } = useAppStore();

  switch (activeView) {
    case 'dashboard':
      return <MainDashboard />;
    case 'dragon':
      return <DragonView />;
    case 'orchestration':
      return <WorkflowCanvas />;
    case 'terminal':
      return <TerminalPanel />;
    case 'editor':
      return <CodeEditor />;
    case 'memory':
      return <MemoryBrowser />;
    case 'monitor':
      return (
        <div className="h-full overflow-y-auto p-4 space-y-4 grid-bg">
          <AgentMonitor />
          <SystemMetrics />
        </div>
      );
    case 'config':
      return <ConfigPanel />;
    case 'devlab':
      return <DevLab />;
    default:
      return <MainDashboard />;
  }
}

export default function Home() {
  const { isConnected } = useWebSocketConnection();

  return (
    <div className="h-screen w-screen flex flex-col bg-surface-0 overflow-hidden">
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar />
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {/* Top Bar */}
          <TopBar />
          {/* Content */}
          <main className="flex-1 overflow-hidden">
            <ActiveViewRenderer />
          </main>
          {/* Status Bar */}
          <StatusBar />
        </div>
      </div>
    </div>
  );
}
