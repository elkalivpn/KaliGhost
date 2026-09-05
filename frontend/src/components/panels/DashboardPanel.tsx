import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { Activity, Globe, Shield, Eye, Zap, Lock, AlertTriangle, CheckCircle } from 'lucide-react'

export function DashboardPanel() {
  const { visualizationMode, setVisualizationMode, securityStatus, workspace } = useAppStore()
  
  const stats = [
    { label: 'Active Projects', value: '3', icon: Activity, color: 'text-accent-cyan' },
    { label: 'CVEs Indexed', value: '127,842', icon: Shield, color: 'text-accent-green' },
    { label: 'Network Nodes', value: '24', icon: Globe, color: 'text-accent-purple' },
    { label: 'Threats Detected', value: '7', icon: AlertTriangle, color: 'text-accent-red' },
  ]
  
  const recentOperations = [
    { id: 1, type: 'Malware Analysis', target: 'sample_2024_01.exe', status: 'completed', time: '2 min ago' },
    { id: 2, type: 'CVE Search', target: 'CVE-2024-1234', status: 'completed', time: '15 min ago' },
    { id: 3, type: 'Purple Team', target: '192.168.1.0/24', status: 'running', time: '1 hour ago' },
    { id: 4, type: 'Steganography', target: 'covert_channel.png', status: 'completed', time: '3 hours ago' },
  ]
  
  return (
    <div className="flex flex-col h-full gap-4 overflow-y-auto p-4">
      {/* Quick Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="bg-bg-secondary border border-border-color rounded-lg p-3 glow-border hover:border-accent-cyan/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
              <span className="text-xs text-text-secondary">{stat.label}</span>
            </div>
            <p className="text-2xl font-bold">{stat.value}</p>
          </div>
        ))}
      </div>
      
      {/* Visualization Mode Selector */}
      <div className="bg-bg-secondary border border-border-color rounded-lg p-4">
        <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
          <Eye className="w-4 h-4 text-accent-cyan" />
          3D Visualization Mode
        </h3>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2">
          <VisualizationButton
            mode="none"
            label="Disabled"
            active={visualizationMode === 'none'}
            onClick={() => setVisualizationMode('none')}
          />
          <VisualizationButton
            mode="threat"
            label="Threat Map"
            active={visualizationMode === 'threat'}
            onClick={() => setVisualizationMode('threat')}
          />
          <VisualizationButton
            mode="network"
            label="Network Topology"
            active={visualizationMode === 'network'}
            onClick={() => setVisualizationMode('network')}
          />
          <VisualizationButton
            mode="malware"
            label="Malware Structure"
            active={visualizationMode === 'malware'}
            onClick={() => setVisualizationMode('malware')}
          />
        </div>
      </div>
      
      {/* Security Status */}
      <div className="bg-bg-secondary border border-border-color rounded-lg p-4">
        <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
          <Shield className="w-4 h-4 text-accent-green" />
          Security Status
        </h3>
        <div className="grid grid-cols-2 gap-2">
          <SecurityStatusItem
            label="Encryption"
            active={securityStatus.encryptionActive}
            icon={<Lock className="w-3 h-3" />}
          />
          <SecurityStatusItem
            label="Tor Routing"
            active={securityStatus.torEnabled}
            icon={<Globe className="w-3 h-3" />}
          />
          <SecurityStatusItem
            label="RAM Only Mode"
            active={securityStatus.ramOnlyMode}
            icon={<Zap className="w-3 h-3" />}
          />
          <SecurityStatusItem
            label="Dead Man's Switch"
            active={securityStatus.deadMansSwitch}
            icon={<AlertTriangle className="w-3 h-3" />}
          />
        </div>
      </div>
      
      {/* Recent Operations */}
      <div className="bg-bg-secondary border border-border-color rounded-lg p-4 flex-1">
        <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
          <Activity className="w-4 h-4 text-accent-purple" />
          Recent Operations
        </h3>
        <div className="space-y-2">
          {recentOperations.map((op) => (
            <div
              key={op.id}
              className="flex items-center justify-between p-2 bg-bg-tertiary rounded border border-border-color hover:border-accent-cyan/30 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${
                  op.status === 'running' ? 'bg-accent-green animate-pulse' : 'bg-text-secondary'
                }`} />
                <div>
                  <p className="text-sm font-medium">{op.type}</p>
                  <p className="text-xs text-text-secondary">{op.target}</p>
                </div>
              </div>
              <div className="text-right">
                <span className={`text-xs px-2 py-0.5 rounded ${
                  op.status === 'running'
                    ? 'bg-accent-green/20 text-accent-green'
                    : 'bg-bg-primary text-text-secondary'
                }`}>
                  {op.status}
                </span>
                <p className="text-xs text-text-secondary mt-1">{op.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Workspace Info */}
      <div className="bg-bg-secondary border border-border-color rounded-lg p-4">
        <h3 className="text-sm font-bold mb-3">Current Workspace</h3>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm">Mode: <span className="text-accent-cyan font-bold uppercase">{workspace.mode}</span></p>
            <p className="text-xs text-text-secondary">Project: {workspace.activeProject || 'None'}</p>
          </div>
          {workspace.isRunning && (
            <CheckCircle className="w-5 h-5 text-accent-green" />
          )}
        </div>
      </div>
    </div>
  )
}

interface VisualizationButtonProps {
  mode: string
  label: string
  active: boolean
  onClick: () => void
}

function VisualizationButton({ mode, label, active, onClick }: VisualizationButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-2 rounded text-sm transition-all ${
        active
          ? 'bg-accent-cyan/20 text-accent-cyan border border-accent-cyan'
          : 'bg-bg-tertiary text-text-secondary border border-border-color hover:border-accent-cyan/30'
      }`}
    >
      {label}
    </button>
  )
}

interface SecurityStatusItemProps {
  label: string
  active: boolean
  icon: React.ReactNode
}

function SecurityStatusItem({ label, active, icon }: SecurityStatusItemProps) {
  return (
    <div className={`flex items-center gap-2 p-2 rounded ${
      active ? 'bg-accent-green/10' : 'bg-bg-tertiary'
    }`}>
      <span className={active ? 'text-accent-green' : 'text-text-secondary'}>
        {icon}
      </span>
      <span className={`text-xs ${active ? 'text-accent-green font-bold' : 'text-text-secondary'}`}>
        {label}: {active ? 'ACTIVE' : 'OFF'}
      </span>
    </div>
  )
}
