'use client';

import { useState, useCallback } from 'react';
import { Plus, Trash2, Play, Copy, Save, RotateCcw, HelpCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface WorkflowNode {
  id: string;
  type: 'trigger' | 'agent' | 'action' | 'output';
  name: string;
  description: string;
  config: Record<string, unknown>;
}

interface WorkflowEdge {
  from: string;
  to: string;
}

export function WorkflowCanvas() {
  const [workflows, setWorkflows] = useState<Array<{ id: string; name: string; nodes: WorkflowNode[]; edges: WorkflowEdge[] }>>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null);
  const [newWorkflowName, setNewWorkflowName] = useState('');

  const currentWorkflow = workflows.find((w) => w.id === selectedWorkflow);

  const createWorkflow = useCallback(() => {
    if (!newWorkflowName.trim()) return;
    const id = `workflow-${Date.now()}`;
    setWorkflows((prev) => [
      ...prev,
      {
        id,
        name: newWorkflowName,
        nodes: [],
        edges: [],
      },
    ]);
    setSelectedWorkflow(id);
    setNewWorkflowName('');
  }, [newWorkflowName]);

  const deleteWorkflow = useCallback((id: string) => {
    setWorkflows((prev) => prev.filter((w) => w.id !== id));
    if (selectedWorkflow === id) {
      setSelectedWorkflow(workflows.length > 1 ? workflows[0].id : null);
    }
  }, [selectedWorkflow, workflows]);

  const addNode = useCallback(
    (type: WorkflowNode['type']) => {
      if (!selectedWorkflow) return;
      const nodeId = `node-${Date.now()}`;
      const newNode: WorkflowNode = {
        id: nodeId,
        type,
        name: `${type.charAt(0).toUpperCase() + type.slice(1)} Node`,
        description: `New ${type} node`,
        config: {},
      };
      setWorkflows((prev) =>
        prev.map((w) =>
          w.id === selectedWorkflow
            ? { ...w, nodes: [...w.nodes, newNode] }
            : w
        )
      );
    },
    [selectedWorkflow]
  );

  const removeNode = useCallback(
    (nodeId: string) => {
      if (!selectedWorkflow) return;
      setWorkflows((prev) =>
        prev.map((w) =>
          w.id === selectedWorkflow
            ? {
              ...w,
              nodes: w.nodes.filter((n) => n.id !== nodeId),
              edges: w.edges.filter((e) => e.from !== nodeId && e.to !== nodeId),
            }
            : w
        )
      );
    },
    [selectedWorkflow]
  );

  const nodeTypeColors: Record<string, string> = {
    trigger: 'bg-orange-400/10 border-orange-400/20 text-orange-400',
    agent: 'bg-cyber-cyan/10 border-cyber-cyan/20 text-cyber-cyan',
    action: 'bg-emerald-400/10 border-emerald-400/20 text-emerald-400',
    output: 'bg-cyber-purple/10 border-cyber-purple/20 text-cyber-purple',
  };

  return (
    <div className="h-full flex gap-4 p-4 overflow-hidden">
      {/* Left Panel: Workflow List */}
      <div className="w-[240px] flex flex-col gap-3 shrink-0">
        <div className="cyber-panel p-3">
          <h3 className="text-xs font-semibold text-foreground mb-2">Workflows</h3>
          <div className="space-y-1 max-h-[300px] overflow-y-auto">
            {workflows.length === 0 ? (
              <p className="text-[10px] text-muted-foreground italic">No workflows yet</p>
            ) : (
              workflows.map((w) => (
                <button
                  key={w.id}
                  onClick={() => setSelectedWorkflow(w.id)}
                  className={cn(
                    'w-full text-left px-2 py-1.5 rounded text-[10px] transition-all',
                    selectedWorkflow === w.id
                      ? 'bg-cyber-cyan/20 border border-cyber-cyan/30 text-cyber-cyan'
                      : 'bg-surface-2 border border-border text-muted-foreground hover:text-foreground'
                  )}
                >
                  <div className="truncate font-medium">{w.name}</div>
                  <div className="text-[9px] text-muted-foreground/60">{w.nodes.length} nodes</div>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Create Workflow */}
        <div className="cyber-panel p-3 space-y-2">
          <input
            type="text"
            placeholder="Workflow name..."
            value={newWorkflowName}
            onChange={(e) => setNewWorkflowName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && createWorkflow()}
            className="w-full h-7 px-2 text-[10px] bg-surface-0 border border-border rounded text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-cyber-cyan/50"
          />
          <button
            onClick={createWorkflow}
            className="w-full flex items-center justify-center gap-1.5 px-2 py-1.5 rounded bg-cyber-cyan/10 border border-cyber-cyan/30 text-[10px] text-cyber-cyan hover:bg-cyber-cyan/20 transition-all"
          >
            <Plus className="h-3 w-3" /> New
          </button>
        </div>
      </div>

      {/* Right Panel: Workflow Editor */}
      <div className="flex-1 flex flex-col min-w-0">
        {!currentWorkflow ? (
          <div className="cyber-panel flex-1 flex flex-col items-center justify-center">
            <HelpCircle className="h-12 w-12 text-muted-foreground/30 mb-3" />
            <p className="text-sm font-semibold text-foreground">No workflow selected</p>
            <p className="text-[10px] text-muted-foreground mt-1">Create a new workflow to get started</p>
          </div>
        ) : (
          <>
            {/* Editor Header */}
            <div className="cyber-panel p-3 mb-3 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-foreground">{currentWorkflow.name}</p>
                <p className="text-[9px] text-muted-foreground">{currentWorkflow.nodes.length} nodes</p>
              </div>
              <div className="flex items-center gap-2">
                <button className="flex items-center gap-1 px-2 py-1 rounded text-[10px] bg-surface-2 border border-border text-muted-foreground hover:text-cyber-cyan transition-all">
                  <Play className="h-3 w-3" /> Execute
                </button>
                <button
                  onClick={() => deleteWorkflow(currentWorkflow.id)}
                  className="flex items-center gap-1 px-2 py-1 rounded text-[10px] bg-surface-2 border border-border text-muted-foreground hover:text-cyber-red transition-all"
                >
                  <Trash2 className="h-3 w-3" />
                </button>
              </div>
            </div>

            {/* Nodes */}
            <div className="flex-1 cyber-panel p-4 overflow-y-auto space-y-2">
              {currentWorkflow.nodes.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <p className="text-[10px] text-muted-foreground mb-3">No nodes in this workflow</p>
                  <p className="text-[9px] text-muted-foreground/60">Add nodes using the buttons below</p>
                </div>
              ) : (
                currentWorkflow.nodes.map((node, idx) => (
                  <div
                    key={node.id}
                    className={cn(
                      'flex items-center gap-3 p-3 rounded-lg border',
                      nodeTypeColors[node.type]
                    )}
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-[11px] font-medium text-foreground truncate">{node.name}</p>
                      <p className="text-[9px] text-muted-foreground truncate">{node.description}</p>
                    </div>
                    {idx < currentWorkflow.nodes.length - 1 && (
                      <div className="text-muted-foreground/30 text-xs">↓</div>
                    )}
                    <button
                      onClick={() => removeNode(node.id)}
                      className="p-1 hover:bg-black/20 rounded transition-all"
                    >
                      <Trash2 className="h-3 w-3" />
                    </button>
                  </div>
                ))
              )}
            </div>

            {/* Add Nodes */}
            <div className="cyber-panel p-3 grid grid-cols-4 gap-2 mt-3">
              {(['trigger', 'agent', 'action', 'output'] as const).map((type) => (
                <button
                  key={type}
                  onClick={() => addNode(type)}
                  className="flex items-center justify-center px-2 py-1.5 rounded text-[10px] bg-surface-2 border border-border text-muted-foreground hover:text-foreground transition-all capitalize"
                >
                  <Plus className="h-3 w-3 mr-1" /> {type}
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
