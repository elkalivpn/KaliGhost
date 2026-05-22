'use client';

import { useState, useCallback } from 'react';
import {
  Settings, Globe, Gauge, Shield, Puzzle, Save, RotateCcw,
  ChevronDown, ChevronRight, Eye, EyeOff, Plus, Trash2,
  Bot, MessageSquare, Key, Download, Upload, Cpu, Sparkles,
  Braces, FileJson, Copy, Check, Wifi, WifiOff, Zap, RefreshCw,
  ExternalLink, AlertCircle, CheckCircle2, XCircle, Loader2, Wrench,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Switch } from '@/components/ui/switch';
import type { AgentConfig } from '@/types';
import {
  useProvidersStore,
  type ProviderConfig,
  type ConnectionMode,
  type ProviderStatus,
} from '@/stores/providers-store';

/* ── Shared form components ── */

function SectionHeader({ title, icon, open, onToggle }: {
  title: string; icon: React.ReactNode; open: boolean; onToggle: () => void;
}) {
  return (
    <button
      onClick={onToggle}
      className="w-full flex items-center justify-between px-4 py-3 hover:bg-surface-2/50 transition-colors rounded-t-lg"
    >
      <div className="flex items-center gap-2.5">
        <span className="text-cyber-cyan">{icon}</span>
        <span className="text-xs font-medium text-foreground">{title}</span>
      </div>
      {open
        ? <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
        : <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />}
    </button>
  );
}

function Field({ label, hint, children }: { label: string; hint?: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-[11px] text-muted-foreground font-medium">{label}</label>
      {hint && <p className="text-[9px] text-muted-foreground/60">{hint}</p>}
      {children}
    </div>
  );
}

function Input({ defaultValue, type = 'text', placeholder, mono = false }: {
  defaultValue?: string; type?: string; placeholder?: string; mono?: boolean;
}) {
  return (
    <input
      type={type}
      defaultValue={defaultValue}
      placeholder={placeholder}
      className={cn(
        'h-8 px-3 text-xs bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-cyber-cyan/50 transition-all',
        mono && 'font-mono text-[11px]'
      )}
    />
  );
}

function TextArea({ defaultValue, rows = 3, placeholder, mono = false }: {
  defaultValue?: string; rows?: number; placeholder?: string; mono?: boolean;
}) {
  return (
    <textarea
      defaultValue={defaultValue}
      rows={rows}
      placeholder={placeholder}
      className={cn(
        'w-full px-3 py-2 text-xs bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-cyber-cyan/50 transition-all resize-none',
        mono && 'font-mono text-[11px]'
      )}
    />
  );
}

function Toggle({ label, description, defaultChecked = false }: {
  label: string; description: string; defaultChecked?: boolean;
}) {
  const [checked, setChecked] = useState(defaultChecked);
  return (
    <div className="flex items-center justify-between py-1.5">
      <div>
        <p className="text-[11px] text-foreground">{label}</p>
        <p className="text-[10px] text-muted-foreground">{description}</p>
      </div>
      <Switch checked={checked} onCheckedChange={setChecked} />
    </div>
  );
}

function Section({ title, icon, children, defaultOpen = false }: {
  title: string; icon: React.ReactNode; children: React.ReactNode; defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="cyber-panel overflow-hidden">
      <SectionHeader title={title} icon={icon} open={open} onToggle={() => setOpen(!open)} />
      {open && (
        <div className="px-4 pb-4 border-t border-border pt-3 space-y-4">
          {children}
        </div>
      )}
    </div>
  );
}

/* ── Agent Prompt Configuration ── */

const defaultAgents: AgentConfig[] = [
  {
    id: 'agent-001', name: 'Recon Agent',
    systemPrompt: 'You are a reconnaissance specialist AI agent integrated into Kali Linux. Your mission is to perform passive and active reconnaissance on target networks. Use tools like Nmap, nslookup, whois, and Shodan to gather intelligence. Always report findings in structured format with risk assessments.',
    model: 'claude-sonnet-4-20250514', temperature: 0.3, maxTokens: 4096, topP: 0.9,
    frequencyPenalty: 0.0, presencePenalty: 0.0, tools: ['nmap', 'nslookup', 'whois', 'shodan', 'theharvester'],
    autoExecute: false, retryOnFail: true, maxRetries: 3, timeout: 120,
  },
  {
    id: 'agent-002', name: 'Scanner Agent',
    systemPrompt: 'You are a vulnerability scanning specialist. Perform comprehensive port scans, service enumeration, and vulnerability detection. Prioritize findings by CVSS score. Use Nmap NSE scripts, Nikto for web scanning, and enum4linux for SMB enumeration.',
    model: 'claude-sonnet-4-20250514', temperature: 0.2, maxTokens: 8192, topP: 0.95,
    frequencyPenalty: 0.0, presencePenalty: 0.0, tools: ['nmap', 'nikto', 'enum4linux', 'gobuster'],
    autoExecute: true, retryOnFail: true, maxRetries: 5, timeout: 300,
  },
  {
    id: 'agent-003', name: 'Exploit Agent',
    systemPrompt: 'You are an authorized penetration testing agent. Only operate on explicitly authorized targets. Attempt exploitation based on vulnerability findings. Use Metasploit, searchsploit, and custom payloads. Always document every step for the final report.',
    model: 'claude-opus-4-20250514', temperature: 0.1, maxTokens: 16384, topP: 0.85,
    frequencyPenalty: 0.1, presencePenalty: 0.1, tools: ['metasploit', 'searchsploit', 'sqlmap', 'hydra'],
    autoExecute: false, retryOnFail: true, maxRetries: 2, timeout: 600,
  },
  {
    id: 'agent-004', name: 'Report Agent',
    systemPrompt: 'You are a technical report writer specialized in penetration testing reports. Compile findings from all agents into professional executive summaries and detailed technical reports. Include risk ratings, remediation advice, and compliance mappings (OWASP, NIST, CIS).',
    model: 'claude-sonnet-4-20250514', temperature: 0.4, maxTokens: 16384, topP: 0.9,
    frequencyPenalty: 0.0, presencePenalty: 0.0, tools: ['report_generator', 'pdf_export', 'chart_builder'],
    autoExecute: true, retryOnFail: true, maxRetries: 3, timeout: 180,
  },
  {
    id: 'agent-005', name: 'Monitor Agent',
    systemPrompt: 'You are a real-time monitoring agent. Watch IDS/IPS alerts, network traffic anomalies, and system logs. Alert on suspicious patterns, potential intrusions, and policy violations. Maintain a running dashboard of security posture.',
    model: 'claude-haiku-4-20250514', temperature: 0.2, maxTokens: 4096, topP: 0.9,
    frequencyPenalty: 0.0, presencePenalty: 0.0, tools: ['tcpdump', 'snort', 'fail2ban', 'log_monitor'],
    autoExecute: true, retryOnFail: true, maxRetries: 5, timeout: 60,
  },
  {
    id: 'agent-006', name: 'Custom Agent',
    systemPrompt: 'You are a versatile AI agent that can be configured for any task. Define your own behavior through the system prompt. You have access to a wide range of tools and can adapt to different cybersecurity scenarios.',
    model: 'claude-sonnet-4-20250514', temperature: 0.7, maxTokens: 8192, topP: 0.95,
    frequencyPenalty: 0.0, presencePenalty: 0.0, tools: ['bash', 'python', 'curl', 'custom_tools'],
    autoExecute: false, retryOnFail: false, maxRetries: 1, timeout: 300,
  },
];

function AgentPromptEditor() {
  const [selectedAgent, setSelectedAgent] = useState(0);
  const [agent, setAgent] = useState<AgentConfig>(defaultAgents[0]);
  const [activeTab, setActiveTab] = useState<'prompt' | 'model' | 'tools' | 'advanced'>('prompt');

  const handleSelectAgent = useCallback((index: number) => {
    setSelectedAgent(index);
    setAgent({ ...defaultAgents[index] });
  }, []);

  const update = (partial: Partial<AgentConfig>) => setAgent((prev) => ({ ...prev, ...partial }));

  return (
    <div className="flex gap-3">
      {/* Agent list sidebar */}
      <div className="w-[180px] shrink-0 space-y-1">
        <p className="text-[10px] text-muted-foreground font-mono mb-2 tracking-wider uppercase">Select Agent</p>
        {defaultAgents.map((a, i) => (
          <button
            key={a.id}
            onClick={() => handleSelectAgent(i)}
            className={cn(
              'w-full text-left px-2.5 py-2 rounded-md text-[11px] transition-all',
              selectedAgent === i
                ? 'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20'
                : 'text-muted-foreground hover:text-foreground hover:bg-surface-2 border border-transparent'
            )}
          >
            <div className="flex items-center gap-2">
              <Bot className="h-3.5 w-3.5 shrink-0" />
              <span className="truncate font-medium">{a.name}</span>
            </div>
          </button>
        ))}
        <button className="w-full flex items-center justify-center gap-1.5 px-2.5 py-2 rounded-md text-[10px] text-muted-foreground hover:text-cyber-cyan border border-dashed border-border hover:border-cyber-cyan/30 transition-all mt-2">
          <Plus className="h-3 w-3" /> Add Agent
        </button>
      </div>

      {/* Agent config area */}
      <div className="flex-1 min-w-0">
        {/* Tab navigation */}
        <div className="flex items-center gap-1 mb-3 border-b border-border pb-2">
          {[
            { id: 'prompt' as const, label: 'System Prompt', icon: <MessageSquare className="h-3 w-3" /> },
            { id: 'model' as const, label: 'Model & Params', icon: <Cpu className="h-3 w-3" /> },
            { id: 'tools' as const, label: 'Tools & Actions', icon: <Braces className="h-3 w-3" /> },
            { id: 'advanced' as const, label: 'Advanced', icon: <Settings className="h-3 w-3" /> },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={cn(
                'flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-[10px] transition-all',
                activeTab === tab.id
                  ? 'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20'
                  : 'text-muted-foreground hover:text-foreground border border-transparent'
              )}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Prompt Tab */}
        {activeTab === 'prompt' && (
          <div className="space-y-3">
            <Field label="Agent Name" hint="Display name for this agent">
              <Input defaultValue={agent.name} onChange={(e) => update({ name: e.target.value })} />
            </Field>
            <Field label="System Prompt" hint="Instructions that define the agent's behavior and personality">
              <TextArea
                defaultValue={agent.systemPrompt}
                rows={10}
                mono
                onChange={(e) => update({ systemPrompt: e.target.value })}
              />
            </Field>
            <div className="flex items-center gap-3">
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-surface-2 border border-border text-[10px] text-muted-foreground hover:text-cyber-cyan transition-all">
                <Copy className="h-3 w-3" /> Copy Template
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-surface-2 border border-border text-[10px] text-muted-foreground hover:text-cyber-cyan transition-all">
                <Sparkles className="h-3 w-3" /> AI Optimize Prompt
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-surface-2 border border-border text-[10px] text-muted-foreground hover:text-cyber-cyan transition-all">
                <RotateCcw className="h-3 w-3" /> Reset
              </button>
            </div>
          </div>
        )}

        {/* Model Tab */}
        {activeTab === 'model' && (
          <div className="grid grid-cols-2 gap-4">
            <Field label="AI Model" hint="Base model for this agent">
              <select
                value={agent.model}
                onChange={(e) => update({ model: e.target.value })}
                className="w-full h-8 px-3 text-xs bg-surface-0 border border-border rounded-md text-foreground focus:outline-none focus:border-cyber-cyan/50 transition-all"
              >
                <option value="claude-opus-4-20250514">Claude Opus 4 (Most Capable)</option>
                <option value="claude-sonnet-4-20250514">Claude Sonnet 4 (Balanced)</option>
                <option value="claude-haiku-4-20250514">Claude Haiku 4 (Fast & Cheap)</option>
                <option value="gpt-4o">GPT-4o (OpenAI)</option>
                <option value="gpt-4o-mini">GPT-4o Mini (Fast)</option>
                <option value="deepseek-v3">DeepSeek V3</option>
                <option value="llama-3.1-70b">Llama 3.1 70B (Local)</option>
                <option value="custom">Custom Model Endpoint</option>
              </select>
            </Field>
            <Field label="Max Tokens" hint="Maximum response length">
              <Input type="number" defaultValue={String(agent.maxTokens)} />
            </Field>
            <Field label="Temperature" hint="Creativity level (0 = deterministic, 1 = creative)">
              <div className="flex items-center gap-2">
                <input
                  type="range" min="0" max="100"
                  defaultValue={Math.round(agent.temperature * 100)}
                  className="flex-1 h-1 accent-cyber-cyan"
                />
                <span className="text-[11px] font-mono text-cyber-cyan w-8 text-right">{agent.temperature.toFixed(1)}</span>
              </div>
            </Field>
            <Field label="Top P" hint="Nucleus sampling threshold">
              <div className="flex items-center gap-2">
                <input
                  type="range" min="0" max="100"
                  defaultValue={Math.round(agent.topP * 100)}
                  className="flex-1 h-1 accent-cyber-cyan"
                />
                <span className="text-[11px] font-mono text-cyber-cyan w-8 text-right">{agent.topP.toFixed(2)}</span>
              </div>
            </Field>
            <Field label="Frequency Penalty" hint="Reduce repetition of frequent tokens">
              <div className="flex items-center gap-2">
                <input type="range" min="0" max="200" defaultValue={Math.round(agent.frequencyPenalty * 100)} className="flex-1 h-1 accent-cyber-purple" />
                <span className="text-[11px] font-mono text-cyber-purple w-8 text-right">{agent.frequencyPenalty.toFixed(1)}</span>
              </div>
            </Field>
            <Field label="Presence Penalty" hint="Encourage talking about new topics">
              <div className="flex items-center gap-2">
                <input type="range" min="0" max="200" defaultValue={Math.round(agent.presencePenalty * 100)} className="flex-1 h-1 accent-cyber-purple" />
                <span className="text-[11px] font-mono text-cyber-purple w-8 text-right">{agent.presencePenalty.toFixed(1)}</span>
              </div>
            </Field>
          </div>
        )}

        {/* Tools Tab */}
        {activeTab === 'tools' && (
          <div className="space-y-3">
            <Field label="Available Tools" hint="Tools this agent can invoke">
              <div className="flex flex-wrap gap-1.5">
                {agent.tools.map((tool, i) => (
                  <span key={i} className="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-cyber-cyan/10 text-[10px] text-cyber-cyan border border-cyber-cyan/20 font-mono">
                    {tool}
                    <button className="hover:text-cyber-red transition-colors"><Trash2 className="h-2.5 w-2.5" /></button>
                  </span>
                ))}
                <button className="inline-flex items-center gap-1 px-2 py-1 rounded-md border border-dashed border-border text-[10px] text-muted-foreground hover:text-cyber-cyan hover:border-cyber-cyan/30 transition-all">
                  <Plus className="h-2.5 w-2.5" /> Add Tool
                </button>
              </div>
            </Field>
            <Toggle label="Auto-execute" description="Execute agent actions without confirmation" defaultChecked={agent.autoExecute} />
            <Toggle label="Retry on failure" description="Automatically retry failed operations" defaultChecked={agent.retryOnFail} />
            <Field label="Max Retries">
              <Input type="number" defaultValue={String(agent.maxRetries)} />
            </Field>
            <Field label="Timeout (seconds)">
              <Input type="number" defaultValue={String(agent.timeout)} />
            </Field>
          </div>
        )}

        {/* Advanced Tab */}
        {activeTab === 'advanced' && (
          <div className="space-y-3">
            <Field label="Custom API Endpoint" hint="Override default model endpoint">
              <Input placeholder="https://api.example.com/v1/chat/completions" mono />
            </Field>
            <Field label="Agent-Specific Environment Variables" hint="JSON format">
              <TextArea defaultValue='{\n  "RECON_TIMEOUT": "60",\n  "MAX_CONCURRENT_SCANS": "5"\n}' mono rows={4} />
            </Field>
            <Field label="Pre-execution Hook" hint="Command/script to run before agent executes">
              <TextArea placeholder="#!/bin/bash\necho 'Starting agent...'" mono rows={3} />
            </Field>
            <Field label="Post-execution Hook" hint="Command/script to run after agent finishes">
              <TextArea placeholder="#!/bin/bash\necho 'Agent completed'" mono rows={3} />
            </Field>
            <Toggle label="Log all interactions" description="Save every agent interaction to memory" defaultChecked={true} />
            <Toggle label="Stream responses" description="Show real-time streaming output" defaultChecked={true} />
          </div>
        )}
      </div>
    </div>
  );
}

/* ── Environment Variables ── */

interface EnvVar { key: string; value: string; masked: boolean; }

const defaultEnvVars: EnvVar[] = [
  { key: 'OPENAI_API_KEY', value: 'sk-proj-xxxx...REDACTED', masked: true },
  { key: 'ANTHROPIC_API_KEY', value: 'sk-ant-xxxx...REDACTED', masked: true },
  { key: 'DATABASE_URL', value: 'postgresql://localhost:5432/dragon', masked: false },
  { key: 'REDIS_URL', value: 'redis://localhost:6379', masked: false },
  { key: 'PROXY_URL', value: 'socks5://127.0.0.1:9050', masked: false },
  { key: 'WORKSPACE_PATH', value: '/opt/kali-dragon/workspace', masked: false },
  { key: 'LOG_LEVEL', value: 'INFO', masked: false },
  { key: 'MAX_CONCURRENT_AGENTS', value: '10', masked: false },
];

function EnvVarManager() {
  const [vars, setVars] = useState<EnvVar[]>(defaultEnvVars);
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');
  const [copied, setCopied] = useState(false);

  const addVar = () => {
    if (!newKey.trim()) return;
    setVars((prev) => [...prev, { key: newKey.trim(), value: newValue, masked: newValue.includes('key') || newValue.includes('secret') || newValue.includes('token') }]);
    setNewKey('');
    setNewValue('');
  };

  const removeVar = (index: number) => setVars((prev) => prev.filter((_, i) => i !== index));

  const toggleMask = (index: number) => setVars((prev) => prev.map((v, i) => i === index ? { ...v, masked: !v.masked } : v));

  const copyAll = () => {
    const envStr = vars.map((v) => `${v.key}=${v.value}`).join('\n');
    navigator.clipboard?.writeText(envStr);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <p className="text-[10px] text-muted-foreground font-mono">{vars.length} variables</p>
        <button onClick={copyAll} className="flex items-center gap-1 px-2 py-1 rounded text-[10px] text-muted-foreground hover:text-cyber-cyan transition-all">
          {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
          {copied ? 'Copied' : 'Copy .env'}
        </button>
      </div>
      <div className="space-y-1 max-h-[300px] overflow-y-auto">
        {vars.map((v, i) => (
          <div key={i} className="flex items-center gap-2 group">
            <span className="text-[11px] font-mono text-cyber-cyan min-w-[160px] truncate">{v.key}</span>
            <span className="text-muted-foreground/40">=</span>
            <span className="flex-1 text-[11px] font-mono text-foreground truncate">
              {v.masked ? '•'.repeat(12) : v.value}
            </span>
            <button onClick={() => toggleMask(i)} className="opacity-0 group-hover:opacity-100 transition-opacity">
              {v.masked ? <Eye className="h-3 w-3 text-muted-foreground hover:text-foreground" /> : <EyeOff className="h-3 w-3 text-muted-foreground hover:text-foreground" />}
            </button>
            <button onClick={() => removeVar(i)} className="opacity-0 group-hover:opacity-100 transition-opacity">
              <Trash2 className="h-3 w-3 text-muted-foreground hover:text-cyber-red" />
            </button>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-2 pt-2 border-t border-border">
        <Input placeholder="KEY" value={newKey} onChange={(e) => setNewKey(e.target.value)} mono />
        <Input placeholder="value" value={newValue} onChange={(e) => setNewValue(e.target.value)} mono className="flex-1" />
        <button onClick={addVar} className="px-2 py-1 rounded-md bg-cyber-cyan/10 border border-cyber-cyan/30 text-[10px] text-cyber-cyan hover:bg-cyber-cyan/20 transition-all">
          <Plus className="h-3 w-3" />
        </button>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════
 *  PROVIDERS & API KEYS — Gestion completo de proveedores
 *  Default: modo local. Sin APIs externas.
 * ══════════════════════════════════════════════════════════ */

function StatusDot({ status }: { status: ProviderStatus }) {
  const config = {
    disconnected: { color: 'bg-muted-foreground/40', label: 'Sin configurar' },
    testing: { color: 'bg-amber-400 animate-pulse', label: 'Probando...' },
    connected: { color: 'bg-emerald-400', label: 'Conectado' },
    error: { color: 'bg-cyber-red', label: 'Error' },
  }[status];
  return (
    <span className={cn('inline-flex items-center gap-1 text-[9px] font-mono',
      status === 'connected' ? 'text-emerald-400' : status === 'error' ? 'text-cyber-red' : status === 'testing' ? 'text-amber-400' : 'text-muted-foreground/50'
    )}>
      <span className={cn('w-1.5 h-1.5 rounded-full', config?.color)} />
      {config?.label}
    </span>
  );
}

function ProviderCard({ provider }: { provider: ProviderConfig }) {
  const { updateProvider, resetProvider } = useProvidersStore();
  const [showKey, setShowKey] = useState(false);
  const [localKey, setLocalKey] = useState(provider.apiKey);
  const [localUrl, setLocalUrl] = useState(provider.baseUrl);
  const [localModel, setLocalModel] = useState(provider.model);

  const isLocal = !provider.isPaid && (provider.id === 'ollama' || provider.id === 'lmstudio' || provider.id === 'custom');

  const handleSave = () => {
    updateProvider(provider.id, {
      apiKey: localKey,
      baseUrl: localUrl,
      model: localModel,
      enabled: !!localKey || isLocal,
    });
  };

  const handleTest = async () => {
    updateProvider(provider.id, { status: 'testing' });
    // Simular test — en produccion esto haria un fetch real al endpoint
    setTimeout(() => {
      const hasKey = localKey || isLocal;
      updateProvider(provider.id, {
        status: hasKey ? 'connected' : 'error',
        enabled: hasKey || isLocal,
      });
    }, 1500);
  };

  const needsKey = !isLocal;

  return (
    <div className={cn(
      'rounded-lg border p-3 transition-all',
      provider.enabled
        ? 'bg-surface-1 border-cyber-cyan/20'
        : 'bg-surface-0 border-border hover:border-border/80'
    )}>
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-base">{provider.icon}</span>
          <div>
            <p className="text-[11px] font-medium text-foreground flex items-center gap-2">
              {provider.name}
              {provider.isPaid && (
                <span className="text-[8px] px-1.5 py-0.5 rounded-full bg-amber-400/10 text-amber-400 border border-amber-400/20">PAID</span>
              )}
              {isLocal && (
                <span className="text-[8px] px-1.5 py-0.5 rounded-full bg-emerald-400/10 text-emerald-400 border border-emerald-400/20">LOCAL</span>
              )}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <StatusDot status={provider.status} />
          <Switch
            checked={provider.enabled}
            onCheckedChange={(checked) => updateProvider(provider.id, { enabled: checked })}
          />
        </div>
      </div>

      <p className="text-[10px] text-muted-foreground mb-3 leading-relaxed">{provider.description}</p>

      {/* Fields */}
      <div className="space-y-2">
        {/* API Key */}
        {needsKey && (
          <div className="flex items-center gap-2">
            <div className="flex-1 relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={localKey}
                onChange={(e) => setLocalKey(e.target.value)}
                placeholder={isLocal ? 'No necesaria' : 'sk-... o tu API key'}
                className="w-full h-7 px-3 text-[10px] font-mono bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-cyber-cyan/50 transition-all pr-8"
              />
              <button
                onClick={() => setShowKey(!showKey)}
                className="absolute right-1.5 top-1/2 -translate-y-1/2 text-muted-foreground/50 hover:text-foreground"
              >
                {showKey ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
              </button>
            </div>
          </div>
        )}

        {/* Base URL */}
        <div className="flex items-center gap-2">
          <span className="text-[9px] text-muted-foreground/60 w-8 shrink-0">URL</span>
          <input
            type="text"
            value={localUrl}
            onChange={(e) => setLocalUrl(e.target.value)}
            className="flex-1 h-7 px-3 text-[10px] font-mono bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-cyber-cyan/50 transition-all"
          />
        </div>

        {/* Model */}
        {provider.category === 'llm' && (
          <div className="flex items-center gap-2">
            <span className="text-[9px] text-muted-foreground/60 w-8 shrink-0">Model</span>
            <input
              type="text"
              value={localModel}
              onChange={(e) => setLocalModel(e.target.value)}
              className="flex-1 h-7 px-3 text-[10px] font-mono bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-cyber-cyan/50 transition-all"
            />
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center gap-2 pt-1">
          <button
            onClick={handleSave}
            className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-cyber-cyan/10 border border-cyber-cyan/20 text-[9px] text-cyber-cyan hover:bg-cyber-cyan/20 transition-all"
          >
            <Save className="h-2.5 w-2.5" /> Guardar
          </button>
          <button
            onClick={handleTest}
            disabled={provider.status === 'testing'}
            className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-surface-2 border border-border text-[9px] text-muted-foreground hover:text-foreground hover:border-surface-3 transition-all disabled:opacity-50"
          >
            {provider.status === 'testing' ? <Loader2 className="h-2.5 w-2.5 animate-spin" /> : <RefreshCw className="h-2.5 w-2.5" />}
            Test
          </button>
          <button
            onClick={() => { resetProvider(provider.id); setLocalKey(''); setLocalUrl(provider.baseUrl); setLocalModel(provider.model); }}
            className="flex items-center gap-1 px-2.5 py-1 rounded-md text-[9px] text-muted-foreground/50 hover:text-cyber-red transition-all"
          >
            <RotateCcw className="h-2.5 w-2.5" />
          </button>
          {provider.docsUrl && (
            <a
              href={provider.docsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 px-2.5 py-1 rounded-md text-[9px] text-muted-foreground/50 hover:text-cyber-blue transition-all ml-auto"
            >
              Docs <ExternalLink className="h-2.5 w-2.5" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

function ProvidersSection() {
  const { connectionMode, setConnectionMode, providers, activeLlmProvider, setActiveLlmProvider } = useProvidersStore();
  const [filter, setFilter] = useState<'all' | 'llm' | 'tool'>('all');

  const llmProviders = providers.filter((p) => p.category === 'llm');
  const toolProviders = providers.filter((p) => p.category === 'tool');
  const filtered = filter === 'all' ? providers : filter === 'llm' ? llmProviders : toolProviders;
  const enabledCount = providers.filter((p) => p.enabled).length;

  return (
    <div className="space-y-4">
      {/* Connection Mode Toggle */}
      <div className="flex items-center gap-3 p-3 rounded-lg bg-surface-0 border border-border">
        <div className="flex-1">
          <p className="text-[11px] font-medium text-foreground mb-1">Modo de Conexion</p>
          <p className="text-[9px] text-muted-foreground">
            {connectionMode === 'local'
              ? 'Todo funciona en local. No se envia ningun dato a servicios externos.'
              : 'Se usaran los proveedores configurados para procesar peticiones.'}
          </p>
        </div>
        <div className="flex items-center bg-surface-2 rounded-lg p-0.5 border border-border">
          <button
            onClick={() => setConnectionMode('local')}
            className={cn(
              'flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[10px] font-medium transition-all',
              connectionMode === 'local'
                ? 'bg-emerald-400/10 text-emerald-400 border border-emerald-400/20'
                : 'text-muted-foreground hover:text-foreground'
            )}
          >
            <WifiOff className="h-3 w-3" /> Local
          </button>
          <button
            onClick={() => setConnectionMode('cloud')}
            className={cn(
              'flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[10px] font-medium transition-all',
              connectionMode === 'cloud'
                ? 'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20'
                : 'text-muted-foreground hover:text-foreground'
            )}
          >
            <Wifi className="h-3 w-3" /> Cloud
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="flex items-center gap-3 text-[10px] text-muted-foreground font-mono">
        <span>{providers.length} proveedores</span>
        <span className="text-border">|</span>
        <span className="text-emerald-400">{enabledCount} activos</span>
        <span className="text-border">|</span>
        <span>{llmProviders.length} LLM</span>
        <span className="text-border">|</span>
        <span>{toolProviders.length} Tools</span>
      </div>

      {/* Active LLM selector (solo en modo cloud) */}
      {connectionMode === 'cloud' && (
        <div className="p-3 rounded-lg bg-cyber-cyan/5 border border-cyber-cyan/10">
          <p className="text-[10px] text-muted-foreground mb-2">Proveedor LLM activo para el chat:</p>
          <div className="flex flex-wrap gap-1.5">
            {llmProviders.filter((p) => p.enabled).map((p) => (
              <button
                key={p.id}
                onClick={() => setActiveLlmProvider(p.id)}
                className={cn(
                  'flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[10px] transition-all border',
                  activeLlmProvider === p.id
                    ? 'bg-cyber-cyan/15 text-cyber-cyan border-cyber-cyan/30'
                    : 'bg-surface-1 text-muted-foreground border-border hover:border-surface-3'
                )}
              >
                <span>{p.icon}</span>
                <span>{p.name}</span>
                {activeLlmProvider === p.id && <Check className="h-3 w-3" />}
              </button>
            ))}
            {llmProviders.filter((p) => p.enabled).length === 0 && (
              <p className="text-[10px] text-muted-foreground/50 italic">
                Ningun proveedor LLM activo. Configura al menos uno abajo.
              </p>
            )}
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex items-center gap-1 border-b border-border pb-1">
        {(['all', 'llm', 'tool'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={cn(
              'flex items-center gap-1 px-2.5 py-1 rounded-md text-[10px] transition-all',
              filter === f ? 'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20' : 'text-muted-foreground hover:text-foreground border border-transparent'
            )}
          >
            {f === 'all' && <Zap className="h-2.5 w-2.5" />}
            {f === 'llm' && <Bot className="h-2.5 w-2.5" />}
            {f === 'tool' && <Wrench className="h-2.5 w-2.5" />}
            {f === 'all' ? 'Todos' : f === 'llm' ? 'Modelos LLM' : 'Herramientas'}
          </button>
        ))}
      </div>

      {/* Provider cards */}
      <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
        {filtered.map((provider) => (
          <ProviderCard key={provider.id} provider={provider} />
        ))}
      </div>
    </div>
  );
}

/* ── Import / Export ── */

function ImportExportSection() {
  return (
    <div className="grid grid-cols-2 gap-3">
      <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-dashed border-border hover:border-cyber-cyan/30 hover:bg-cyber-cyan/5 transition-all group">
        <Download className="h-6 w-6 text-muted-foreground group-hover:text-cyber-cyan transition-colors" />
        <span className="text-[11px] font-medium text-foreground">Export Config</span>
        <span className="text-[9px] text-muted-foreground">Download as JSON file</span>
      </button>
      <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-dashed border-border hover:border-cyber-purple/30 hover:bg-cyber-purple/5 transition-all group">
        <Upload className="h-6 w-6 text-muted-foreground group-hover:text-cyber-purple transition-colors" />
        <span className="text-[11px] font-medium text-foreground">Import Config</span>
        <span className="text-[9px] text-muted-foreground">Load from JSON file</span>
      </button>
      <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-dashed border-border hover:border-emerald-400/30 hover:bg-emerald-400/5 transition-all group">
        <FileJson className="h-6 w-6 text-muted-foreground group-hover:text-emerald-400 transition-colors" />
        <span className="text-[11px] font-medium text-foreground">Export Agents</span>
        <span className="text-[9px] text-muted-foreground">All agent configs as JSON</span>
      </button>
      <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-dashed border-border hover:border-amber-400/30 hover:bg-amber-400/5 transition-all group">
        <Copy className="h-6 w-6 text-muted-foreground group-hover:text-amber-400 transition-colors" />
        <span className="text-[11px] font-medium text-foreground">Share Template</span>
        <span className="text-[9px] text-muted-foreground">Generate shareable config link</span>
      </button>
    </div>
  );
}

/* ── Plugins ── */

interface PluginItem { name: string; description: string; version: string; enabled: boolean; }
const mockPlugins: PluginItem[] = [
  { name: 'Nmap Integration', description: 'Network scanning via Nmap', version: '2.1.0', enabled: true },
  { name: 'Metasploit Bridge', description: 'Connect to Metasploit Framework', version: '1.8.3', enabled: true },
  { name: 'Burp Suite Link', description: 'Web application testing', version: '1.2.0', enabled: false },
  { name: 'Wireshark Capture', description: 'Real-time packet analysis', version: '3.0.1', enabled: true },
  { name: 'Hashcat Cracker', description: 'Password cracking module', version: '1.5.0', enabled: false },
  { name: 'OSINT Collector', description: 'Intelligence gathering tools', version: '2.0.0', enabled: true },
  { name: 'Cloud Scout', description: 'AWS/Azure/GCP enumeration', version: '1.0.0', enabled: false },
  { name: 'Malware Sandbox', description: 'Cuckoo/VirusTotal integration', version: '1.3.2', enabled: true },
];

function PluginItemRow({ plugin }: { plugin: PluginItem }) {
  const [enabled, setEnabled] = useState(plugin.enabled);
  return (
    <div className="flex items-center justify-between py-2 border-b border-border/50 last:border-0">
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <p className="text-[11px] font-medium text-foreground">{plugin.name}</p>
          <span className="text-[9px] font-mono text-muted-foreground/50">v{plugin.version}</span>
        </div>
        <p className="text-[10px] text-muted-foreground">{plugin.description}</p>
      </div>
      <Switch checked={enabled} onCheckedChange={setEnabled} />
    </div>
  );
}

function PluginsSection() {
  return (
    <div className="space-y-1 max-h-[300px] overflow-y-auto">
      {mockPlugins.map((plugin) => (
        <PluginItemRow key={plugin.name} plugin={plugin} />
      ))}
    </div>
  );
}

/* ── Main Config Panel ── */

export function ConfigPanel() {
  return (
    <div className="h-full overflow-y-auto p-4 space-y-3 grid-bg">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-semibold text-foreground">Configuration</h3>
          <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20">
            6 Agents Configured
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-2 border border-border text-[11px] text-muted-foreground hover:text-foreground hover:border-surface-3 transition-all">
            <RotateCcw className="h-3 w-3" /> Reset All
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/30 text-[11px] text-cyber-cyan hover:bg-cyber-cyan/20 transition-all">
            <Save className="h-3 w-3" /> Save Changes
          </button>
        </div>
      </div>

      {/* Agent Prompts - Most important, default open */}
      <Section title="Agent Prompts & Configuration" icon={<Bot className="h-4 w-4" />} defaultOpen={true}>
        <AgentPromptEditor />
      </Section>

      {/* General */}
      <Section title="General Settings" icon={<Settings className="h-4 w-4" />}>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Project Name">
            <Input defaultValue="Kali Dragon Control Center" />
          </Field>
          <Field label="Workspace Path">
            <Input defaultValue="/opt/kali-dragon" mono />
          </Field>
          <div className="col-span-2">
            <Field label="Project Description">
              <TextArea defaultValue="Elite cybersecurity agent orchestration platform with AI-powered multi-agent control for penetration testing and security assessment." rows={2} />
            </Field>
          </div>
          <Toggle label="Auto-start on boot" description="Start all agents when the system boots" defaultChecked={true} />
          <Toggle label="Debug mode" description="Verbose logging and debug output" defaultChecked={false} />
          <Toggle label="Dark mode" description="Always use dark theme" defaultChecked={true} />
          <Toggle label="Auto-save" description="Save configuration changes automatically" defaultChecked={true} />
          <Toggle label="Sound notifications" description="Audio alerts for important events" defaultChecked={false} />
          <Toggle label="Minimize to tray" description="Run in background when window is closed" defaultChecked={true} />
        </div>
      </Section>

      {/* Network */}
      <Section title="Network & Proxy" icon={<Globe className="h-4 w-4" />}>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Proxy URL">
            <Input defaultValue="socks5://127.0.0.1:9050" mono placeholder="socks5://host:port" />
          </Field>
          <Field label="Port Range">
            <Input defaultValue="1-65535" placeholder="e.g., 1-65535" />
          </Field>
          <div className="col-span-2">
            <Field label="Allowed Hosts / Networks">
              <TextArea defaultValue="192.168.1.0/24\n10.0.0.0/24\n172.16.0.0/16" mono rows={3} />
            </Field>
          </div>
          <Toggle label="DNS over HTTPS" description="Route DNS through secure channel" defaultChecked={true} />
          <Toggle label="TLS Certificate Verification" description="Verify certificates for all connections" defaultChecked={true} />
        </div>
      </Section>

      {/* Performance */}
      <Section title="Performance" icon={<Gauge className="h-4 w-4" />}>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Max Concurrent Agents">
            <Input type="number" defaultValue="10" />
          </Field>
          <Field label="Memory Limit (MB)">
            <Input type="number" defaultValue="6144" />
          </Field>
          <Field label="Request Timeout (seconds)">
            <Input type="number" defaultValue="30" />
          </Field>
          <Field label="Thread Pool Size">
            <Input type="number" defaultValue="50" />
          </Field>
          <Toggle label="Auto-scaling" description="Adjust resources based on load" defaultChecked={true} />
          <Toggle label="GPU Acceleration" description="Use GPU for AI model inference" defaultChecked={false} />
        </div>
      </Section>

      {/* Environment Variables */}
      <Section title="Environment Variables" icon={<Braces className="h-4 w-4" />}>
        <EnvVarManager />
      </Section>

      {/* Providers & API Keys */}
      <Section title="Providers & API Keys" icon={<Wifi className="h-4 w-4" />} defaultOpen={true}>
        <ProvidersSection />
      </Section>

      {/* Security */}
      <Section title="Security & Access" icon={<Shield className="h-4 w-4" />}>
        <div className="space-y-4">
          <Toggle label="End-to-end Encryption" description="AES-256 encryption for all agent communications" defaultChecked={true} />
          <Field label="Access Control List">
            <TextArea
              defaultValue="admin@kali-dragon — FULL_ACCESS\nanalyst@kali-dragon — READ_WRITE\nmonitor@kali-dragon — READ_ONLY\napi-service — AGENT_ACCESS"
              mono rows={4}
            />
          </Field>
          <Toggle label="Audit Logging" description="Log all configuration changes and access attempts" defaultChecked={true} />
          <Toggle label="2FA Required" description="Require two-factor authentication for admin access" defaultChecked={false} />
        </div>
      </Section>

      {/* Plugins */}
      <Section title="Plugins & Extensions" icon={<Puzzle className="h-4 w-4" />}>
        <PluginsSection />
      </Section>

      {/* Import / Export */}
      <Section title="Import / Export" icon={<FileJson className="h-4 w-4" />}>
        <ImportExportSection />
      </Section>
    </div>
  );
}
