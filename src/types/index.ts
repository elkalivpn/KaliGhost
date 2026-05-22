export interface Agent {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'busy' | 'error';
  task: string;
  progress: number;
  cpu: number;
  memory: number;
  uptime: string;
  type: 'recon' | 'scanner' | 'exploit' | 'report' | 'monitor' | 'custom';
}

export interface MemoryEntry {
  id: string;
  agentId: string;
  agentName: string;
  type: 'conversation' | 'task' | 'result' | 'error';
  content: string;
  timestamp: string;
  size: string;
  tags: string[];
}

export interface SystemMetric {
  time: string;
  cpu: number;
  memory: number;
  networkIn: number;
  networkOut: number;
}

export interface ActivityEvent {
  id: string;
  agent: string;
  action: string;
  target: string;
  timestamp: string;
  type: 'info' | 'success' | 'warning' | 'error';
}

export type ActiveView =
  | 'dashboard'
  | 'dragon'
  | 'orchestration'
  | 'terminal'
  | 'editor'
  | 'memory'
  | 'monitor'
  | 'config'
  | 'devlab';

/* ── Dev Lab Types ── */
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  files?: string[];
}

export interface ChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: string;
  messageCount: number;
}

export interface ProjectFile {
  name: string;
  type: 'file' | 'folder';
  children?: ProjectFile[];
  language?: string;
  content?: string;
  size?: string;
}

export interface DevLabProject {
  id: string;
  name: string;
  description: string;
  language: string;
  lastModified: string;
  fileCount: number;
}

/* ── Workflow / Orchestration Types ── */

export type WorkflowNodeCategory = 'trigger' | 'agent' | 'action' | 'logic' | 'output' | 'transform';

export interface WorkflowNodeTemplate {
  type: string;
  label: string;
  description: string;
  category: WorkflowNodeCategory;
  icon: string;
  color: string;
  fields: WorkflowNodeField[];
}

export interface WorkflowNodeField {
  name: string;
  label: string;
  type: 'text' | 'textarea' | 'select' | 'number' | 'toggle' | 'code';
  defaultValue: string;
  options?: { label: string; value: string }[];
  placeholder?: string;
}

export interface AgentConfig {
  id: string;
  name: string;
  systemPrompt: string;
  model: string;
  temperature: number;
  maxTokens: number;
  topP: number;
  frequencyPenalty: number;
  presencePenalty: number;
  tools: string[];
  autoExecute: boolean;
  retryOnFail: boolean;
  maxRetries: number;
  timeout: number;
}
