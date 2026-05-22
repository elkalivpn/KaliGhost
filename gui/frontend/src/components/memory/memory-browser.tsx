'use client';

import { useState } from 'react';
import { Search, Download, Upload, Plus, Trash2, Eye, EyeOff, Copy, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MemoryEntry {
  id: string;
  agentId: string;
  content: string;
  type: 'conversation' | 'task' | 'result' | 'error';
  timestamp: string;
  tags: string[];
}

export function MemoryBrowser() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [entries, setEntries] = useState<MemoryEntry[]>([]);
  const [copied, setCopied] = useState(false);

  const typeColors: Record<string, string> = {
    conversation: 'text-cyber-blue bg-cyber-blue/10 border-cyber-blue/20',
    task: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
    result: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
    error: 'text-cyber-red bg-cyber-red/10 border-cyber-red/20',
  };

  const filteredEntries = entries.filter((e) => {
    const matchesSearch = !searchQuery || 
      e.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesType = filterType === 'all' || e.type === filterType;
    return matchesSearch && matchesType;
  });

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4 grid-bg">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-foreground">Agent Memory Database</h3>
          <p className="text-[10px] text-muted-foreground mt-0.5">{entries.length} entries stored</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-2 border border-border text-[10px] text-muted-foreground hover:text-cyber-cyan transition-all">
            <Download className="h-3 w-3" /> Export
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-2 border border-border text-[10px] text-muted-foreground hover:text-cyber-cyan transition-all">
            <Upload className="h-3 w-3" /> Import
          </button>
        </div>
      </div>

      {/* Search & Filter */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search memory..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-8 pl-9 pr-4 text-xs bg-surface-2 border border-border rounded-lg text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-cyber-cyan/50 transition-all"
          />
        </div>
        <div className="flex items-center gap-1.5">
          {['all', 'conversation', 'task', 'result', 'error'].map((type) => (
            <button
              key={type}
              onClick={() => setFilterType(type)}
              className={cn(
                'px-2 py-1 rounded text-[10px] capitalize border transition-all',
                filterType === type
                  ? 'border-cyber-cyan/30 bg-cyber-cyan/10 text-cyber-cyan'
                  : 'border-border text-muted-foreground hover:text-foreground'
              )}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* Empty State */}
      {entries.length === 0 ? (
        <div className="cyber-panel p-12 flex flex-col items-center justify-center text-center">
          <div className="w-12 h-12 rounded-lg bg-surface-2 border border-border flex items-center justify-center mb-4">
            <Search className="h-6 w-6 text-muted-foreground" />
          </div>
          <p className="text-sm font-semibold text-foreground mb-1">No Memory Entries Yet</p>
          <p className="text-xs text-muted-foreground max-w-xs">Agent memory entries will appear here as tasks are executed and results are processed.</p>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/30 text-[10px] text-cyber-cyan hover:bg-cyber-cyan/20 transition-all mt-4">
            <Plus className="h-3 w-3" /> Create Manual Entry
          </button>
        </div>
      ) : (
        <div className="cyber-panel p-4">
          <table className="w-full text-[11px]">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left px-3 py-2 text-muted-foreground font-medium">Type</th>
                <th className="text-left px-3 py-2 text-muted-foreground font-medium">Content</th>
                <th className="text-left px-3 py-2 text-muted-foreground font-medium">Tags</th>
                <th className="text-left px-3 py-2 text-muted-foreground font-medium">Time</th>
                <th className="text-center px-3 py-2 text-muted-foreground font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map((entry) => (
                <tr key={entry.id} className="border-b border-border/50 hover:bg-surface-2/50 transition-colors">
                  <td className="px-3 py-2">
                    <span className={cn('px-1.5 py-0.5 rounded text-[9px] border capitalize', typeColors[entry.type])}>
                      {entry.type}
                    </span>
                  </td>
                  <td className="px-3 py-2 text-muted-foreground truncate max-w-xs">{entry.content}</td>
                  <td className="px-3 py-2 flex flex-wrap gap-1">
                    {entry.tags.map((tag) => (
                      <span key={tag} className="px-1 py-0.5 rounded text-[8px] bg-surface-3 text-muted-foreground">
                        {tag}
                      </span>
                    ))}
                  </td>
                  <td className="px-3 py-2 text-muted-foreground font-mono text-[10px]">{entry.timestamp}</td>
                  <td className="px-3 py-2 flex items-center justify-center gap-1">
                    <button className="p-1 hover:bg-surface-3 rounded transition-colors">
                      <Copy className="h-3 w-3 text-muted-foreground hover:text-cyber-cyan" />
                    </button>
                    <button className="p-1 hover:bg-surface-3 rounded transition-colors">
                      <Trash2 className="h-3 w-3 text-muted-foreground hover:text-cyber-red" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-4 gap-3">
        <div className="cyber-panel p-3 text-center">
          <p className="text-[10px] text-muted-foreground">Total Entries</p>
          <p className="text-lg font-mono font-bold text-cyber-cyan mt-1">{entries.length}</p>
        </div>
        <div className="cyber-panel p-3 text-center">
          <p className="text-[10px] text-muted-foreground">Conversations</p>
          <p className="text-lg font-mono font-bold text-cyber-blue mt-1">{entries.filter(e => e.type === 'conversation').length}</p>
        </div>
        <div className="cyber-panel p-3 text-center">
          <p className="text-[10px] text-muted-foreground">Results</p>
          <p className="text-lg font-mono font-bold text-emerald-400 mt-1">{entries.filter(e => e.type === 'result').length}</p>
        </div>
        <div className="cyber-panel p-3 text-center">
          <p className="text-[10px] text-muted-foreground">Errors</p>
          <p className="text-lg font-mono font-bold text-cyber-red mt-1">{entries.filter(e => e.type === 'error').length}</p>
        </div>
      </div>
    </div>
  );
}
