'use client';

import { useState, useMemo } from 'react';
import { Search, Filter, ChevronDown, ChevronUp, X, Tag } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { MemoryEntry } from '@/types';

const mockMemoryEntries: MemoryEntry[] = [
  {
    id: 'mem-001',
    agentId: 'agent-001',
    agentName: 'Recon Agent',
    type: 'task',
    content: 'Initiated subnet scan on 192.168.1.0/24. Discovered 14 active hosts with varying OS fingerprints. 3 hosts running Windows Server 2022, 8 hosts running Ubuntu 22.04, 2 hosts running macOS Ventura, 1 host running Kali Linux (honeypot detected).',
    timestamp: '2024-06-15 14:23:11',
    size: '1.2 KB',
    tags: ['network', 'recon', 'scan'],
  },
  {
    id: 'mem-002',
    agentId: 'agent-002',
    agentName: 'Scanner Agent',
    type: 'result',
    content: 'Port scan results for 10.0.0.0/24: Found 23 open ports across 8 hosts. Critical findings: Port 22 (SSH) open on 5 hosts with weak key exchange algorithms. Port 3306 (MySQL) exposed on 10.0.0.15 with default credentials. Port 445 (SMB) open on 3 hosts with SMBv1 enabled.',
    timestamp: '2024-06-15 14:18:45',
    size: '2.4 KB',
    tags: ['ports', 'vulnerability', 'critical'],
  },
  {
    id: 'mem-003',
    agentId: 'agent-003',
    agentName: 'Exploit Agent',
    type: 'error',
    content: 'Exploit attempt for CVE-2024-3094 (XZ Utils backdoor) failed on target 10.0.0.15. Target system is not running affected XZ Utils version. Error: VERSION_MISMATCH. Recommended action: Try alternate exploit chain or pivot to different vulnerability.',
    timestamp: '2024-06-15 14:12:33',
    size: '0.8 KB',
    tags: ['exploit', 'failed', 'cve-2024-3094'],
  },
  {
    id: 'mem-004',
    agentId: 'agent-001',
    agentName: 'Recon Agent',
    type: 'conversation',
    content: 'User instructed: "Focus on the DMZ segment 10.0.0.0/24 first, then move to internal network 172.16.0.0/16. Pay special attention to web-facing services." Agent acknowledged and adjusted scan priorities accordingly.',
    timestamp: '2024-06-15 14:05:00',
    size: '0.6 KB',
    tags: ['instruction', 'priority'],
  },
  {
    id: 'mem-005',
    agentId: 'agent-004',
    agentName: 'Report Agent',
    type: 'result',
    content: 'Executive summary generated for Q2 2024 penetration test. Total findings: 12 Critical, 28 High, 45 Medium, 67 Low. Key recommendations: Patch CVE-2024-3094 immediately, disable SMBv1 across all servers, implement network segmentation between DMZ and internal network.',
    timestamp: '2024-06-15 13:55:22',
    size: '3.1 KB',
    tags: ['report', 'executive', 'summary'],
  },
  {
    id: 'mem-006',
    agentId: 'agent-002',
    agentName: 'Scanner Agent',
    type: 'task',
    content: 'Running service version detection on discovered hosts. Using Nmap -sV with aggressive timing template. Current progress: 8/14 hosts completed. Identified services: Apache 2.4.52, nginx 1.18.0, OpenSSH 8.9p1, MySQL 8.0.32, PostgreSQL 15.2.',
    timestamp: '2024-06-15 13:48:10',
    size: '1.5 KB',
    tags: ['service-detection', 'nmap', 'in-progress'],
  },
  {
    id: 'mem-007',
    agentId: 'agent-005',
    agentName: 'Monitor Agent',
    type: 'result',
    content: 'IDS alert analysis: 3 false positives identified in the last hour from Snort ruleset ET SCAN. Legitimate traffic from internal monitoring system was flagged. Rule SID 2000127 needs tuning. No actual intrusion attempts detected.',
    timestamp: '2024-06-15 13:42:55',
    size: '0.9 KB',
    tags: ['ids', 'false-positive', 'snort'],
  },
  {
    id: 'mem-008',
    agentId: 'agent-006',
    agentName: 'Payload Agent',
    type: 'task',
    content: 'Crafting custom reverse shell payload for Linux x86_64 target. Using msfvenom with custom encoder chain to bypass EDR. Payload type: meterpreter/reverse_tcp. LHOST: 10.10.10.1, LPORT: 4444. Encoding: shikata_ga_nai x5 + xor_dynamic.',
    timestamp: '2024-06-15 13:35:18',
    size: '1.1 KB',
    tags: ['payload', 'msfvenom', 'custom'],
  },
  {
    id: 'mem-009',
    agentId: 'agent-003',
    agentName: 'Exploit Agent',
    type: 'result',
    content: 'Successfully exploited CVE-2023-44487 (HTTP/2 Rapid Reset) on target 10.0.0.20 (nginx 1.18.0). Gained low-privilege shell access. Privilege escalation attempt in progress using kernel exploit CVE-2023-32233.',
    timestamp: '2024-06-15 13:28:44',
    size: '1.8 KB',
    tags: ['exploit', 'success', 'http2', 'privilege-escalation'],
  },
  {
    id: 'mem-010',
    agentId: 'agent-001',
    agentName: 'Recon Agent',
    type: 'conversation',
    content: 'Agent reported: "Honeypot detected at 192.168.1.100 running Cowrie. All interaction data is being logged by the blue team. Recommend excluding this host from further testing and documenting the finding." User approved exclusion.',
    timestamp: '2024-06-15 13:20:05',
    size: '0.7 KB',
    tags: ['honeypot', 'cowrie', 'blue-team'],
  },
];

const typeColors: Record<string, string> = {
  conversation: 'text-cyber-blue bg-cyber-blue/10 border-cyber-blue/20',
  task: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  result: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  error: 'text-cyber-red bg-cyber-red/10 border-cyber-red/20',
};

export function MemoryBrowser() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [sortAsc, setSortAsc] = useState(true);

  const filteredEntries = useMemo(() => {
    let entries = [...mockMemoryEntries];

    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      entries = entries.filter(
        (e) =>
          e.agentName.toLowerCase().includes(q) ||
          e.content.toLowerCase().includes(q) ||
          e.tags.some((t) => t.toLowerCase().includes(q))
      );
    }

    if (filterType !== 'all') {
      entries = entries.filter((e) => e.type === filterType);
    }

    entries.sort((a, b) => {
      const cmp = a.timestamp.localeCompare(b.timestamp);
      return sortAsc ? -cmp : cmp;
    });

    return entries;
  }, [searchQuery, filterType, sortAsc]);

  return (
    <div className="h-full flex flex-col p-4 gap-4 grid-bg">
      {/* Header */}
      <div className="flex items-center justify-between shrink-0">
        <div>
          <h3 className="text-sm font-semibold text-foreground">Agent Memory Database</h3>
          <p className="text-[10px] text-muted-foreground mt-0.5">{mockMemoryEntries.length} entries across 6 agents</p>
        </div>
      </div>

      {/* Search & Filter */}
      <div className="flex items-center gap-3 shrink-0">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search memory entries..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-8 pl-9 pr-4 text-xs bg-surface-2 border border-border rounded-lg text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-cyber-cyan/50 transition-all"
          />
        </div>
        <div className="flex items-center gap-1.5">
          <Filter className="h-3.5 w-3.5 text-muted-foreground" />
          {['all', 'conversation', 'task', 'result', 'error'].map((type) => (
            <button
              key={type}
              onClick={() => setFilterType(type)}
              className={cn(
                'px-2 py-1 rounded text-[10px] capitalize border transition-all',
                filterType === type
                  ? 'border-cyber-cyan/30 bg-cyber-cyan/10 text-cyber-cyan'
                  : 'border-border text-muted-foreground hover:text-foreground hover:border-surface-3'
              )}
            >
              {type}
            </button>
          ))}
        </div>
        <button
          onClick={() => setSortAsc(!sortAsc)}
          className="flex items-center gap-1 px-2 py-1 rounded text-[10px] border border-border text-muted-foreground hover:text-foreground transition-colors"
        >
          {sortAsc ? <ChevronDown className="h-3 w-3" /> : <ChevronUp className="h-3 w-3" />}
          Time
        </button>
      </div>

      {/* Table */}
      <div className="flex-1 overflow-hidden cyber-panel">
        <div className="overflow-x-auto h-full">
          <table className="w-full text-[11px]">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left px-3 py-2.5 text-muted-foreground font-medium">Agent</th>
                <th className="text-left px-3 py-2.5 text-muted-foreground font-medium">Type</th>
                <th className="text-left px-3 py-2.5 text-muted-foreground font-medium">Content</th>
                <th className="text-left px-3 py-2.5 text-muted-foreground font-medium">Tags</th>
                <th className="text-left px-3 py-2.5 text-muted-foreground font-medium">Timestamp</th>
                <th className="text-left px-3 py-2.5 text-muted-foreground font-medium">Size</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map((entry) => (
                <tr key={entry.id} onClick={() => setExpandedId(expandedId === entry.id ? null : entry.id)} className="border-b border-border/50 hover:bg-surface-2/50 cursor-pointer transition-colors">
                  <td className="px-3 py-2.5 text-foreground font-medium">{entry.agentName}</td>
                  <td className="px-3 py-2.5">
                    <span className={cn('px-1.5 py-0.5 rounded-full text-[9px] border capitalize', typeColors[entry.type])}>
                      {entry.type}
                    </span>
                  </td>
                  <td className="px-3 py-2.5 text-muted-foreground max-w-xs truncate">{entry.content}</td>
                  <td className="px-3 py-2.5">
                    <div className="flex items-center gap-1 flex-wrap">
                      {entry.tags.slice(0, 2).map((tag) => (
                        <span key={tag} className="px-1 py-0.5 rounded text-[8px] bg-surface-3 text-muted-foreground">
                          {tag}
                        </span>
                      ))}
                      {entry.tags.length > 2 && (
                        <span className="text-[8px] text-muted-foreground">+{entry.tags.length - 2}</span>
                      )}
                    </div>
                  </td>
                  <td className="px-3 py-2.5 text-muted-foreground font-mono whitespace-nowrap">{entry.timestamp}</td>
                  <td className="px-3 py-2.5 text-muted-foreground font-mono">{entry.size}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Expanded Detail Modal */}
      {expandedId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={() => setExpandedId(null)}>
          <div className="cyber-panel glow-cyan-strong w-full max-w-2xl max-h-[80vh] m-4 flex flex-col" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between px-4 py-3 border-b border-border">
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-foreground">
                  {mockMemoryEntries.find((e) => e.id === expandedId)?.agentName}
                </span>
                <span className={cn('px-1.5 py-0.5 rounded-full text-[9px] border capitalize', typeColors[mockMemoryEntries.find((e) => e.id === expandedId)?.type || 'task'])}>
                  {mockMemoryEntries.find((e) => e.id === expandedId)?.type}
                </span>
              </div>
              <button onClick={() => setExpandedId(null)} className="text-muted-foreground hover:text-foreground">
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              <p className="text-xs text-foreground leading-relaxed mb-4">
                {mockMemoryEntries.find((e) => e.id === expandedId)?.content}
              </p>
              <div className="flex items-center gap-2 flex-wrap">
                <Tag className="h-3 w-3 text-muted-foreground" />
                {mockMemoryEntries.find((e) => e.id === expandedId)?.tags.map((tag) => (
                  <span key={tag} className="px-2 py-0.5 rounded text-[10px] bg-surface-3 text-muted-foreground border border-border">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex items-center justify-between px-4 py-2 border-t border-border text-[10px] text-muted-foreground">
              <span className="font-mono">{mockMemoryEntries.find((e) => e.id === expandedId)?.timestamp}</span>
              <span className="font-mono">{mockMemoryEntries.find((e) => e.id === expandedId)?.size}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
