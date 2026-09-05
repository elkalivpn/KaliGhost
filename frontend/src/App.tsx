import { useState } from 'react'
import { useAppStore } from '../store/appStore'
import { ThreatVisualization3D } from './components/3d/ThreatVisualization3D'
import { TerminalPanel } from './components/panels/TerminalPanel'
import { AgentChatPanel } from './components/panels/AgentChatPanel'
import { AgentConfigPanel } from './components/panels/AgentConfigPanel'
import { DashboardPanel } from './components/panels/DashboardPanel'
import { 
  LayoutDashboard, 
  Terminal, 
  MessageSquare, 
  Settings, 
  Menu, 
  X,
  Ghost,
  Maximize2
} from 'lucide-react'

function App() {
  const { activePanels, togglePanel, visualizationMode } = useAppStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [activeTab, setActiveTab] = useState<'dashboard' | 'agent' | 'config'>('dashboard')
  
  const navItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { id: 'agent', icon: MessageSquare, label: 'AI Agent' },
    { id: 'config', icon: Settings, label: 'Configuration' },
  ] as const
  
  return (
    <div className="flex h-screen bg-bg-primary cyber-grid">
      {/* Sidebar */}
      <div className={`flex flex-col bg-bg-secondary border-r border-border-color transition-all duration-300 ${
        sidebarOpen ? 'w-64' : 'w-16'
      }`}>
        {/* Logo */}
        <div className="flex items-center justify-between p-4 border-b border-border-color">
          {sidebarOpen && (
            <div className="flex items-center gap-2">
              <Ghost className="w-6 h-6 text-accent-cyan" />
              <span className="font-bold glow-text">KaliGhost</span>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-1 hover:bg-bg-tertiary rounded transition-colors"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 p-2 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded transition-colors ${
                activeTab === item.id
                  ? 'bg-accent-purple/20 text-accent-purple border border-accent-purple/50'
                  : 'text-text-secondary hover:bg-bg-tertiary hover:text-text-primary'
              }`}
            >
              <item.icon className="w-5 h-5" />
              {sidebarOpen && <span>{item.label}</span>}
            </button>
          ))}
        </nav>
        
        {/* Quick Toggles */}
        {sidebarOpen && (
          <div className="p-4 border-t border-border-color">
            <div className="space-y-2">
              <p className="text-xs text-text-secondary font-bold mb-2">ACTIVE PANELS</p>
              {['terminal', 'agent-chat'].map((panel) => (
                <button
                  key={panel}
                  onClick={() => togglePanel(panel)}
                  className={`w-full flex items-center justify-between px-2 py-1.5 rounded text-xs ${
                    activePanels.includes(panel)
                      ? 'bg-accent-green/20 text-accent-green'
                      : 'bg-bg-tertiary text-text-secondary'
                  }`}
                >
                  <span className="capitalize">{panel.replace('-', ' ')}</span>
                  <Maximize2 className="w-3 h-3" />
                </button>
              ))}
            </div>
          </div>
        )}
        
        {/* Version */}
        {sidebarOpen && (
          <div className="p-4 border-t border-border-color">
            <p className="text-xs text-text-secondary">v1.0.0 - Nexus Edition</p>
            <p className="text-xs text-accent-cyan mt-1">Uncensored Mode Active</p>
          </div>
        )}
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <div className="flex items-center justify-between px-6 py-3 bg-bg-secondary/50 border-b border-border-color backdrop-blur">
          <h1 className="text-xl font-bold glow-text">
            {activeTab === 'dashboard' && 'Operations Dashboard'}
            {activeTab === 'agent' && 'Yrays AI Agent'}
            {activeTab === 'config' && 'System Configuration'}
          </h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-bg-tertiary rounded border border-border-color">
              <div className="w-2 h-2 bg-accent-green rounded-full animate-pulse" />
              <span className="text-xs">System Online</span>
            </div>
          </div>
        </div>
        
        {/* Content Area */}
        <div className="flex-1 flex overflow-hidden relative">
          {/* 3D Visualization Background */}
          {visualizationMode !== 'none' && (
            <ThreatVisualization3D mode={visualizationMode} />
          )}
          
          {/* Panels Container */}
          <div className="flex-1 flex gap-4 p-4 overflow-hidden relative z-10">
            {/* Left Panel - Dynamic based on tab */}
            <div className="w-96 flex-shrink-0 overflow-y-auto">
              {activeTab === 'dashboard' && <DashboardPanel />}
              {activeTab === 'agent' && <AgentChatPanel />}
              {activeTab === 'config' && <AgentConfigPanel />}
            </div>
            
            {/* Right Panel - Terminal (always visible when active) */}
            {activePanels.includes('terminal') && (
              <div className="flex-1 min-w-[400px]">
                <TerminalPanel />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
