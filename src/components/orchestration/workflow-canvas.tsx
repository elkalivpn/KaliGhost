'use client';

import { useCallback, useMemo, useRef, useState } from 'react';
import {
  ReactFlow,
  Controls,
  MiniMap,
  Background,
  type Node,
  type Edge,
  type OnNodesChange,
  type OnEdgesChange,
  type OnConnect,
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  BackgroundVariant,
  useReactFlow,
  ReactFlowProvider,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import {
  TriggerNode,
  AgentNode,
  ActionNode,
  LogicNode,
  OutputNode,
  TransformNode,
} from './agent-nodes';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import {
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent,
} from '@/components/ui/collapsible';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

import {
  Zap,
  Globe,
  Clock,
  Radio,
  Bot,
  Shield,
  Search,
  FileText,
  Eye,
  Play,
  Terminal,
  FileCode,
  GitBranch,
  Shuffle,
  Repeat,
  GitMerge,
  Timer,
  Split,
  Filter,
  ArrowLeftRight,
  ArrowUpDown,
  Layers,
  Send,
  Bell,
  FileDown,
  Database,
  Save,
  Undo2,
  Redo2,
  ZoomIn,
  ZoomOut,
  Maximize2,
  X,
  ChevronDown,
  ChevronRight,
  GripVertical,
} from 'lucide-react';
import type { WorkflowNodeTemplate, WorkflowNodeField } from '@/types';

/* ────────────────────────────────────────────────────────────────
   Node palette data
   ──────────────────────────────────────────────────────────────── */

interface PaletteItem extends WorkflowNodeTemplate {
  iconComponent: React.ReactNode;
}

const paletteCategories: { name: string; items: PaletteItem[] }[] = [
  {
    name: 'Triggers',
    items: [
      {
        type: 'triggerManual',
        label: 'Manual Start',
        description: 'Triggered by user',
        category: 'trigger',
        icon: 'zap',
        color: 'orange',
        iconComponent: <Zap className="h-4 w-4 text-orange-400" />,
        fields: [
          { name: 'description', label: 'Description', type: 'text', defaultValue: '', placeholder: 'Workflow trigger description' },
        ],
      },
      {
        type: 'triggerWebhook',
        label: 'Webhook',
        description: 'HTTP endpoint trigger',
        category: 'trigger',
        icon: 'globe',
        color: 'orange',
        iconComponent: <Globe className="h-4 w-4 text-orange-400" />,
        fields: [
          { name: 'path', label: 'Webhook Path', type: 'text', defaultValue: '/api/webhook', placeholder: '/api/webhook' },
          { name: 'method', label: 'HTTP Method', type: 'select', defaultValue: 'POST', options: [{ label: 'GET', value: 'GET' }, { label: 'POST', value: 'POST' }, { label: 'PUT', value: 'PUT' }] },
        ],
      },
      {
        type: 'triggerCron',
        label: 'Cron Schedule',
        description: 'Time-based trigger',
        category: 'trigger',
        icon: 'clock',
        color: 'orange',
        iconComponent: <Clock className="h-4 w-4 text-orange-400" />,
        fields: [
          { name: 'cron', label: 'Cron Expression', type: 'text', defaultValue: '0 */6 * * *', placeholder: '0 */6 * * *' },
          { name: 'timezone', label: 'Timezone', type: 'select', defaultValue: 'UTC', options: [{ label: 'UTC', value: 'UTC' }, { label: 'US/Eastern', value: 'US/Eastern' }, { label: 'Europe/London', value: 'Europe/London' }] },
        ],
      },
      {
        type: 'triggerEvent',
        label: 'Event Listener',
        description: 'Event-driven trigger',
        category: 'trigger',
        icon: 'radio',
        color: 'orange',
        iconComponent: <Radio className="h-4 w-4 text-orange-400" />,
        fields: [
          { name: 'eventType', label: 'Event Type', type: 'text', defaultValue: '', placeholder: 'e.g. scan.complete' },
          { name: 'filter', label: 'Event Filter', type: 'text', defaultValue: '', placeholder: 'Optional filter expression' },
        ],
      },
    ],
  },
  {
    name: 'Agents',
    items: [
      {
        type: 'agentRecon',
        label: 'Recon Agent',
        description: 'Network reconnaissance',
        category: 'agent',
        icon: 'search',
        color: 'cyan',
        iconComponent: <Search className="h-4 w-4 text-cyan-400" />,
        fields: [
          { name: 'target', label: 'Target Scope', type: 'text', defaultValue: '', placeholder: '192.168.1.0/24' },
          { name: 'depth', label: 'Scan Depth', type: 'select', defaultValue: 'normal', options: [{ label: 'Quick', value: 'quick' }, { label: 'Normal', value: 'normal' }, { label: 'Deep', value: 'deep' }] },
          { name: 'stealth', label: 'Stealth Mode', type: 'toggle', defaultValue: 'false' },
        ],
      },
      {
        type: 'agentScanner',
        label: 'Scanner Agent',
        description: 'Vulnerability scanning',
        category: 'agent',
        icon: 'shield',
        color: 'cyan',
        iconComponent: <Shield className="h-4 w-4 text-cyan-400" />,
        fields: [
          { name: 'target', label: 'Target', type: 'text', defaultValue: '', placeholder: 'Target host or range' },
          { name: 'scanType', label: 'Scan Type', type: 'select', defaultValue: 'full', options: [{ label: 'Quick', value: 'quick' }, { label: 'Full', value: 'full' }, { label: 'Custom', value: 'custom' }] },
          { name: 'ports', label: 'Port Range', type: 'text', defaultValue: '1-10000', placeholder: '1-65535' },
        ],
      },
      {
        type: 'agentExploit',
        label: 'Exploit Agent',
        description: 'Exploitation engine',
        category: 'agent',
        icon: 'bot',
        color: 'cyan',
        iconComponent: <Bot className="h-4 w-4 text-cyan-400" />,
        fields: [
          { name: 'target', label: 'Target', type: 'text', defaultValue: '', placeholder: 'Exploit target' },
          { name: 'payload', label: 'Payload Type', type: 'select', defaultValue: 'reverse_shell', options: [{ label: 'Reverse Shell', value: 'reverse_shell' }, { label: 'Bind Shell', value: 'bind_shell' }, { label: 'Meterpreter', value: 'meterpreter' }] },
          { name: 'lhost', label: 'LHOST', type: 'text', defaultValue: '', placeholder: 'Listener address' },
        ],
      },
      {
        type: 'agentReport',
        label: 'Report Agent',
        description: 'Generate reports',
        category: 'agent',
        icon: 'filetext',
        color: 'cyan',
        iconComponent: <FileText className="h-4 w-4 text-cyan-400" />,
        fields: [
          { name: 'format', label: 'Report Format', type: 'select', defaultValue: 'pdf', options: [{ label: 'PDF', value: 'pdf' }, { label: 'HTML', value: 'html' }, { label: 'JSON', value: 'json' }, { label: 'Markdown', value: 'md' }] },
          { name: 'sections', label: 'Sections', type: 'textarea', defaultValue: 'exec,findings,risk', placeholder: 'exec,findings,risk' },
        ],
      },
      {
        type: 'agentCustom',
        label: 'Custom Agent',
        description: 'User-defined agent',
        category: 'agent',
        icon: 'eye',
        color: 'cyan',
        iconComponent: <Eye className="h-4 w-4 text-cyan-400" />,
        fields: [
          { name: 'model', label: 'LLM Model', type: 'select', defaultValue: 'gpt-4o', options: [{ label: 'GPT-4o', value: 'gpt-4o' }, { label: 'Claude-3.5', value: 'claude-3.5' }, { label: 'Local', value: 'local' }] },
          { name: 'systemPrompt', label: 'System Prompt', type: 'textarea', defaultValue: '', placeholder: 'Agent system prompt...' },
        ],
      },
    ],
  },
  {
    name: 'Actions',
    items: [
      {
        type: 'actionCommand',
        label: 'Execute Command',
        description: 'Run shell command',
        category: 'action',
        icon: 'play',
        color: 'green',
        iconComponent: <Play className="h-4 w-4 text-emerald-400" />,
        fields: [
          { name: 'command', label: 'Command', type: 'textarea', defaultValue: '', placeholder: 'Enter command to execute' },
          { name: 'timeout', label: 'Timeout (s)', type: 'number', defaultValue: '300' },
        ],
      },
      {
        type: 'actionScript',
        label: 'Run Script',
        description: 'Execute a script file',
        category: 'action',
        icon: 'terminal',
        color: 'green',
        iconComponent: <Terminal className="h-4 w-4 text-emerald-400" />,
        fields: [
          { name: 'path', label: 'Script Path', type: 'text', defaultValue: '', placeholder: '/opt/scripts/scan.sh' },
          { name: 'args', label: 'Arguments', type: 'text', defaultValue: '', placeholder: '--verbose --output json' },
        ],
      },
      {
        type: 'actionHttp',
        label: 'HTTP Request',
        description: 'Send HTTP request',
        category: 'action',
        icon: 'globe',
        color: 'green',
        iconComponent: <Globe className="h-4 w-4 text-emerald-400" />,
        fields: [
          { name: 'url', label: 'URL', type: 'text', defaultValue: '', placeholder: 'https://api.example.com' },
          { name: 'method', label: 'Method', type: 'select', defaultValue: 'GET', options: [{ label: 'GET', value: 'GET' }, { label: 'POST', value: 'POST' }, { label: 'PUT', value: 'PUT' }, { label: 'DELETE', value: 'DELETE' }] },
          { name: 'headers', label: 'Headers (JSON)', type: 'textarea', defaultValue: '{}', placeholder: '{"Authorization": "Bearer ..."}' },
        ],
      },
      {
        type: 'actionFile',
        label: 'File Operation',
        description: 'Read/write files',
        category: 'action',
        icon: 'filecode',
        color: 'green',
        iconComponent: <FileCode className="h-4 w-4 text-emerald-400" />,
        fields: [
          { name: 'operation', label: 'Operation', type: 'select', defaultValue: 'read', options: [{ label: 'Read', value: 'read' }, { label: 'Write', value: 'write' }, { label: 'Append', value: 'append' }, { label: 'Delete', value: 'delete' }] },
          { name: 'path', label: 'File Path', type: 'text', defaultValue: '', placeholder: '/tmp/output.txt' },
        ],
      },
    ],
  },
  {
    name: 'Logic',
    items: [
      {
        type: 'logicIf',
        label: 'If/Else Condition',
        description: 'Branch on condition',
        category: 'logic',
        icon: 'gitbranch',
        color: 'amber',
        iconComponent: <GitBranch className="h-4 w-4 text-amber-400" />,
        fields: [
          { name: 'field', label: 'Field', type: 'text', defaultValue: '', placeholder: '$.vulnerabilities.length' },
          { name: 'operator', label: 'Operator', type: 'select', defaultValue: 'gt', options: [{ label: 'Greater Than', value: 'gt' }, { label: 'Less Than', value: 'lt' }, { label: 'Equals', value: 'eq' }, { label: 'Contains', value: 'contains' }] },
          { name: 'value', label: 'Value', type: 'text', defaultValue: '0' },
        ],
      },
      {
        type: 'logicSwitch',
        label: 'Switch',
        description: 'Multi-branch routing',
        category: 'logic',
        icon: 'shuffle',
        color: 'amber',
        iconComponent: <Shuffle className="h-4 w-4 text-amber-400" />,
        fields: [
          { name: 'field', label: 'Field', type: 'text', defaultValue: '', placeholder: '$.status' },
          { name: 'cases', label: 'Cases (comma)', type: 'text', defaultValue: '', placeholder: 'critical,high,medium,low' },
        ],
      },
      {
        type: 'logicLoop',
        label: 'Loop',
        description: 'Iterate over items',
        category: 'logic',
        icon: 'repeat',
        color: 'amber',
        iconComponent: <Repeat className="h-4 w-4 text-amber-400" />,
        fields: [
          { name: 'source', label: 'Source Field', type: 'text', defaultValue: '', placeholder: '$.targets' },
          { name: 'maxIterations', label: 'Max Iterations', type: 'number', defaultValue: '100' },
          { name: 'concurrency', label: 'Concurrency', type: 'number', defaultValue: '5' },
        ],
      },
      {
        type: 'logicMerge',
        label: 'Merge',
        description: 'Merge multiple inputs',
        category: 'logic',
        icon: 'gitmerge',
        color: 'amber',
        iconComponent: <GitMerge className="h-4 w-4 text-amber-400" />,
        fields: [
          { name: 'mode', label: 'Merge Mode', type: 'select', defaultValue: 'append', options: [{ label: 'Append', value: 'append' }, { label: 'Combine', value: 'combine' }, { label: 'Choose Branch', value: 'choose' }] },
        ],
      },
      {
        type: 'logicDelay',
        label: 'Delay',
        description: 'Wait before continuing',
        category: 'logic',
        icon: 'timer',
        color: 'amber',
        iconComponent: <Timer className="h-4 w-4 text-amber-400" />,
        fields: [
          { name: 'seconds', label: 'Delay (seconds)', type: 'number', defaultValue: '5' },
        ],
      },
    ],
  },
  {
    name: 'Transform',
    items: [
      {
        type: 'transformParser',
        label: 'Data Parser',
        description: 'Parse data formats',
        category: 'transform',
        icon: 'split',
        color: 'blue',
        iconComponent: <Split className="h-4 w-4 text-sky-400" />,
        fields: [
          { name: 'format', label: 'Input Format', type: 'select', defaultValue: 'json', options: [{ label: 'JSON', value: 'json' }, { label: 'XML', value: 'xml' }, { label: 'CSV', value: 'csv' }, { label: 'YAML', value: 'yaml' }] },
        ],
      },
      {
        type: 'transformFilter',
        label: 'Filter',
        description: 'Filter data items',
        category: 'transform',
        icon: 'filter',
        color: 'blue',
        iconComponent: <Filter className="h-4 w-4 text-sky-400" />,
        fields: [
          { name: 'condition', label: 'Condition', type: 'text', defaultValue: '', placeholder: '$.severity == "critical"' },
        ],
      },
      {
        type: 'transformMap',
        label: 'Map',
        description: 'Transform field values',
        category: 'transform',
        icon: 'arrowleftright',
        color: 'blue',
        iconComponent: <ArrowLeftRight className="h-4 w-4 text-sky-400" />,
        fields: [
          { name: 'mapping', label: 'Field Mapping (JSON)', type: 'textarea', defaultValue: '{}', placeholder: '{"old_name": "new_name"}' },
        ],
      },
      {
        type: 'transformSort',
        label: 'Sort',
        description: 'Sort data items',
        category: 'transform',
        icon: 'arrowupdown',
        color: 'blue',
        iconComponent: <ArrowUpDown className="h-4 w-4 text-sky-400" />,
        fields: [
          { name: 'field', label: 'Sort Field', type: 'text', defaultValue: '', placeholder: '$.severity' },
          { name: 'order', label: 'Order', type: 'select', defaultValue: 'desc', options: [{ label: 'Ascending', value: 'asc' }, { label: 'Descending', value: 'desc' }] },
        ],
      },
      {
        type: 'transformAggregate',
        label: 'Aggregate',
        description: 'Aggregate data values',
        category: 'transform',
        icon: 'layers',
        color: 'blue',
        iconComponent: <Layers className="h-4 w-4 text-sky-400" />,
        fields: [
          { name: 'operation', label: 'Operation', type: 'select', defaultValue: 'count', options: [{ label: 'Count', value: 'count' }, { label: 'Sum', value: 'sum' }, { label: 'Average', value: 'avg' }, { label: 'Min', value: 'min' }, { label: 'Max', value: 'max' }] },
          { name: 'field', label: 'Target Field', type: 'text', defaultValue: '', placeholder: '$.score' },
        ],
      },
    ],
  },
  {
    name: 'Output',
    items: [
      {
        type: 'outputReport',
        label: 'Send Report',
        description: 'Generate & send report',
        category: 'output',
        icon: 'send',
        color: 'purple',
        iconComponent: <Send className="h-4 w-4 text-violet-400" />,
        fields: [
          { name: 'format', label: 'Format', type: 'select', defaultValue: 'pdf', options: [{ label: 'PDF', value: 'pdf' }, { label: 'HTML', value: 'html' }, { label: 'Markdown', value: 'md' }] },
          { name: 'destination', label: 'Destination', type: 'text', defaultValue: '', placeholder: 'email, slack, file' },
        ],
      },
      {
        type: 'outputNotification',
        label: 'Notification',
        description: 'Send notification',
        category: 'output',
        icon: 'bell',
        color: 'purple',
        iconComponent: <Bell className="h-4 w-4 text-violet-400" />,
        fields: [
          { name: 'channel', label: 'Channel', type: 'select', defaultValue: 'slack', options: [{ label: 'Slack', value: 'slack' }, { label: 'Discord', value: 'discord' }, { label: 'Email', value: 'email' }, { label: 'Webhook', value: 'webhook' }] },
          { name: 'message', label: 'Message', type: 'textarea', defaultValue: '', placeholder: 'Notification message...' },
        ],
      },
      {
        type: 'outputLog',
        label: 'Log to File',
        description: 'Write to log file',
        category: 'output',
        icon: 'filedown',
        color: 'purple',
        iconComponent: <FileDown className="h-4 w-4 text-violet-400" />,
        fields: [
          { name: 'path', label: 'Log Path', type: 'text', defaultValue: '/var/log/dragon/', placeholder: '/var/log/dragon/' },
          { name: 'level', label: 'Log Level', type: 'select', defaultValue: 'info', options: [{ label: 'Debug', value: 'debug' }, { label: 'Info', value: 'info' }, { label: 'Warning', value: 'warn' }, { label: 'Error', value: 'error' }] },
        ],
      },
      {
        type: 'outputDatabase',
        label: 'Database Write',
        description: 'Write to database',
        category: 'output',
        icon: 'database',
        color: 'purple',
        iconComponent: <Database className="h-4 w-4 text-violet-400" />,
        fields: [
          { name: 'connection', label: 'Connection String', type: 'text', defaultValue: '', placeholder: 'sqlite:///data.db' },
          { name: 'table', label: 'Table Name', type: 'text', defaultValue: '', placeholder: 'scan_results' },
          { name: 'operation', label: 'Operation', type: 'select', defaultValue: 'insert', options: [{ label: 'Insert', value: 'insert' }, { label: 'Upsert', value: 'upsert' }, { label: 'Update', value: 'update' }] },
        ],
      },
    ],
  },
];

/* ────────────────────────────────────────────────────────────────
   Map template type → ReactFlow node type string
   ──────────────────────────────────────────────────────────────── */

function nodeTypeFromCategory(cat: string): string {
  switch (cat) {
    case 'trigger':
      return 'triggerNode';
    case 'agent':
      return 'agentNode';
    case 'action':
      return 'actionNode';
    case 'logic':
      return 'logicNode';
    case 'transform':
      return 'transformNode';
    case 'output':
      return 'outputNode';
    default:
      return 'agentNode';
  }
}

/* ────────────────────────────────────────────────────────────────
   Sample workflow nodes & edges
   ──────────────────────────────────────────────────────────────── */

const sampleNodes: Node[] = [
  {
    id: 'n1',
    type: 'triggerNode',
    position: { x: 250, y: 200 },
    data: {
      label: 'Manual Start',
      description: 'User-triggered pipeline',
      status: 'success',
      progress: 100,
      icon: 'zap',
      category: 'trigger',
    },
  },
  {
    id: 'n2',
    type: 'agentNode',
    position: { x: 550, y: 100 },
    data: {
      label: 'Recon Agent',
      description: 'Network reconnaissance scan',
      status: 'success',
      progress: 100,
      icon: 'search',
      category: 'agent',
    },
  },
  {
    id: 'n3',
    type: 'agentNode',
    position: { x: 550, y: 300 },
    data: {
      label: 'Scanner Agent',
      description: 'Vulnerability scanning',
      status: 'running',
      progress: 64,
      icon: 'shield',
      category: 'agent',
    },
  },
  {
    id: 'n4',
    type: 'logicNode',
    position: { x: 850, y: 200 },
    data: {
      label: 'If/Else Condition',
      description: 'Check vuln count > 0',
      status: 'pending',
      progress: 0,
      icon: 'gitbranch',
      category: 'logic',
    },
  },
  {
    id: 'n5',
    type: 'agentNode',
    position: { x: 1150, y: 100 },
    data: {
      label: 'Exploit Agent',
      description: 'Exploitation engine',
      status: 'pending',
      progress: 0,
      icon: 'bot',
      category: 'agent',
    },
  },
  {
    id: 'n6',
    type: 'outputNode',
    position: { x: 1150, y: 300 },
    data: {
      label: 'Generate Report',
      description: 'Create pentest report',
      status: 'pending',
      progress: 0,
      icon: 'filetext',
      category: 'output',
    },
  },
];

const sampleEdges: Edge[] = [
  {
    id: 'e1-2',
    source: 'n1',
    target: 'n2',
    animated: true,
    type: 'smoothstep',
    style: { stroke: '#00f0ff', strokeWidth: 2 },
  },
  {
    id: 'e1-3',
    source: 'n1',
    target: 'n3',
    animated: true,
    type: 'smoothstep',
    style: { stroke: '#00f0ff', strokeWidth: 2 },
  },
  {
    id: 'e2-4',
    source: 'n2',
    target: 'n4',
    animated: true,
    type: 'smoothstep',
    style: { stroke: '#00f0ff', strokeWidth: 2 },
  },
  {
    id: 'e3-4',
    source: 'n3',
    target: 'n4',
    animated: true,
    type: 'smoothstep',
    style: { stroke: '#fbbf24', strokeWidth: 2 },
  },
  {
    id: 'e4-5',
    source: 'n4',
    target: 'n5',
    animated: true,
    type: 'smoothstep',
    style: { stroke: '#22c55e', strokeWidth: 2 },
    label: 'true',
    labelStyle: { fill: '#22c55e', fontWeight: 600, fontSize: 11 },
    labelBgStyle: { fill: '#0d1117', fillOpacity: 0.85 },
    labelBgPadding: [6, 4] as [number, number],
    labelBgBorderRadius: 4,
  },
  {
    id: 'e4-6',
    source: 'n4',
    target: 'n6',
    animated: true,
    type: 'smoothstep',
    style: { stroke: '#ef4444', strokeWidth: 2 },
    label: 'false',
    labelStyle: { fill: '#ef4444', fontWeight: 600, fontSize: 11 },
    labelBgStyle: { fill: '#0d1117', fillOpacity: 0.85 },
    labelBgPadding: [6, 4] as [number, number],
    labelBgBorderRadius: 4,
  },
];

/* ────────────────────────────────────────────────────────────────
   Mock output data for the properties panel
   ──────────────────────────────────────────────────────────────── */

const mockOutputs: Record<string, string> = {
  triggerManual: JSON.stringify(
    { triggered: true, timestamp: '2025-01-15T14:30:00Z', user: 'operator' },
    null,
    2
  ),
  agentRecon: JSON.stringify(
    { hosts_found: 24, live_hosts: 18, open_ports: 142, duration: '4m 22s' },
    null,
    2
  ),
  agentScanner: JSON.stringify(
    { vulnerabilities: { critical: 3, high: 7, medium: 15, low: 23 }, scanned: 18, remaining: 6, progress: '64%' },
    null,
    2
  ),
  logicIf: JSON.stringify(
    { condition: '$.vulnerabilities.critical > 0', result: true, branch: 'true' },
    null,
    2
  ),
  agentExploit: JSON.stringify(
    { status: 'pending', exploits_loaded: 45, targets: 0, message: 'Waiting for condition...' },
    null,
    2
  ),
  outputReport: JSON.stringify(
    { status: 'pending', format: 'pdf', destination: '/reports/', message: 'Waiting for data...' },
    null,
    2
  ),
};

/* ────────────────────────────────────────────────────────────────
   LEFT PANEL: Node Palette
   ──────────────────────────────────────────────────────────────── */

function NodePalette() {
  const [search, setSearch] = useState('');
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  const filteredCategories = useMemo(() => {
    const q = search.toLowerCase();
    if (!q) return paletteCategories;
    return paletteCategories
      .map((cat) => ({
        ...cat,
        items: cat.items.filter(
          (item) =>
            item.label.toLowerCase().includes(q) ||
            item.description.toLowerCase().includes(q)
        ),
      }))
      .filter((cat) => cat.items.length > 0);
  }, [search]);

  const toggleCollapse = (name: string) => {
    setCollapsed((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  const onDragStart = useCallback(
    (event: React.DragEvent, item: PaletteItem) => {
      event.dataTransfer.setData(
        'application/reactflow',
        JSON.stringify(item)
      );
      event.dataTransfer.effectAllowed = 'move';
    },
    []
  );

  return (
    <div className="w-[220px] bg-surface-1 border-r border-border flex flex-col shrink-0">
      {/* Header */}
      <div className="px-3 py-2.5 border-b border-border">
        <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">
          Nodes
        </p>
        <div className="relative">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground" />
          <Input
            placeholder="Search nodes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="h-7 pl-7 pr-2 text-[11px] bg-surface-0 border-border focus-visible:ring-cyber-cyan/30"
          />
        </div>
      </div>

      {/* Categories */}
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
          {filteredCategories.map((cat) => (
            <Collapsible
              key={cat.name}
              open={!collapsed[cat.name]}
              onOpenChange={() => toggleCollapse(cat.name)}
            >
              <CollapsibleTrigger className="flex items-center gap-1.5 w-full px-2 py-1.5 rounded-md hover:bg-surface-2 transition-colors">
                {collapsed[cat.name] ? (
                  <ChevronRight className="h-3 w-3 text-muted-foreground shrink-0" />
                ) : (
                  <ChevronDown className="h-3 w-3 text-muted-foreground shrink-0" />
                )}
                <span className="text-[11px] font-semibold text-foreground">
                  {cat.name}
                </span>
                <Badge
                  variant="secondary"
                  className="ml-auto text-[9px] h-4 px-1.5 font-mono"
                >
                  {cat.items.length}
                </Badge>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <div className="space-y-0.5 mt-0.5 mb-1">
                  {cat.items.map((item) => (
                    <div
                      key={item.type}
                      draggable
                      onDragStart={(e) => onDragStart(e, item)}
                      className="flex items-center gap-2.5 px-2 py-1.5 rounded-md hover:bg-surface-2 cursor-grab active:cursor-grabbing transition-colors group"
                    >
                      <div className="h-7 w-7 rounded-md bg-surface-2 border border-border flex items-center justify-center shrink-0 group-hover:border-muted-foreground/30 transition-colors">
                        {item.iconComponent}
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-[11px] font-medium text-foreground truncate leading-tight">
                          {item.label}
                        </p>
                        <p className="text-[9px] text-muted-foreground truncate leading-tight mt-0.5">
                          {item.description}
                        </p>
                      </div>
                      <GripVertical className="h-3 w-3 text-muted-foreground/40 opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                    </div>
                  ))}
                </div>
              </CollapsibleContent>
            </Collapsible>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────
   RIGHT PANEL: Node Properties
   ──────────────────────────────────────────────────────────────── */

function NodePropertiesPanel({
  node,
  onClose,
}: {
  node: Node | null;
  onClose: () => void;
}) {
  const data = node?.data as {
    label: string;
    description?: string;
    status?: string;
    icon?: string;
    category?: string;
    [key: string]: unknown;
  } | undefined;

  // Find the template from palette to get fields
  const template = useMemo(() => {
    if (!node) return null;
    for (const cat of paletteCategories) {
      const found = cat.items.find((item) => item.type === node.type?.replace('Node', ''));
      if (found) return found;
      // Try matching by node data icon + category
      const byData = cat.items.find(
        (item) => item.icon === data?.icon && item.category === data?.category
      );
      if (byData) return byData;
    }
    return null;
  }, [node, data?.icon, data?.category]);

  const fields = template?.fields ?? [];

  if (!node) return null;

  const catColorMap: Record<string, string> = {
    trigger: 'text-orange-400',
    agent: 'text-cyber-cyan',
    action: 'text-emerald-400',
    logic: 'text-amber-400',
    transform: 'text-sky-400',
    output: 'text-violet-400',
  };

  const catBgMap: Record<string, string> = {
    trigger: 'bg-orange-400/10',
    agent: 'bg-cyber-cyan/10',
    action: 'bg-emerald-400/10',
    logic: 'bg-amber-400/10',
    transform: 'bg-sky-400/10',
    output: 'bg-violet-400/10',
  };

  const catName = data.category ?? 'agent';

  return (
    <div className="w-[280px] bg-surface-1 border-l border-border flex flex-col shrink-0">
      {/* Panel Header */}
      <div className="flex items-center gap-2 px-3 py-2.5 border-b border-border">
        <div
          className={`h-6 w-6 rounded flex items-center justify-center ${catBgMap[catName] ?? 'bg-surface-2'}`}
        >
          <span className={`text-[10px] font-semibold uppercase ${catColorMap[catName] ?? 'text-foreground'}`}>
            {catName.charAt(0)}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-xs font-semibold text-foreground truncate">
            {data.label}
          </p>
          <p className="text-[9px] text-muted-foreground">
            Node Properties
          </p>
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="h-6 w-6 text-muted-foreground hover:text-foreground"
          onClick={onClose}
        >
          <X className="h-3.5 w-3.5" />
        </Button>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="settings" className="flex-1 flex flex-col min-h-0">
        <div className="px-3 pt-2">
          <TabsList className="w-full h-7 bg-surface-0">
            <TabsTrigger value="settings" className="text-[10px] h-5 px-2 flex-1">
              Settings
            </TabsTrigger>
            <TabsTrigger value="config" className="text-[10px] h-5 px-2 flex-1">
              Config
            </TabsTrigger>
            <TabsTrigger value="output" className="text-[10px] h-5 px-2 flex-1">
              Output
            </TabsTrigger>
          </TabsList>
        </div>

        <ScrollArea className="flex-1 min-h-0">
          {/* Settings Tab */}
          <TabsContent value="settings" className="p-3 space-y-3 mt-0">
            <div className="space-y-1.5">
              <label className="text-[10px] text-muted-foreground font-medium">
                Name
              </label>
              <Input
                defaultValue={data.label}
                className="h-7 text-[11px] bg-surface-0 border-border"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-[10px] text-muted-foreground font-medium">
                Description
              </label>
              <Textarea
                defaultValue={data.description ?? ''}
                placeholder="Node description..."
                className="text-[11px] bg-surface-0 border-border min-h-[60px] resize-none"
              />
            </div>
            <Separator />
            <div className="space-y-2.5">
              <div className="flex items-center justify-between">
                <label className="text-[10px] text-muted-foreground font-medium">
                  Enabled
                </label>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-[10px] text-muted-foreground font-medium">
                  Continue on Error
                </label>
                <Switch />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-[10px] text-muted-foreground font-medium">
                  Retry on Failure
                </label>
                <Switch defaultChecked />
              </div>
            </div>
            <Separator />
            <div className="space-y-1.5">
              <label className="text-[10px] text-muted-foreground font-medium">
                Node ID
              </label>
              <div className="px-2 py-1 bg-surface-0 rounded border border-border">
                <span className="text-[10px] font-mono text-muted-foreground">
                  {node.id}
                </span>
              </div>
            </div>
            <div className="space-y-1.5">
              <label className="text-[10px] text-muted-foreground font-medium">
                Type
              </label>
              <div className="px-2 py-1 bg-surface-0 rounded border border-border">
                <span className="text-[10px] font-mono text-muted-foreground">
                  {node.type}
                </span>
              </div>
            </div>
          </TabsContent>

          {/* Config Tab */}
          <TabsContent value="config" className="p-3 space-y-3 mt-0">
            {fields.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                <p className="text-[11px]">No configuration fields</p>
                <p className="text-[9px] mt-1">This node uses default settings</p>
              </div>
            ) : (
              fields.map((field: WorkflowNodeField) => (
                <div key={field.name} className="space-y-1.5">
                  <label className="text-[10px] text-muted-foreground font-medium">
                    {field.label}
                  </label>
                  {field.type === 'text' && (
                    <Input
                      defaultValue={field.defaultValue}
                      placeholder={field.placeholder}
                      className="h-7 text-[11px] bg-surface-0 border-border"
                    />
                  )}
                  {field.type === 'number' && (
                    <Input
                      type="number"
                      defaultValue={field.defaultValue}
                      placeholder={field.placeholder}
                      className="h-7 text-[11px] bg-surface-0 border-border"
                    />
                  )}
                  {field.type === 'textarea' && (
                    <Textarea
                      defaultValue={field.defaultValue}
                      placeholder={field.placeholder}
                      className="text-[11px] bg-surface-0 border-border min-h-[60px] resize-none font-mono"
                    />
                  )}
                  {field.type === 'select' && field.options && (
                    <Select defaultValue={field.defaultValue}>
                      <SelectTrigger className="h-7 text-[11px] bg-surface-0 border-border w-full">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-surface-1 border-border">
                        {field.options.map((opt) => (
                          <SelectItem
                            key={opt.value}
                            value={opt.value}
                            className="text-[11px]"
                          >
                            {opt.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                  {field.type === 'toggle' && (
                    <Switch
                      defaultChecked={field.defaultValue === 'true'}
                    />
                  )}
                  {field.type === 'code' && (
                    <Textarea
                      defaultValue={field.defaultValue}
                      placeholder={field.placeholder}
                      className="text-[11px] bg-surface-0 border-border min-h-[80px] resize-none font-mono"
                    />
                  )}
                </div>
              ))
            )}
          </TabsContent>

          {/* Output Tab */}
          <TabsContent value="output" className="p-3 mt-0">
            <div className="flex items-center justify-between mb-2">
              <label className="text-[10px] text-muted-foreground font-medium">
                Last Output
              </label>
              <Badge variant="secondary" className="text-[9px] h-4 px-1.5 font-mono">
                {data.status === 'success' ? '200 OK' : data.status === 'running' ? 'PENDING' : 'IDLE'}
              </Badge>
            </div>
            <div className="bg-surface-0 border border-border rounded-md p-2.5">
              <pre className="text-[10px] font-mono text-foreground/80 whitespace-pre-wrap break-all leading-relaxed max-h-[400px] overflow-y-auto">
                {mockOutputs[node.type?.replace('Node', '') ?? ''] ??
                  mockOutputs[data.icon ?? ''] ??
                  JSON.stringify(
                    {
                      status: data.status ?? 'idle',
                      progress: data.progress ?? 0,
                      message: 'No output yet',
                      timestamp: new Date().toISOString(),
                    },
                    null,
                    2
                  )}
              </pre>
            </div>
          </TabsContent>
        </ScrollArea>
      </Tabs>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────
   TOP BAR
   ──────────────────────────────────────────────────────────────── */

function WorkflowTopBar({
  workflowName,
  onWorkflowNameChange,
  nodeCount,
  edgeCount,
}: {
  workflowName: string;
  onWorkflowNameChange: (v: string) => void;
  nodeCount: number;
  edgeCount: number;
}) {
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(workflowName);

  const handleSave = () => {
    setEditing(false);
    onWorkflowNameChange(name);
  };

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 border-b border-border bg-surface-1 shrink-0">
      {/* Workflow Name */}
      <div className="flex items-center gap-2 mr-3">
        {editing ? (
          <Input
            autoFocus
            value={name}
            onChange={(e) => setName(e.target.value)}
            onBlur={handleSave}
            onKeyDown={(e) => e.key === 'Enter' && handleSave()}
            className="h-6 w-44 text-xs font-semibold bg-surface-0 border-cyber-cyan/30 focus-visible:ring-cyber-cyan/20"
          />
        ) : (
          <button
            onClick={() => setEditing(true)}
            className="text-xs font-semibold text-foreground hover:text-cyber-cyan transition-colors truncate max-w-[180px]"
          >
            {name}
          </button>
        )}
      </div>

      <Separator orientation="vertical" className="h-4" />

      {/* Actions */}
      <Button
        variant="ghost"
        size="sm"
        className="h-7 gap-1.5 text-[10px] text-muted-foreground hover:text-foreground"
        onClick={() => {}}
      >
        <Undo2 className="h-3 w-3" />
        Undo
      </Button>
      <Button
        variant="ghost"
        size="sm"
        className="h-7 gap-1.5 text-[10px] text-muted-foreground hover:text-foreground"
        onClick={() => {}}
      >
        <Redo2 className="h-3 w-3" />
        Redo
      </Button>

      <Separator orientation="vertical" className="h-4" />

      <Button
        variant="ghost"
        size="sm"
        className="h-7 gap-1.5 text-[10px] text-muted-foreground hover:text-foreground"
        onClick={() => {}}
      >
        <ZoomIn className="h-3 w-3" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        className="h-7 gap-1.5 text-[10px] text-muted-foreground hover:text-foreground"
        onClick={() => {}}
      >
        <ZoomOut className="h-3 w-3" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        className="h-7 gap-1.5 text-[10px] text-muted-foreground hover:text-foreground"
        onClick={() => {}}
      >
        <Maximize2 className="h-3 w-3" />
        Fit
      </Button>

      <div className="ml-auto flex items-center gap-2">
        {/* Stats */}
        <div className="flex items-center gap-2 mr-2">
          <span className="text-[10px] font-mono text-muted-foreground">
            {nodeCount} nodes
          </span>
          <span className="text-[10px] font-mono text-muted-foreground">
            {edgeCount} edges
          </span>
        </div>

        {/* Save */}
        <Button
          variant="outline"
          size="sm"
          className="h-7 gap-1.5 text-[10px] bg-surface-2 border-border hover:bg-surface-3"
          onClick={() => {}}
        >
          <Save className="h-3 w-3" />
          Save
        </Button>

        {/* Execute */}
        <Button
          size="sm"
          className="h-7 gap-1.5 text-[10px] bg-cyber-cyan text-surface-0 hover:bg-cyber-cyan/90 font-semibold"
          onClick={() => {}}
        >
          <Play className="h-3 w-3" />
          Execute
        </Button>
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────
   MAIN CANVAS (wrapped in ReactFlowProvider)
   ──────────────────────────────────────────────────────────────── */

const nodeTypes = {
  triggerNode: TriggerNode,
  agentNode: AgentNode,
  actionNode: ActionNode,
  logicNode: LogicNode,
  outputNode: OutputNode,
  transformNode: TransformNode,
};

function FlowCanvasInner({
  onNodeSelect,
}: {
  onNodeSelect: (node: Node | null) => void;
}) {
  const [nodes, setNodes] = useState<Node[]>(sampleNodes);
  const [edges, setEdges] = useState<Edge[]>(sampleEdges);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { screenToFlowPosition } = useReactFlow();

  const onNodesChange: OnNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect: OnConnect = useCallback(
    (connection) =>
      setEdges((eds) =>
        addEdge(
          {
            ...connection,
            animated: true,
            type: 'smoothstep',
            style: { stroke: '#00f0ff', strokeWidth: 2 },
          },
          eds
        )
      ),
    []
  );

  const onNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      onNodeSelect(node);
    },
    [onNodeSelect]
  );

  const onPaneClick = useCallback(() => {
    onNodeSelect(null);
  }, [onNodeSelect]);

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const raw = event.dataTransfer.getData('application/reactflow');
      if (!raw) return;

      try {
        const item: PaletteItem = JSON.parse(raw);
        const position = screenToFlowPosition({
          x: event.clientX,
          y: event.clientY,
        });

        const newNode: Node = {
          id: `${item.type}-${Date.now()}`,
          type: nodeTypeFromCategory(item.category),
          position,
          data: {
            label: item.label,
            description: item.description,
            status: 'idle',
            progress: 0,
            icon: item.icon,
            category: item.category,
          },
        };

        setNodes((nds) => [...nds, newNode]);
      } catch {
        // Invalid JSON, ignore
      }
    },
    [screenToFlowPosition]
  );

  const defaultEdgeOptions = useMemo(
    () => ({
      type: 'smoothstep' as const,
      animated: true,
      style: { stroke: '#00f0ff', strokeWidth: 2 },
    }),
    []
  );

  return (
    <div ref={reactFlowWrapper} className="flex-1 h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        onDragOver={onDragOver}
        onDrop={onDrop}
        nodeTypes={nodeTypes}
        defaultEdgeOptions={defaultEdgeOptions}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        proOptions={{ hideAttribution: true }}
        deleteKeyCode={['Backspace', 'Delete']}
        snapToGrid
        snapGrid={[16, 16]}
        minZoom={0.2}
        maxZoom={2}
      >
        <Controls
          showInteractive={false}
          className="!bg-surface-1 !border-border !rounded-lg"
        />
        <MiniMap
          className="!bg-surface-1 !border-border !rounded-lg"
          nodeColor={(node) => {
            const cat = (node.data as { category?: string })?.category;
            switch (cat) {
              case 'trigger': return '#fb923c';
              case 'agent': return '#00f0ff';
              case 'action': return '#34d399';
              case 'logic': return '#fbbf24';
              case 'output': return '#a78bfa';
              case 'transform': return '#38bdf8';
              default: return '#00f0ff';
            }
          }}
          maskColor="rgba(10, 10, 15, 0.8)"
          pannable
          zoomable
        />
        <Background
          variant={BackgroundVariant.Dots}
          color="#1e293b"
          gap={20}
          size={1}
        />
      </ReactFlow>
    </div>
  );
}

/* ────────────────────────────────────────────────────────────────
   EXPORTED WorkflowCanvas
   ──────────────────────────────────────────────────────────────── */

export function WorkflowCanvas() {
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [workflowName, setWorkflowName] = useState('Pentest Pipeline v1');

  return (
    <div className="h-full w-full flex flex-col">
      {/* Top Bar */}
      <WorkflowTopBar
        workflowName={workflowName}
        onWorkflowNameChange={setWorkflowName}
        nodeCount={sampleNodes.length}
        edgeCount={sampleEdges.length}
      />

      {/* Main Area: 3 panels */}
      <div className="flex-1 flex min-h-0">
        {/* Left: Node Palette */}
        <NodePalette />

        {/* Center: Canvas */}
        <ReactFlowProvider>
          <FlowCanvasInner onNodeSelect={setSelectedNode} />
        </ReactFlowProvider>

        {/* Right: Properties */}
        <NodePropertiesPanel
          node={selectedNode}
          onClose={() => setSelectedNode(null)}
        />
      </div>
    </div>
  );
}
