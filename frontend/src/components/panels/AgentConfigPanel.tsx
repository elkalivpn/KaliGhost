import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { Settings, Shield, Cpu, Network, Eye, Lock, Zap } from 'lucide-react'

export function AgentConfigPanel() {
  const { agentConfig, setAgentConfig, securityStatus, updateSecurityStatus } = useAppStore()
  const [showSystemPrompt, setShowSystemPrompt] = useState(false)
  
  const models = [
    { id: 'uncensored-v1', name: 'Yrays Uncensored v1', description: 'Full capabilities, no restrictions' },
    { id: 'security-expert', name: 'Security Expert', description: 'Specialized in vulnerability analysis' },
    { id: 'malware-analyst', name: 'Malware Analyst', description: 'Reverse engineering specialist' },
    { id: 'exploit-dev', name: 'Exploit Developer', description: '0-day exploit creation' },
    { id: 'redteam-auto', name: 'Red Team Autonomous', description: 'Autonomous penetration testing' },
    { id: 'code-obfuscation', name: 'Code Obfuscation', description: 'Polymorphic code generation' },
  ]
  
  return (
    <div className="bg-bg-secondary border border-border-color rounded-lg p-4 glow-border">
      <div className="flex items-center gap-2 mb-4">
        <Cpu className="w-5 h-5 text-accent-cyan" />
        <h3 className="text-lg font-bold glow-text">Yrays Agent Configuration</h3>
      </div>
      
      {/* Model Selection */}
      <div className="mb-4">
        <label className="block text-sm text-text-secondary mb-2">AI Model</label>
        <select
          value={agentConfig.model}
          onChange={(e) => setAgentConfig({ model: e.target.value })}
          className="w-full bg-bg-tertiary border border-border-color rounded px-3 py-2 text-text-primary focus:border-accent-purple outline-none"
        >
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name} - {model.description}
            </option>
          ))}
        </select>
      </div>
      
      {/* Temperature Slider */}
      <div className="mb-4">
        <label className="block text-sm text-text-secondary mb-2">
          Temperature: {agentConfig.temperature}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={agentConfig.temperature}
          onChange={(e) => setAgentConfig({ temperature: parseFloat(e.target.value) })}
          className="w-full accent-accent-purple"
        />
        <div className="flex justify-between text-xs text-text-secondary">
          <span>Precise</span>
          <span>Creative</span>
        </div>
      </div>
      
      {/* Max Tokens */}
      <div className="mb-4">
        <label className="block text-sm text-text-secondary mb-2">
          Max Tokens: {agentConfig.maxTokens}
        </label>
        <input
          type="range"
          min="256"
          max="8192"
          step="256"
          value={agentConfig.maxTokens}
          onChange={(e) => setAgentConfig({ maxTokens: parseInt(e.target.value) })}
          className="w-full accent-accent-cyan"
        />
      </div>
      
      {/* Autonomous Mode Toggle */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Zap className={`w-4 h-4 ${agentConfig.autonomousMode ? 'text-accent-red' : 'text-text-secondary'}`} />
          <span className="text-sm">Autonomous Mode</span>
        </div>
        <button
          onClick={() => setAgentConfig({ autonomousMode: !agentConfig.autonomousMode })}
          className={`px-3 py-1 rounded text-sm transition-all ${
            agentConfig.autonomousMode
              ? 'bg-accent-red text-white pulse-red'
              : 'bg-bg-tertiary text-text-secondary'
          }`}
        >
          {agentConfig.autonomousMode ? 'ACTIVE' : 'OFF'}
        </button>
      </div>
      
      {/* Uncensored Toggle */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Lock className={`w-4 h-4 ${agentConfig.uncensored ? 'text-accent-green' : 'text-text-secondary'}`} />
          <span className="text-sm">Uncensored Mode</span>
        </div>
        <button
          onClick={() => setAgentConfig({ uncensored: !agentConfig.uncensored })}
          className={`px-3 py-1 rounded text-sm transition-all ${
            agentConfig.uncensored
              ? 'bg-accent-green text-black font-bold'
              : 'bg-bg-tertiary text-text-secondary'
          }`}
        >
          {agentConfig.uncensored ? 'ENABLED' : 'DISABLED'}
        </button>
      </div>
      
      {/* System Prompt Editor */}
      <div className="mb-4">
        <button
          onClick={() => setShowSystemPrompt(!showSystemPrompt)}
          className="flex items-center gap-2 text-sm text-accent-cyan hover:text-accent-purple transition-colors"
        >
          <Settings className="w-4 h-4" />
          {showSystemPrompt ? 'Hide' : 'Edit'} System Prompt
        </button>
        
        {showSystemPrompt && (
          <textarea
            value={agentConfig.systemPrompt}
            onChange={(e) => setAgentConfig({ systemPrompt: e.target.value })}
            rows={8}
            className="mt-2 w-full bg-bg-tertiary border border-border-color rounded px-3 py-2 text-text-primary text-sm font-mono focus:border-accent-purple outline-none resize-none"
            placeholder="Enter custom system prompt..."
          />
        )}
      </div>
      
      {/* Security Status */}
      <div className="border-t border-border-color pt-4 mt-4">
        <h4 className="text-sm font-bold text-text-secondary mb-3 flex items-center gap-2">
          <Shield className="w-4 h-4" />
          Active Security Features
        </h4>
        
        <div className="grid grid-cols-2 gap-2">
          <SecurityToggle
            icon={<Lock className="w-3 h-3" />}
            label="Encryption"
            active={securityStatus.encryptionActive}
            onClick={() => updateSecurityStatus({ encryptionActive: !securityStatus.encryptionActive })}
          />
          <SecurityToggle
            icon={<Network className="w-3 h-3" />}
            label="Tor Routing"
            active={securityStatus.torEnabled}
            onClick={() => updateSecurityStatus({ torEnabled: !securityStatus.torEnabled })}
          />
          <SecurityToggle
            icon={<Cpu className="w-3 h-3" />}
            label="RAM Only"
            active={securityStatus.ramOnlyMode}
            onClick={() => updateSecurityStatus({ ramOnlyMode: !securityStatus.ramOnlyMode })}
          />
          <SecurityToggle
            icon={<Eye className="w-3 h-3" />}
            label="Dead Man's Switch"
            active={securityStatus.deadMansSwitch}
            onClick={() => updateSecurityStatus({ deadMansSwitch: !securityStatus.deadMansSwitch })}
          />
        </div>
      </div>
    </div>
  )
}

interface SecurityToggleProps {
  icon: React.ReactNode
  label: string
  active: boolean
  onClick: () => void
}

function SecurityToggle({ icon, label, active, onClick }: SecurityToggleProps) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-2 py-1.5 rounded text-xs transition-all ${
        active
          ? 'bg-accent-green/20 text-accent-green border border-accent-green/50'
          : 'bg-bg-tertiary text-text-secondary border border-border-color'
      }`}
    >
      {icon}
      {label}
    </button>
  )
}
