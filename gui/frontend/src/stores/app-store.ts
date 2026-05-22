import { create } from 'zustand';
import type { Agent, ActiveView } from '@/types';

interface AppState {
  activeView: ActiveView;
  sidebarCollapsed: boolean;
  agents: Agent[];
  runningProcesses: number;
  memoryUsage: number;
  networkIO: string;

  setActiveView: (view: ActiveView) => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setAgents: (agents: Agent[]) => void;
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  setRunningProcesses: (count: number) => void;
  setMemoryUsage: (usage: number) => void;
  setNetworkIO: (io: string) => void;
}

// TODO: Replace with real agent data from API
const defaultAgents: Agent[] = [];

export const useAppStore = create<AppState>((set) => ({
  activeView: 'dashboard',
  sidebarCollapsed: false,
  agents: defaultAgents,
  runningProcesses: 0,
  memoryUsage: 0,
  networkIO: '0 GB/s',

  setActiveView: (view) => set({ activeView: view }),
  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
  setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
  setAgents: (agents) => set({ agents }),
  updateAgent: (id, updates) =>
    set((state) => ({
      agents: state.agents.map((a) => (a.id === id ? { ...a, ...updates } : a)),
    })),
  setRunningProcesses: (count) => set({ runningProcesses: count }),
  setMemoryUsage: (usage) => set({ memoryUsage: usage }),
  setNetworkIO: (io) => set({ networkIO: io }),
}));
