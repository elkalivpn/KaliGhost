'use client';

import { memo } from 'react';
import type { NodeProps } from '@xyflow/react';
import { Handle, Position } from '@xyflow/react';
import { Badge } from '@/components/ui/badge';
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
} from 'lucide-react';
import type { WorkflowNodeCategory } from '@/types';

/* ── Icon map keyed by the `icon` string stored in node data ── */
const iconMap: Record<string, React.ReactNode> = {
  zap: <Zap className="h-3.5 w-3.5" />,
  globe: <Globe className="h-3.5 w-3.5" />,
  clock: <Clock className="h-3.5 w-3.5" />,
  radio: <Radio className="h-3.5 w-3.5" />,
  bot: <Bot className="h-3.5 w-3.5" />,
  shield: <Shield className="h-3.5 w-3.5" />,
  search: <Search className="h-3.5 w-3.5" />,
  filetext: <FileText className="h-3.5 w-3.5" />,
  eye: <Eye className="h-3.5 w-3.5" />,
  play: <Play className="h-3.5 w-3.5" />,
  terminal: <Terminal className="h-3.5 w-3.5" />,
  filecode: <FileCode className="h-3.5 w-3.5" />,
  gitbranch: <GitBranch className="h-3.5 w-3.5" />,
  shuffle: <Shuffle className="h-3.5 w-3.5" />,
  repeat: <Repeat className="h-3.5 w-3.5" />,
  gitmerge: <GitMerge className="h-3.5 w-3.5" />,
  timer: <Timer className="h-3.5 w-3.5" />,
  split: <Split className="h-3.5 w-3.5" />,
  filter: <Filter className="h-3.5 w-3.5" />,
  arrowleftright: <ArrowLeftRight className="h-3.5 w-3.5" />,
  arrowupdown: <ArrowUpDown className="h-3.5 w-3.5" />,
  layers: <Layers className="h-3.5 w-3.5" />,
  send: <Send className="h-3.5 w-3.5" />,
  bell: <Bell className="h-3.5 w-3.5" />,
  filedown: <FileDown className="h-3.5 w-3.5" />,
  database: <Database className="h-3.5 w-3.5" />,
};

/* ── Category → colour mapping ── */
const categoryStyles: Record<
  WorkflowNodeCategory,
  {
    accent: string;
    bg: string;
    border: string;
    handle: string;
    progressFrom: string;
    progressTo: string;
    headerBg: string;
  }
> = {
  trigger: {
    accent: 'text-orange-400',
    bg: 'bg-orange-400/5',
    border: 'border-orange-400/25',
    handle: 'bg-orange-400',
    progressFrom: 'from-orange-400',
    progressTo: 'to-red-500',
    headerBg: 'bg-gradient-to-r from-orange-500/10 to-red-500/10',
  },
  agent: {
    accent: 'text-cyber-cyan',
    bg: 'bg-cyber-cyan/5',
    border: 'border-cyber-cyan/25',
    handle: 'bg-cyber-cyan',
    progressFrom: 'from-cyber-cyan',
    progressTo: 'to-cyber-blue',
    headerBg: 'bg-gradient-to-r from-cyan-500/10 to-blue-500/10',
  },
  action: {
    accent: 'text-emerald-400',
    bg: 'bg-emerald-400/5',
    border: 'border-emerald-400/25',
    handle: 'bg-emerald-400',
    progressFrom: 'from-emerald-400',
    progressTo: 'to-green-500',
    headerBg: 'bg-gradient-to-r from-emerald-500/10 to-green-500/10',
  },
  logic: {
    accent: 'text-amber-400',
    bg: 'bg-amber-400/5',
    border: 'border-amber-400/25',
    handle: 'bg-amber-400',
    progressFrom: 'from-amber-400',
    progressTo: 'to-yellow-500',
    headerBg: 'bg-gradient-to-r from-amber-500/10 to-yellow-500/10',
  },
  output: {
    accent: 'text-violet-400',
    bg: 'bg-violet-400/5',
    border: 'border-violet-400/25',
    handle: 'bg-violet-400',
    progressFrom: 'from-violet-400',
    progressTo: 'to-purple-500',
    headerBg: 'bg-gradient-to-r from-violet-500/10 to-purple-500/10',
  },
  transform: {
    accent: 'text-sky-400',
    bg: 'bg-sky-400/5',
    border: 'border-sky-400/25',
    handle: 'bg-sky-400',
    progressFrom: 'from-sky-400',
    progressTo: 'to-blue-500',
    headerBg: 'bg-gradient-to-r from-sky-500/10 to-blue-500/10',
  },
};

const statusVariant: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
  running: 'default',
  idle: 'secondary',
  error: 'destructive',
  success: 'outline',
  pending: 'secondary',
};

const statusLabel: Record<string, string> = {
  running: 'Running',
  idle: 'Idle',
  error: 'Error',
  success: 'Success',
  pending: 'Pending',
};

/* ── Shared node renderer used by all node types ── */
interface WorkflowNodeData {
  label: string;
  description?: string;
  status?: string;
  progress?: number;
  icon?: string;
  color?: string;
  category?: WorkflowNodeCategory;
  [key: string]: unknown;
}

function WorkflowNodeShell({
  data,
  selected,
}: {
  data: WorkflowNodeData;
  selected: boolean;
}) {
  const cat = data.category ?? 'agent';
  const styles = categoryStyles[cat];
  const status = data.status ?? 'idle';
  const progress = data.progress ?? 0;

  return (
    <div
      className={`
        relative min-w-[200px] max-w-[240px] rounded-lg overflow-hidden
        bg-surface-1 border ${selected ? 'border-foreground/30' : styles.border}
        transition-all duration-150
        ${selected ? 'shadow-lg' : 'shadow-md'}
      `}
      style={{
        boxShadow: selected
          ? `0 0 12px ${styles.handle === 'bg-orange-400' ? 'rgba(251,146,60,0.2)' : styles.handle === 'bg-cyber-cyan' ? 'rgba(0,240,255,0.2)' : styles.handle === 'bg-emerald-400' ? 'rgba(52,211,153,0.2)' : styles.handle === 'bg-amber-400' ? 'rgba(251,191,36,0.2)' : styles.handle === 'bg-violet-400' ? 'rgba(167,139,250,0.2)' : 'rgba(56,189,248,0.2)'}, 0 0 32px rgba(0,0,0,0.4)`
          : undefined,
      }}
    >
      {/* Input Handle */}
      <Handle
        type="target"
        position={Position.Left}
        className={`!w-2.5 !h-2.5 !border-2 !border-surface-1 ${styles.handle} !-left-[5px]`}
      />

      {/* Header */}
      <div className={`px-3 py-2 ${styles.headerBg} border-b border-border`}>
        <div className="flex items-center gap-2">
          <div
            className={`h-7 w-7 rounded-md flex items-center justify-center ${styles.bg} ${styles.accent}`}
          >
            {iconMap[data.icon ?? 'bot'] ?? <Bot className="h-3.5 w-3.5" />}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-foreground truncate leading-tight">
              {data.label}
            </p>
            {data.description && (
              <p className="text-[9px] text-muted-foreground truncate mt-0.5">
                {data.description}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Body */}
      <div className="px-3 py-2 flex items-center gap-2">
        <Badge
          variant={statusVariant[status] ?? 'secondary'}
          className="text-[9px] h-4 px-1.5 font-mono"
        >
          {statusLabel[status] ?? status}
        </Badge>
        <div className="flex-1 flex items-center gap-1.5">
          <div className="flex-1 h-1 bg-surface-0 rounded-full overflow-hidden">
            <div
              className={`h-full bg-gradient-to-r ${styles.progressFrom} ${styles.progressTo} rounded-full transition-all`}
              style={{ width: `${progress}%` }}
            />
          </div>
          <span className="text-[9px] text-muted-foreground font-mono w-6 text-right">
            {progress}%
          </span>
        </div>
      </div>

      {/* Output Handle */}
      <Handle
        type="source"
        position={Position.Right}
        className={`!w-2.5 !h-2.5 !border-2 !border-surface-1 ${styles.handle} !-right-[5px]`}
      />
    </div>
  );
}

/* ── Memoised node components ── */

function TriggerNodeInner(props: NodeProps) {
  const d = props.data as WorkflowNodeData;
  return (
    <WorkflowNodeShell
      data={{ ...d, category: 'trigger' }}
      selected={!!props.selected}
    />
  );
}

function AgentNodeInner(props: NodeProps) {
  const d = props.data as WorkflowNodeData;
  return (
    <WorkflowNodeShell
      data={{ ...d, category: 'agent' }}
      selected={!!props.selected}
    />
  );
}

function ActionNodeInner(props: NodeProps) {
  const d = props.data as WorkflowNodeData;
  return (
    <WorkflowNodeShell
      data={{ ...d, category: 'action' }}
      selected={!!props.selected}
    />
  );
}

function LogicNodeInner(props: NodeProps) {
  const d = props.data as WorkflowNodeData;
  return (
    <WorkflowNodeShell
      data={{ ...d, category: 'logic' }}
      selected={!!props.selected}
    />
  );
}

function OutputNodeInner(props: NodeProps) {
  const d = props.data as WorkflowNodeData;
  return (
    <WorkflowNodeShell
      data={{ ...d, category: 'output' }}
      selected={!!props.selected}
    />
  );
}

function TransformNodeInner(props: NodeProps) {
  const d = props.data as WorkflowNodeData;
  return (
    <WorkflowNodeShell
      data={{ ...d, category: 'transform' }}
      selected={!!props.selected}
    />
  );
}

export const TriggerNode = memo(TriggerNodeInner);
export const AgentNode = memo(AgentNodeInner);
export const ActionNode = memo(ActionNodeInner);
export const LogicNode = memo(LogicNodeInner);
export const OutputNode = memo(OutputNodeInner);
export const TransformNode = memo(TransformNodeInner);
