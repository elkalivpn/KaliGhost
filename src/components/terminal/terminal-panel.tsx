'use client';

import { useEffect, useRef, useState } from 'react';
import { Terminal as TerminalIcon, Plus, X } from 'lucide-react';

interface TerminalTab {
  id: string;
  label: string;
}

const initialHistory = [
  '\x1b[1;36m╔══════════════════════════════════════════════╗\x1b[0m',
  '\x1b[1;36m║     KALI DRAGON — AGENT CONTROL CENTER     ║\x1b[0m',
  '\x1b[1;36m║          Secure Terminal v3.2.1              ║\x1b[0m',
  '\x1b[1;36m╚══════════════════════════════════════════════╝\x1b[0m',
  '',
  '\x1b[32m[✓]\x1b[0m Connected to Dragon Core Engine',
  '\x1b[32m[✓]\x1b[0m Agent fleet synchronized (6 agents)',
  '\x1b[32m[✓]\x1b[0m Neural processing cores: 8/8 online',
  '',
  '\x1b[1;33mroot@kali-dragon:~#\x1b[0m nmap -sV -sC 192.168.1.0/24',
  '\x1b[90mStarting Nmap 7.94 ( https://nmap.org )\x1b[0m',
  '\x1b[90mNmap scan report for gateway (192.168.1.1)\x1b[0m',
  '\x1b[90mHost is up (0.0023s latency).\x1b[0m',
  '\x1b[32mPORT    STATE  SERVICE   VERSION\x1b[0m',
  '\x1b[37m22/tcp  open   ssh       OpenSSH 8.9p1\x1b[0m',
  '\x1b[37m80/tcp  open   http      Apache 2.4.52\x1b[0m',
  '\x1b[37m443/tcp open   ssl/http  Apache 2.4.52\x1b[0m',
  '\x1b[37m3306/tcp open mysql     MySQL 8.0.32\x1b[0m',
  '',
  '\x1b[1;33mroot@kali-dragon:~#\x1b[0m msfconsole -q',
  '\x1b[32m[*]\x1b[0m Metasploit Framework initialized',
  '\x1b[32m[*]\x1b[0m Loaded 2437 exploit modules',
  '\x1b[32m[*]\x1b[0m Loaded 1235 auxiliary modules',
  '',
];

const initialHistory2 = [
  '\x1b[1;36m╔══════════════════════════════════════════════╗\x1b[0m',
  '\x1b[1;36m║           SECONDARY TERMINAL                 ║\x1b[0m',
  '\x1b[1;36m╚══════════════════════════════════════════════╝\x1b[0m',
  '',
  '\x1b[1;33mroot@kali-dragon:~#\x1b[0m nikto -h https://target.local',
  '\x1b[90m- Nikto v2.1.6\x1b[0m',
  '\x1b[33m+ Server: Apache/2.4.52 (Ubuntu)\x1b[0m',
  '\x1b[33m+ /: The X-Content-Type-Options header is not set.\x1b[0m',
  '\x1b[32m+ 7915 requests: 0 error(s) and 23 item(s) reported\x1b[0m',
  '',
  '\x1b[1;33mroot@kali-dragon:~#\x1b[0m _',
];

function stripAnsi(str: string): string {
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

function parseLines(text: string): string[] {
  return text.split('\n');
}

function TerminalView({ history }: { history: string[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = useState('');
  const [lines, setLines] = useState<string[]>(history);
  const [commandHistory, setCommandHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [lines]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const cmd = input.trim();
      if (!cmd) return;

      const newLines = [...lines, `\x1b[1;33mroot@kali-dragon:~#\x1b[0m ${cmd}`];
      setCommandHistory((prev) => [...prev, cmd]);
      setHistoryIndex(-1);

      // Simulate command responses
      if (cmd === 'help') {
        newLines.push(
          '\x1b[36mAvailable commands:\x1b[0m',
          '  help       - Show this help',
          '  clear      - Clear terminal',
          '  agents     - List active agents',
          '  status     - System status',
          '  scan       - Run network scan',
          '  whoami     - Current user',
        );
      } else if (cmd === 'clear') {
        setLines([]);
        setInput('');
        return;
      } else if (cmd === 'agents') {
        newLines.push(
          '\x1b[32m[ACTIVE]\x1b[0m Recon Agent     — Scanning subnet 192.168.1.0/24',
          '\x1b[33m[BUSY]\x1b[0m   Scanner Agent   — Port scanning 10.0.0.1-254',
          '\x1b[31m[ERROR]\x1b[0m  Exploit Agent   — Attempting CVE-2024-3094',
          '\x1b[32m[ACTIVE]\x1b[0m Report Agent    — Generating pentest report',
          '\x1b[32m[ACTIVE]\x1b[0m Monitor Agent   — Watching IDS/IPS alerts',
        );
      } else if (cmd === 'status') {
        newLines.push(
          '\x1b[36mDragon Core v3.2.1 — Status Report\x1b[0m',
          '  Neural Cores: \x1b[32m8/8 Online\x1b[0m',
          '  CPU Usage:    \x1b[33m42.3%\x1b[0m',
          '  Memory:       \x1b[33m67.1% (4.3/6.4 GB)\x1b[0m',
          '  Network:      \x1b[32m1.2 GB/s\x1b[0m',
          '  Uptime:       \x1b[37m47d 12h 33m\x1b[0m',
        );
      } else if (cmd === 'whoami') {
        newLines.push('\x1b[32mroot (Dragon Core Administrator)\x1b[0m');
      } else if (cmd === 'scan') {
        newLines.push(
          '\x1b[33m[*]\x1b[0m Initiating network scan...',
          '\x1b[32m[✓]\x1b[0m Scan complete: 14 hosts discovered',
          '\x1b[32m[✓]\x1b[0m 23 open ports identified',
        );
      } else {
        newLines.push(`\x1b[31mbash: ${cmd}: command not found\x1b[0m`);
      }

      setLines(newLines);
      setInput('');
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (commandHistory.length > 0) {
        const newIndex = historyIndex === -1 ? commandHistory.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(newIndex);
        setInput(commandHistory[newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex !== -1) {
        const newIndex = historyIndex + 1;
        if (newIndex >= commandHistory.length) {
          setHistoryIndex(-1);
          setInput('');
        } else {
          setHistoryIndex(newIndex);
          setInput(commandHistory[newIndex]);
        }
      }
    }
  };

  return (
    <div
      className="h-full w-full bg-[#0d1117] font-mono text-xs cursor-text overflow-hidden"
      onClick={() => inputRef.current?.focus()}
    >
      <div ref={containerRef} className="h-full overflow-y-auto p-3 pb-12">
        {lines.map((line, i) => (
          <div key={i} className="leading-5 whitespace-pre-wrap break-all">
            <span dangerouslySetInnerHTML={{ __html: line.replace(/\x1b\[[0-9;]*m/g, (match) => {
              const codes = match.slice(2, -1).split(';').map(Number);
              let style = '';
              let className = '';
              if (codes.includes(1)) className += 'font-bold ';
              if (codes.includes(0) && codes.length === 1) return '';
              if (codes.includes(31) || codes.includes(1) && codes.includes(31)) className += 'text-red-400';
              else if (codes.includes(32)) className += 'text-green-400';
              else if (codes.includes(33)) className += 'text-yellow-400';
              else if (codes.includes(36)) className += 'text-cyan-400';
              else if (codes.includes(37)) className += 'text-gray-300';
              else if (codes.includes(90)) className += 'text-gray-500';
              return `<span class="${className}">`;
            }).replace(/\x1b\[0m/g, '</span>') }} />
          </div>
        ))}

        {/* Input line */}
        <div className="flex items-center leading-5">
          <span className="text-yellow-400 font-bold">root@kali-dragon:~#&nbsp;</span>
          <div className="relative flex-1">
            <input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full bg-transparent text-gray-200 outline-none caret-cyan-400"
              autoFocus
              spellCheck={false}
            />
          </div>
          <span className="inline-block w-2 h-4 bg-cyan-400 animate-cursor-blink ml-0.5" />
        </div>
      </div>
    </div>
  );
}

export function TerminalPanel() {
  const [tabs, setTabs] = useState<TerminalTab[]>([
    { id: '1', label: 'Terminal 1' },
  ]);
  const [activeTab, setActiveTab] = useState('1');

  const addTab = () => {
    const newId = String(tabs.length + 1);
    setTabs([...tabs, { id: newId, label: `Terminal ${newId}` }]);
    setActiveTab(newId);
  };

  const removeTab = (id: string) => {
    if (tabs.length <= 1) return;
    const newTabs = tabs.filter((t) => t.id !== id);
    setTabs(newTabs);
    if (activeTab === id) {
      setActiveTab(newTabs[newTabs.length - 1].id);
    }
  };

  return (
    <div className="h-full flex flex-col bg-surface-0">
      {/* Tab Bar */}
      <div className="flex items-center gap-1 px-2 py-1.5 border-b border-border bg-surface-1 shrink-0">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-[11px] cursor-pointer transition-colors ${
              activeTab === tab.id
                ? 'bg-surface-2 text-foreground border border-border'
                : 'text-muted-foreground hover:text-foreground'
            }`}
            onClick={() => setActiveTab(tab.id)}
          >
            <TerminalIcon className="h-3 w-3" />
            <span>{tab.label}</span>
            {tabs.length > 1 && (
              <button
                onClick={(e) => { e.stopPropagation(); removeTab(tab.id); }}
                className="ml-1 hover:text-cyber-red transition-colors"
              >
                <X className="h-2.5 w-2.5" />
              </button>
            )}
          </div>
        ))}
        <button
          onClick={addTab}
          className="flex items-center justify-center w-5 h-5 rounded hover:bg-surface-2 text-muted-foreground hover:text-cyber-cyan transition-colors"
        >
          <Plus className="h-3 w-3" />
        </button>
        <div className="ml-auto flex items-center gap-2 text-[10px] text-muted-foreground">
          <span className="px-1.5 py-0.5 rounded bg-surface-2 border border-border">bash</span>
          <span className="font-mono">UTF-8</span>
        </div>
      </div>

      {/* Terminal Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === '1' && <TerminalView history={initialHistory} />}
        {activeTab === '2' && <TerminalView history={initialHistory2} />}
        {activeTab !== '1' && activeTab !== '2' && (
          <TerminalView history={[
            '',
            '\x1b[1;36m╔══════════════════════════════════════════════╗\x1b[0m',
            `\x1b[1;36m║           ${tabs.find(t => t.id === activeTab)?.label || 'Terminal'}                  ║\x1b[0m`,
            '\x1b[1;36m╚══════════════════════════════════════════════╝\x1b[0m',
            '',
            '\x1b[1;33mroot@kali-dragon:~#\x1b[0m _',
          ]} />
        )}
      </div>
    </div>
  );
}
