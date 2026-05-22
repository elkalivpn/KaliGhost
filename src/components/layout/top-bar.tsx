'use client';

import { Search, Bell, Cpu, MemoryStick, Wifi } from 'lucide-react';
import { useAppStore } from '@/stores/app-store';

const viewLabels: Record<string, string> = {
  dashboard: 'Dashboard',
  dragon: 'Dragon Core',
  orchestration: 'Orchestration',
  terminal: 'Terminal',
  editor: 'Code Editor',
  memory: 'Memory Browser',
  monitor: 'System Monitor',
  config: 'Configuration',
};

export function TopBar() {
  const { activeView, sidebarCollapsed } = useAppStore();

  return (
    <header suppressHydrationWarning className="relative flex items-center h-12 px-4 bg-surface-1 border-b border-border shrink-0">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 min-w-0 mr-4">
        <span className="text-xs text-muted-foreground truncate">
          Kali Dragon
        </span>
        <span className="text-xs text-muted-foreground/40">/</span>
        <span className="text-xs text-cyber-cyan font-medium truncate">
          {viewLabels[activeView] || activeView}
        </span>
      </div>

      {/* Search Bar */}
      <div className="flex-1 max-w-md mx-auto">
        <div className="relative group">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground group-focus-within:text-cyber-cyan transition-colors" />
          <input
            type="text"
            placeholder="Search agents, commands, logs..."
            className="w-full h-8 pl-9 pr-4 text-xs bg-surface-2 border border-border rounded-lg text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-cyber-cyan/50 focus:ring-1 focus:ring-cyber-cyan/20 transition-all duration-200"
          />
          <kbd className="absolute right-2 top-1/2 -translate-y-1/2 hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 text-[10px] font-mono text-muted-foreground bg-surface-0 border border-border rounded">
            ⌘K
          </kbd>
        </div>
      </div>

      {/* System Indicators */}
      <div className="flex items-center gap-3 ml-4">
        <div className="hidden sm:flex items-center gap-1.5 px-2 py-1 rounded-md bg-surface-2 border border-border text-[10px]">
          <Cpu className="h-3 w-3 text-cyber-cyan" />
          <span className="text-muted-foreground">CPU</span>
          <span className="text-foreground font-mono font-medium">42%</span>
        </div>
        <div className="hidden md:flex items-center gap-1.5 px-2 py-1 rounded-md bg-surface-2 border border-border text-[10px]">
          <MemoryStick className="h-3 w-3 text-cyber-cyan" />
          <span className="text-muted-foreground">RAM</span>
          <span className="text-foreground font-mono font-medium">67%</span>
        </div>
        <div className="hidden lg:flex items-center gap-1.5 px-2 py-1 rounded-md bg-surface-2 border border-border text-[10px]">
          <Wifi className="h-3 w-3 text-emerald-400" />
          <span className="text-emerald-400 font-mono font-medium">1.2 GB/s</span>
        </div>

        {/* Divider */}
        <div className="w-px h-5 bg-border" />

        {/* Notifications */}
        <button className="relative p-1.5 rounded-md hover:bg-surface-2 transition-colors">
          <Bell className="h-4 w-4 text-muted-foreground hover:text-foreground transition-colors" />
          <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-cyber-red rounded-full animate-status-pulse" />
        </button>

        {/* User Avatar */}
        <div className="h-7 w-7 rounded-full bg-gradient-to-br from-cyber-cyan/30 to-cyber-purple/30 border border-cyber-cyan/20 flex items-center justify-center">
          <span className="text-[10px] font-bold text-cyber-cyan">R</span>
        </div>
      </div>

      {/* Bottom glow line */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyber-cyan/20 to-transparent" />
    </header>
  );
}
