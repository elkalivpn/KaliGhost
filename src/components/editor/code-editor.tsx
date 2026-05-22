'use client';

import { useState } from 'react';
import MonacoEditor from '@monaco-editor/react';
import {
  File, Folder, FolderOpen, ChevronRight, ChevronDown,
  Save, X, ChevronLeft,
} from 'lucide-react';

interface FileItem {
  name: string;
  type: 'file' | 'folder';
  children?: FileItem[];
  language?: string;
  content?: string;
}

const fileTree: FileItem[] = [
  {
    name: 'pentest-tools',
    type: 'folder',
    children: [
      {
        name: 'scanner.py',
        type: 'file',
        language: 'python',
        content: `#!/usr/bin/env python3
"""
Kali Dragon - Network Scanner Module
Part of the Agent Control Center pentest toolkit
"""

import socket
import threading
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor

@dataclass
class ScanResult:
    """Represents a single port scan result."""
    host: str
    port: int
    state: str = "closed"
    service: str = "unknown"
    banner: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "host": self.host,
            "port": self.port,
            "state": self.state,
            "service": self.service,
            "banner": self.banner,
            "timestamp": self.timestamp,
        }

class NetworkScanner:
    """Multi-threaded network scanner with service detection."""

    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
                   443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

    def __init__(self, timeout: float = 1.0, max_threads: int = 100):
        self.timeout = timeout
        self.max_threads = max_threads
        self.results: List[ScanResult] = []
        self._lock = threading.Lock()

    def scan_port(self, host: str, port: int) -> Optional[ScanResult]:
        """Scan a single port on the target host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))

            if result == 0:
                banner = ""
                try:
                    sock.send(b"HEAD / HTTP/1.0\\r\\n\\r\\n")
                    banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
                except Exception:
                    pass

                scan_result = ScanResult(
                    host=host,
                    port=port,
                    state="open",
                    banner=banner,
                )
                with self._lock:
                    self.results.append(scan_result)
                return scan_result
        except Exception as e:
            print(f"[!] Error scanning {host}:{port} - {e}")
        finally:
            sock.close()
        return None

    def scan_host(self, host: str, ports: List[int] = None) -> List[ScanResult]:
        """Scan all specified ports on a target host."""
        ports = ports or self.COMMON_PORTS
        self.results = []

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [
                executor.submit(self.scan_port, host, port)
                for port in ports
            ]
            for future in futures:
                future.result()

        return self.results

    def generate_report(self) -> str:
        """Generate a formatted scan report."""
        open_ports = [r for r in self.results if r.state == "open"]
        report = [
            "=" * 60,
            "KALI DRAGON - Network Scan Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total ports scanned: {len(self.COMMON_PORTS)}",
            f"Open ports found: {len(open_ports)}",
            "=" * 60,
        ]
        for r in open_ports:
            report.append(f"  [{r.state.upper():6s}] {r.host}:{r.port} ({r.service})")
            if r.banner:
                for line in r.banner.split("\\n")[:3]:
                    report.append(f"          | {line}")
        return "\\n".join(report)


if __name__ == "__main__":
    scanner = NetworkScanner(timeout=0.5, max_threads=50)
    results = scanner.scan_host("192.168.1.1")
    print(scanner.generate_report())
`,
      },
      {
        name: 'exploit.py',
        type: 'file',
        language: 'python',
        content: `#!/usr/bin/env python3
"""
Kali Dragon - Exploit Framework Module
WARNING: For authorized penetration testing only
"""

import requests
import hashlib
from typing import Dict, Optional


class ExploitAgent:
    """Automated exploit agent for known CVEs."""

    def __init__(self, target: str, timeout: int = 10):
        self.target = target
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "KaliDragon/3.2.1"
        })

    def check_cve(self, cve_id: str) -> Dict:
        """Check if target is vulnerable to specific CVE."""
        # Placeholder for actual exploit logic
        return {
            "cve": cve_id,
            "target": self.target,
            "vulnerable": False,
            "details": "Check not implemented"
        }

    def run(self) -> Dict:
        """Run exploit chain against target."""
        return {"status": "initialized", "target": self.target}
`,
      },
      {
        name: 'report_gen.py',
        type: 'file',
        language: 'python',
        content: `#!/usr/bin/env python3
"""Kali Dragon - Report Generator"""
from datetime import datetime

def generate_report(data: dict) -> str:
    return f"Pentest Report - {datetime.now().isoformat()}\\n{data}"
`,
      },
    ],
  },
  {
    name: 'configs',
    type: 'folder',
    children: [
      {
        name: 'dragon.conf',
        type: 'file',
        language: 'ini',
        content: `[dragon]
version=3.2.1
cores=8
max_agents=10

[network]
proxy=socks5://127.0.0.1:9050
timeout=30

[security]
encryption=aes256
api_key=REDACTED
`,
      },
    ],
  },
  {
    name: 'README.md',
    type: 'file',
    language: 'markdown',
    content: `# Kali Dragon Control Center\n\nElite cybersecurity agent orchestration platform.\n\n## Features\n- Multi-agent orchestration\n- Real-time monitoring\n- Workflow automation\n- Neural processing engine`,
  },
];

const languageOptions = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'bash', label: 'Shell' },
  { value: 'ini', label: 'INI' },
  { value: 'markdown', label: 'Markdown' },
];

function FileTreeItem({
  item,
  depth,
  activeFile,
  onSelectFile,
}: {
  item: FileItem;
  depth: number;
  activeFile: string;
  onSelectFile: (item: FileItem) => void;
}) {
  const [expanded, setExpanded] = useState(depth === 0);

  return (
    <div>
      <button
        className={`w-full flex items-center gap-1.5 py-1 px-2 text-[11px] hover:bg-surface-2 transition-colors ${
          activeFile === item.name ? 'bg-surface-2 text-cyber-cyan' : 'text-muted-foreground'
        }`}
        style={{ paddingLeft: `${depth * 12 + 8}px` }}
        onClick={() => {
          if (item.type === 'folder') {
            setExpanded(!expanded);
          } else {
            onSelectFile(item);
          }
        }}
      >
        {item.type === 'folder' ? (
          <>
            {expanded ? <ChevronDown className="h-3 w-3 flex-shrink-0" /> : <ChevronRight className="h-3 w-3 flex-shrink-0" />}
            {expanded ? <FolderOpen className="h-3.5 w-3.5 text-cyan-400 flex-shrink-0" /> : <Folder className="h-3.5 w-3.5 text-amber-400 flex-shrink-0" />}
          </>
        ) : (
          <>
            <span className="w-3" />
            <File className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
          </>
        )}
        <span className="truncate">{item.name}</span>
      </button>
      {item.type === 'folder' && expanded && item.children?.map((child) => (
        <FileTreeItem
          key={child.name}
          item={child}
          depth={depth + 1}
          activeFile={activeFile}
          onSelectFile={onSelectFile}
        />
      ))}
    </div>
  );
}

export function CodeEditor() {
  const [activeFile, setActiveFile] = useState<FileItem>(fileTree[0].children![0]);
  const [openFiles, setOpenFiles] = useState<FileItem[]>([fileTree[0].children![0]]);
  const [language, setLanguage] = useState('python');
  const [showExplorer, setShowExplorer] = useState(true);
  const [cursorLine, setCursorLine] = useState(1);
  const [cursorCol, setCursorCol] = useState(1);

  const handleFileSelect = (item: FileItem) => {
    setActiveFile(item);
    setLanguage(item.language || 'plaintext');
    if (!openFiles.find((f) => f.name === item.name)) {
      setOpenFiles([...openFiles, item]);
    }
  };

  const closeFile = (name: string) => {
    const newFiles = openFiles.filter((f) => f.name !== name);
    setOpenFiles(newFiles);
    if (activeFile.name === name && newFiles.length > 0) {
      setActiveFile(newFiles[newFiles.length - 1]);
      setLanguage(newFiles[newFiles.length - 1].language || 'plaintext');
    }
  };

  return (
    <div className="h-full flex bg-surface-0">
      {/* File Explorer */}
      {showExplorer && (
        <div className="w-56 border-r border-border bg-surface-1 flex flex-col shrink-0">
          <div className="flex items-center justify-between px-3 py-2 border-b border-border">
            <span className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Explorer</span>
            <button onClick={() => setShowExplorer(false)} className="text-muted-foreground hover:text-foreground">
              <ChevronLeft className="h-3 w-3" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto py-1">
            {fileTree.map((item) => (
              <FileTreeItem
                key={item.name}
                item={item}
                depth={0}
                activeFile={activeFile.name}
                onSelectFile={handleFileSelect}
              />
            ))}
          </div>
        </div>
      )}

      {/* Editor Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Tab Bar */}
        <div className="flex items-center border-b border-border bg-surface-1 shrink-0 overflow-x-auto">
          {!showExplorer && (
            <button
              onClick={() => setShowExplorer(true)}
              className="flex items-center gap-1 px-2 py-1.5 border-r border-border hover:bg-surface-2 text-muted-foreground"
            >
              <ChevronRight className="h-3 w-3" />
            </button>
          )}
          {openFiles.map((file) => (
            <div
              key={file.name}
              className={`flex items-center gap-1.5 px-3 py-1.5 border-r border-border text-[11px] cursor-pointer group shrink-0 ${
                activeFile.name === file.name
                  ? 'bg-surface-0 text-foreground border-b-2 border-b-cyber-cyan'
                  : 'text-muted-foreground hover:text-foreground hover:bg-surface-2'
              }`}
              onClick={() => handleFileSelect(file)}
            >
              <File className="h-3 w-3" />
              <span>{file.name}</span>
              <button
                onClick={(e) => { e.stopPropagation(); closeFile(file.name); }}
                className="ml-1 opacity-0 group-hover:opacity-100 hover:text-cyber-red transition-all"
              >
                <X className="h-2.5 w-2.5" />
              </button>
            </div>
          ))}
        </div>

        {/* Language Selector */}
        <div className="flex items-center gap-2 px-3 py-1 border-b border-border bg-surface-1 shrink-0">
          <span className="text-[10px] text-muted-foreground">Language:</span>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-surface-2 border border-border rounded px-2 py-0.5 text-[10px] text-foreground focus:outline-none focus:border-cyber-cyan/50"
          >
            {languageOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          <div className="ml-auto flex items-center gap-2">
            <button className="flex items-center gap-1 px-2 py-0.5 rounded text-[10px] text-muted-foreground hover:text-cyber-cyan hover:bg-surface-2 transition-colors">
              <Save className="h-3 w-3" /> Save
            </button>
          </div>
        </div>

        {/* Monaco Editor */}
        <div className="flex-1">
          <MonacoEditor
            height="100%"
            language={language}
            theme="vs-dark"
            value={activeFile.content || ''}
            onChange={() => {}}
            options={{
              fontSize: 13,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              minimap: { enabled: true, scale: 1 },
              scrollBeyondLastLine: false,
              wordWrap: 'on',
              lineNumbers: 'on',
              renderLineHighlight: 'line',
              cursorBlinking: 'smooth',
              cursorSmoothCaretAnimation: 'on',
              smoothScrolling: true,
              padding: { top: 8 },
              background: '#0d1117',
              scrollbar: {
                verticalScrollbarSize: 6,
                horizontalScrollbarSize: 6,
              },
            }}
            onMount={(editor) => {
              editor.onDidChangeCursorPosition((e) => {
                setCursorLine(e.position.lineNumber);
                setCursorCol(e.position.column);
              });
            }}
          />
        </div>

        {/* Status Bar */}
        <div className="flex items-center gap-4 px-3 py-1 border-t border-border bg-surface-1 text-[10px] text-muted-foreground shrink-0">
          <span className="font-mono">Ln {cursorLine}, Col {cursorCol}</span>
          <span>UTF-8</span>
          <span className="capitalize">{language}</span>
          <div className="ml-auto flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span>Dragon Engine Ready</span>
          </div>
        </div>
      </div>
    </div>
  );
}
