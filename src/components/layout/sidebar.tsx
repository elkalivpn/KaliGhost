'use client';

import {
  LayoutDashboard,
  Flame,
  GitBranch,
  TerminalSquare,
  Code2,
  Database,
  Activity,
  Settings,
  Shield,
  ChevronLeft,
  ChevronRight,
  Sparkles,
} from 'lucide-react';
import { useAppStore } from '@/stores/app-store';
import type { ActiveView } from '@/types';
import { cn } from '@/lib/utils';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

interface NavItem {
  view: ActiveView;
  label: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { view: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard className="h-5 w-5" /> },
  { view: 'dragon', label: 'Dragon Core', icon: <Flame className="h-5 w-5" /> },
  { view: 'orchestration', label: 'Orchestration', icon: <GitBranch className="h-5 w-5" /> },
  { view: 'terminal', label: 'Terminal', icon: <TerminalSquare className="h-5 w-5" /> },
  { view: 'editor', label: 'Editor', icon: <Code2 className="h-5 w-5" /> },
  { view: 'devlab', label: 'Dev Lab', icon: <Sparkles className="h-5 w-5" /> },
  { view: 'memory', label: 'Memory', icon: <Database className="h-5 w-5" /> },
  { view: 'monitor', label: 'Monitor', icon: <Activity className="h-5 w-5" /> },
  { view: 'config', label: 'Config', icon: <Settings className="h-5 w-5" /> },
];

export function Sidebar() {
  const { activeView, setActiveView, sidebarCollapsed, toggleSidebar } = useAppStore();

  return (
    <TooltipProvider delayDuration={0}>
      <aside
        className={cn(
          'relative flex flex-col h-full bg-surface-1 border-r border-border transition-all duration-300 ease-in-out',
          sidebarCollapsed ? 'w-16' : 'w-[280px]'
        )}
      >
        {/* Toggle Button */}
        <button
          onClick={toggleSidebar}
          className="absolute -right-3 top-6 z-50 h-6 w-6 rounded-full bg-surface-2 border border-border flex items-center justify-center text-muted-foreground hover:text-cyber-cyan hover:border-cyber-cyan/50 transition-all duration-200"
        >
          {sidebarCollapsed ? (
            <ChevronRight className="h-3 w-3" />
          ) : (
            <ChevronLeft className="h-3 w-3" />
          )}
        </button>

        {/* Logo Area */}
        <div className={cn(
          'flex items-center gap-3 px-4 py-5 border-b border-border',
          sidebarCollapsed && 'justify-center px-2'
        )}>
          <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-cyber-cyan/20 to-cyber-purple/20 flex items-center justify-center glow-cyan flex-shrink-0">
            <Shield className="h-5 w-5 text-cyber-cyan" />
          </div>
          {!sidebarCollapsed && (
            <div className="overflow-hidden">
              <h1 className="text-sm font-bold text-foreground truncate text-glow-cyan">
                Kali Dragon
              </h1>
              <p className="text-[10px] text-muted-foreground tracking-widest uppercase">
                Control Center
              </p>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-3 px-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = activeView === item.view;
            const button = (
              <button
                key={item.view}
                onClick={() => setActiveView(item.view)}
                className={cn(
                  'w-full flex items-center gap-3 rounded-lg transition-all duration-200 group',
                  sidebarCollapsed ? 'justify-center p-2.5' : 'px-3 py-2.5',
                  isActive
                    ? 'bg-cyber-cyan/10 text-cyber-cyan glow-cyan'
                    : 'text-muted-foreground hover:text-foreground hover:bg-surface-2'
                )}
              >
                <span className={cn(
                  'flex-shrink-0 transition-transform duration-200',
                  isActive && 'drop-shadow-[0_0_6px_rgba(0,240,255,0.5)]'
                )}>
                  {item.icon}
                </span>
                {!sidebarCollapsed && (
                  <span className="text-sm font-medium truncate">{item.label}</span>
                )}
                {!sidebarCollapsed && isActive && (
                  <div className="ml-auto w-1.5 h-1.5 rounded-full bg-cyber-cyan animate-status-pulse" />
                )}
              </button>
            );

            if (sidebarCollapsed) {
              return (
                <Tooltip key={item.view}>
                  <TooltipTrigger asChild>
                    {button}
                  </TooltipTrigger>
                  <TooltipContent side="right" className="bg-surface-2 border-border text-foreground">
                    {item.label}
                  </TooltipContent>
                </Tooltip>
              );
            }
            return button;
          })}
        </nav>

        {/* Bottom Section */}
        <div className={cn(
          'px-4 py-4 border-t border-border',
          sidebarCollapsed && 'px-2'
        )}>
          <div className={cn(
            'flex items-center gap-3',
            sidebarCollapsed && 'justify-center'
          )}>
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-cyber-cyan/20 to-cyber-red/20 flex items-center justify-center flex-shrink-0">
              <Flame className="h-4 w-4 text-cyber-cyan" />
            </div>
            {!sidebarCollapsed && (
              <div className="overflow-hidden">
                <p className="text-xs font-medium text-foreground truncate">Dragon Engine</p>
                <p className="text-[10px] text-emerald-400">v3.2.1</p>
              </div>
            )}
          </div>
        </div>

        {/* Right glow border */}
        <div className="absolute top-0 right-0 w-px h-full bg-gradient-to-b from-transparent via-cyber-cyan/10 to-transparent" />
      </aside>
    </TooltipProvider>
  );
}
