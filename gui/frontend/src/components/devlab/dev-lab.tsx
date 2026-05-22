'use client';

import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { useToast } from '@/hooks/use-toast';
import type { ChatMessage, ChatSession, ProjectFile, DevLabProject } from '@/types';
import { useProvidersStore } from '@/stores/providers-store';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Separator } from '@/components/ui/separator';
import { Switch } from '@/components/ui/switch';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

import {
  Send,
  Paperclip,
  Bot,
  RotateCcw,
  Copy,
  Check,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Plus,
  Trash2,
  Search,
  ExternalLink,
  RefreshCw,
  File,
  Folder,
  FolderOpen,
  Code2,
  Terminal,
  Globe,
  Shield,
  Database,
  Sparkles,
  X,
  MoreVertical,
  Eye,
  FolderTree,
  FileText,
  MessageSquare,
  FolderKanban,
  Settings,
  Flame,
  Clock,
} from 'lucide-react';

/* ═══════════════════════════════════════════════════════════════
   MOCK DATA
   ═══════════════════════════════════════════════════════════════ */

const WELCOME_MESSAGE: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content: `Hey! I'm **DragonDev**, your AI development agent.

I can help you build anything: web apps, scripts, security tools, games, AI agents, system utilities...

What do you want to create today?`,
  timestamp: new Date().toISOString(),
};

const MOCK_FILE_TREE: ProjectFile = {
  name: 'my-project',
  type: 'folder',
  children: [
    {
      name: 'src',
      type: 'folder',
      children: [
        { name: 'index.ts', type: 'file', language: 'typescript', content: `import express from 'express';\nimport { config } from './config';\nimport { createServer } from './server';\n\nconst app = express();\nconst PORT = config.port || 3000;\n\napp.get('/', (req, res) => {\n  res.json({ status: 'ok', uptime: process.uptime() });\n});\n\napp.listen(PORT, () => {\n  console.log(\`Server running on port \${PORT}\`);\n});` },
        { name: 'app.ts', type: 'file', language: 'typescript', content: `import { Application } from 'express';\nimport { setupMiddleware } from './middleware';\nimport { setupRoutes } from './routes';\n\nexport function createApp(): Application {\n  const app: Application = express();\n  setupMiddleware(app);\n  setupRoutes(app);\n  return app;\n}` },
        { name: 'utils.ts', type: 'file', language: 'typescript', content: `export function generateId(): string {\n  return crypto.randomUUID();\n}\n\nexport function sanitize(str: string): string {\n  return str.replace(/<[^>]*>/g, '');\n}\n\nexport async function retry<T>(\n  fn: () => Promise<T>,\n  retries = 3\n): Promise<T> {\n  for (let i = 0; i < retries; i++) {\n    try { return await fn(); }\n    catch (e) { if (i === retries - 1) throw e; }\n  }\n  throw new Error('Max retries exceeded');\n}` },
        {
          name: 'components',
          type: 'folder',
          children: [
            { name: 'Header.tsx', type: 'file', language: 'typescript', content: `import React from 'react';\n\nexport function Header({ title }: { title: string }) {\n  return (\n    <header className="flex items-center px-6 py-4 border-b">\n      <h1 className="text-2xl font-bold">{title}</h1>\n    </header>\n  );\n}` },
            { name: 'Footer.tsx', type: 'file', language: 'typescript', content: `import React from 'react';\n\nexport function Footer() {\n  return (\n    <footer className="px-6 py-4 border-t text-sm text-muted">\n      © 2025 DragonDev Lab\n    </footer>\n  );\n}` },
            { name: 'Button.tsx', type: 'file', language: 'typescript', content: `import React from 'react';\n\ninterface ButtonProps {\n  variant?: 'primary' | 'secondary' | 'danger';\n  children: React.ReactNode;\n  onClick?: () => void;\n}\n\nexport function Button({ variant = 'primary', children, onClick }: ButtonProps) {\n  const styles = {\n    primary: 'bg-cyan-500 text-black hover:bg-cyan-400',\n    secondary: 'bg-gray-700 text-white hover:bg-gray-600',\n    danger: 'bg-red-500 text-white hover:bg-red-400',\n  };\n  return (\n    <button\n      className={\`px-4 py-2 rounded font-medium \${styles[variant]}\`}\n      onClick={onClick}\n    >\n      {children}\n    </button>\n  );\n}` },
          ],
        },
      ],
    },
    {
      name: 'public',
      type: 'folder',
      children: [
        { name: 'index.html', type: 'file', language: 'html', content: `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width">\n  <title>My Project</title>\n</head>\n<body>\n  <div id="root"></div>\n</body>\n</html>` },
      ],
    },
    { name: 'package.json', type: 'file', language: 'json', content: `{\n  "name": "my-project",\n  "version": "1.0.0",\n  "type": "module",\n  "scripts": {\n    "dev": "tsx watch src/index.ts",\n    "build": "tsc && node dist/index.js"\n  },\n  "dependencies": {\n    "express": "^4.18.0"\n  }\n}` },
    { name: 'tsconfig.json', type: 'file', language: 'json', content: `{\n  "compilerOptions": {\n    "target": "ES2022",\n    "module": "ESNext",\n    "moduleResolution": "bundler",\n    "strict": true,\n    "outDir": "./dist"\n  }\n}` },
    { name: 'README.md', type: 'file', language: 'markdown', content: `# My Project\n\nA production-ready TypeScript application.\n\n## Getting Started\n\n\`\`\`bash\nnpm install\nnpm run dev\n\`\`\`\n\n## Features\n\n- Express server\n- TypeScript strict mode\n- Hot reload` },
    { name: '.env', type: 'file', language: 'bash', content: `PORT=3000\nNODE_ENV=development\nDATABASE_URL=sqlite://./db.sqlite` },
  ],
};

const MOCK_SESSIONS: ChatSession[] = [
  { id: 's1', title: 'Build a port scanner', lastMessage: 'Created scanner.py with async scanning capabilities...', timestamp: '2h ago', messageCount: 12 },
  { id: 's2', title: 'React dashboard', lastMessage: "Here's the complete dashboard with charts...", timestamp: '1d ago', messageCount: 24 },
  { id: 's3', title: 'Python keylogger', lastMessage: "I can't help with that request.", timestamp: '2d ago', messageCount: 3 },
  { id: 's4', title: 'Discord bot', lastMessage: 'The bot is ready with commands and events...', timestamp: '3d ago', messageCount: 18 },
  { id: 's5', title: 'Docker setup', lastMessage: "Here's the Dockerfile and compose config...", timestamp: '5d ago', messageCount: 8 },
];

const MOCK_PROJECTS: DevLabProject[] = [
  { id: 'p1', name: 'Pentest Toolkit', description: 'Comprehensive penetration testing toolkit with scanner, exploiter, and reporter modules', language: 'Python', lastModified: '2h ago', fileCount: 15 },
  { id: 'p2', name: 'Web Dashboard', description: 'Real-time analytics dashboard with interactive charts and data visualization', language: 'TypeScript/React', lastModified: '1d ago', fileCount: 23 },
  { id: 'p3', name: 'Security Scanner', description: 'High-performance vulnerability scanner with concurrent scanning engine', language: 'Go', lastModified: '3d ago', fileCount: 8 },
  { id: 'p4', name: 'AI Agent Framework', description: 'Modular AI agent framework with plugin system and tool integration', language: 'Python', lastModified: '5d ago', fileCount: 31 },
];

const MOCK_DOCS = [
  {
    id: 'd1',
    title: 'API Reference',
    icon: Code2,
    date: '2h ago',
    snippet: 'RESTful API endpoints for agent control, task management, and system monitoring...',
    content: `# API Reference

## Authentication
All API requests require a Bearer token in the Authorization header.

\`\`\`
Authorization: Bearer <your-token>
\`\`\`

## Endpoints

### POST /api/agents
Create a new agent instance.
\`\`\`json
{
  "name": "Scanner Agent",
  "type": "scanner",
  "config": { "target": "10.0.0.0/24" }
}
\`\`\`

### GET /api/agents
List all active agents with status and metrics.

### POST /api/tasks
Submit a new task to the task queue.

### GET /api/system/metrics
Retrieve real-time system metrics (CPU, memory, network).

## Rate Limits
- 100 requests/minute for standard tier
- 1000 requests/minute for premium tier`,
  },
  {
    id: 'd2',
    title: 'Architecture Guide',
    icon: Database,
    date: '1d ago',
    snippet: 'System architecture overview including microservices, message bus, and data flow...',
    content: `# Architecture Guide

## Overview
The DragonDev platform uses a microservices architecture with the following components:

## Core Services
- **Agent Manager** — Manages agent lifecycle and scheduling
- **Task Queue** — Redis-backed job queue with priority support
- **API Gateway** — Rate-limited REST API with JWT auth
- **WebSocket Server** — Real-time agent communication
- **Storage Layer** — SQLite for config, file system for artifacts

## Data Flow
1. User submits task via API
2. Task enters priority queue
3. Agent Manager assigns task to available agent
4. Agent executes and streams results via WebSocket
5. Results persisted to storage

## Scaling
- Horizontal scaling via agent instances
- Connection pooling for database access
- In-memory caching for hot paths`,
  },
  {
    id: 'd3',
    title: 'Security Protocols',
    icon: Shield,
    date: '3d ago',
    snippet: 'Security measures, access controls, encryption standards, and audit logging...',
    content: `# Security Protocols

## Access Control
- Role-based access control (RBAC) with admin, operator, viewer roles
- API tokens with configurable expiry
- IP allowlisting for API endpoints

## Encryption
- AES-256-GCM for data at rest
- TLS 1.3 for all network communication
- Encrypted environment variables

## Audit Logging
- All API requests logged with timestamps
- Agent actions recorded with full context
- Log retention: 90 days

## Sandboxing
- Agents execute in isolated containers
- Network access restricted to configured targets
- File system access limited to workspace directory`,
  },
  {
    id: 'd4',
    title: 'Deployment Guide',
    icon: Globe,
    date: '5d ago',
    snippet: 'Step-by-step deployment instructions for Docker, Kubernetes, and bare metal...',
    content: `# Deployment Guide

## Docker Deployment
\`\`\`bash
# Clone the repository
git clone https://github.com/dragondev/platform.git
cd platform

# Build the image
docker build -t dragondev .

# Run the container
docker run -d -p 3000:3000 -v ./data:/app/data dragondev
\`\`\`

## Environment Variables
\`\`\`
PORT=3000
DATABASE_URL=sqlite://./data/db.sqlite
JWT_SECRET=<your-secret>
LOG_LEVEL=info
\`\`\`

## Health Check
\`\`\`
GET /api/health
\`\`\`
Returns: \`{ "status": "ok", "version": "3.2.1" }\`

## Backup
- Database: \`sqlite3 data/db.sqlite ".backup backup.db"\`
- Config: Copy \`.env\` and \`config/\` directory`,
  },
];

const FILE_ICONS: Record<string, { icon: typeof File; color: string }> = {
  typescript: { icon: Code2, color: 'text-blue-400' },
  javascript: { icon: Code2, color: 'text-yellow-400' },
  python: { icon: Terminal, color: 'text-green-400' },
  json: { icon: File, color: 'text-yellow-300' },
  html: { icon: Globe, color: 'text-orange-400' },
  css: { icon: Globe, color: 'text-purple-400' },
  markdown: { icon: FileText, color: 'text-gray-300' },
  bash: { icon: Terminal, color: 'text-emerald-400' },
  go: { icon: Code2, color: 'text-cyan-300' },
  rust: { icon: Code2, color: 'text-orange-500' },
};

function getFileIcon(name: string): { icon: typeof File; color: string } {
  const ext = name.split('.').pop()?.toLowerCase() || '';
  const langMap: Record<string, string> = {
    ts: 'typescript', tsx: 'typescript', js: 'javascript', jsx: 'javascript',
    py: 'python', json: 'json', html: 'html', css: 'css', md: 'markdown',
    sh: 'bash', env: 'bash', go: 'go', rs: 'rust',
  };
  return FILE_ICONS[langMap[ext] || ''] || { icon: File, color: 'text-muted-foreground' };
}

function findFileInTree(node: ProjectFile, path: string[]): ProjectFile | null {
  if (path.length === 0) return node;
  if (node.type === 'folder' && node.children) {
    const next = node.children.find((c) => c.name === path[0]);
    return next ? findFileInTree(next, path.slice(1)) : null;
  }
  return null;
}

/* ═══════════════════════════════════════════════════════════════
   CODE BLOCK COMPONENT
   ═══════════════════════════════════════════════════════════════ */

function CodeBlock({ code, language }: { code: string; language: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      /* ignore clipboard errors */
    }
  }, [code]);

  return (
    <div className="my-3 rounded-lg border border-border overflow-hidden group">
      <div className="flex items-center justify-between px-4 py-2 bg-surface-2 border-b border-border">
        <span className="text-xs font-mono text-muted-foreground">{language || 'code'}</span>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 px-2 text-xs text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity"
          onClick={handleCopy}
        >
          {copied ? <Check className="h-3 w-3 text-emerald-400 mr-1" /> : <Copy className="h-3 w-3 mr-1" />}
          {copied ? 'Copied' : 'Copy'}
        </Button>
      </div>
      <div className="p-4 bg-surface-0 overflow-x-auto">
        <pre className="text-sm font-mono text-foreground leading-relaxed">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════
   MARKDOWN RENDERER
   ═══════════════════════════════════════════════════════════════ */

function MarkdownContent({ content }: { content: string }) {
  const parts = useMemo(() => {
    const result: React.ReactNode[] = [];
    const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
    let lastIndex = 0;
    let match: RegExpExecArray | null;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      if (match.index > lastIndex) {
        const text = content.slice(lastIndex, match.index);
        result.push(<InlineMarkdown key={`text-${lastIndex}`} text={text} />);
      }
      result.push(
        <CodeBlock key={`code-${match.index}`} code={match[2].trim()} language={match[1]} />
      );
      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
      result.push(<InlineMarkdown key={`text-${lastIndex}`} text={content.slice(lastIndex)} />);
    }

    return result;
  }, [content]);

  return <div className="space-y-1">{parts}</div>;
}

function InlineMarkdown({ text }: { text: string }) {
  const lines = text.split('\n');
  const elements: React.ReactNode[] = [];
  let keyIdx = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Headers
    const headerMatch = line.match(/^(#{1,3})\s+(.+)/);
    if (headerMatch) {
      const level = headerMatch[1].length;
      const Tag = `h${Math.min(level + 1, 4)}` as keyof JSX.IntrinsicElements;
      elements.push(
        React.createElement(
          Tag,
          { key: `h-${keyIdx++}`, className: 'font-semibold mt-2 mb-1 text-foreground' },
          <InlineText text={headerMatch[2]} />
        )
      );
      continue;
    }

    // List items
    const listMatch = line.match(/^[-*]\s+(.+)/);
    if (listMatch) {
      elements.push(
        <li key={`li-${keyIdx++}`} className="ml-4 list-disc text-foreground/90">
          <InlineText text={listMatch[1]} />
        </li>
      );
      continue;
    }

    // Blockquote
    const quoteMatch = line.match(/^>\s*(.+)/);
    if (quoteMatch) {
      elements.push(
        <blockquote key={`bq-${keyIdx++}`} className="border-l-2 border-cyber-cyan/30 pl-3 my-1 text-muted-foreground italic">
          <InlineText text={quoteMatch[1]} />
        </blockquote>
      );
      continue;
    }

    // Empty line
    if (line.trim() === '') {
      elements.push(<div key={`br-${keyIdx++}`} className="h-2" />);
      continue;
    }

    // Regular paragraph
    elements.push(
      <p key={`p-${keyIdx++}`} className="text-foreground/90 leading-relaxed">
        <InlineText text={line} />
      </p>
    );
  }

  return <>{elements}</>;
}

function InlineText({ text }: { text: string }) {
  const parts: React.ReactNode[] = [];
  // Pattern: bold, italic, inline code
  const regex = /(\*\*(.+?)\*\*)|(`([^`]+)`)|(\*(.+?)\*)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(<span key={`t-${lastIndex}`}>{text.slice(lastIndex, match.index)}</span>);
    }
    if (match[2]) {
      parts.push(<strong key={`b-${match.index}`} className="font-semibold text-foreground">{match[2]}</strong>);
    } else if (match[4]) {
      parts.push(
        <code key={`c-${match.index}`} className="px-1.5 py-0.5 rounded bg-surface-2 text-cyber-cyan text-xs font-mono">
          {match[4]}
        </code>
      );
    } else if (match[6]) {
      parts.push(<em key={`i-${match.index}`} className="italic">{match[6]}</em>);
    }
    lastIndex = match.index + match[0].length;
  }

  if (lastIndex < text.length) {
    parts.push(<span key={`t-${lastIndex}`}>{text.slice(lastIndex)}</span>);
  }

  return <>{parts}</>;
}

/* ═══════════════════════════════════════════════════════════════
   FILE TREE ITEM
   ═══════════════════════════════════════════════════════════════ */

function FileTreeItem({
  node,
  path,
  depth,
  expandedFolders,
  toggleFolder,
  selectedFile,
  onSelectFile,
}: {
  node: ProjectFile;
  path: string[];
  depth: number;
  expandedFolders: Set<string>;
  toggleFolder: (path: string) => void;
  selectedFile: string | null;
  onSelectFile: (path: string, file: ProjectFile) => void;
}) {
  const fullPath = path.join('/');
  const isFolder = node.type === 'folder';
  const isExpanded = expandedFolders.has(fullPath);
  const isSelected = selectedFile === fullPath;
  const fileIconInfo = getFileIcon(node.name);
  const FileIcon = fileIconInfo.icon;

  return (
    <div>
      <button
        className={`w-full flex items-center gap-1.5 px-2 py-1 text-sm rounded transition-colors group ${
          isSelected
            ? 'bg-cyber-cyan/10 text-cyber-cyan'
            : 'text-foreground/80 hover:bg-surface-2 hover:text-foreground'
        }`}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
        onClick={() => {
          if (isFolder) toggleFolder(fullPath);
          else onSelectFile(fullPath, node);
        }}
      >
        {isFolder ? (
          <>
            {isExpanded ? (
              <ChevronDown className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            ) : (
              <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            )}
            {isExpanded ? (
              <FolderOpen className="h-4 w-4 text-cyber-cyan shrink-0" />
            ) : (
              <Folder className="h-4 w-4 text-cyber-cyan/70 shrink-0" />
            )}
          </>
        ) : (
          <>
            <span className="w-3.5 shrink-0" />
            <FileIcon className={`h-4 w-4 shrink-0 ${fileIconInfo.color}`} />
          </>
        )}
        <span className="truncate text-left">{node.name}</span>
      </button>
      {isFolder && isExpanded && node.children && (
        <div>
          {[...node.children]
            .sort((a, b) => {
              if (a.type !== b.type) return a.type === 'folder' ? -1 : 1;
              return a.name.localeCompare(b.name);
            })
            .map((child) => (
              <FileTreeItem
                key={child.name}
                node={child}
                path={[...path, child.name]}
                depth={depth + 1}
                expandedFolders={expandedFolders}
                toggleFolder={toggleFolder}
                selectedFile={selectedFile}
                onSelectFile={onSelectFile}
              />
            ))}
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════
   LOADING INDICATOR
   ═══════════════════════════════════════════════════════════════ */

function LoadingDots() {
  return (
    <div className="flex items-center gap-1 py-2 px-1">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="w-2 h-2 rounded-full bg-cyber-cyan/60 animate-bounce"
          style={{ animationDelay: `${i * 150}ms`, animationDuration: '600ms' }}
        />
      ))}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════
   MAIN DEV LAB COMPONENT
   ═══════════════════════════════════════════════════════════════ */

export function DevLab() {
  const { toast } = useToast();

  /* ── Panel state ── */
  const [leftOpen, setLeftOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(true);
  const [leftTab, setLeftTab] = useState<'preview' | 'files' | 'docs'>('files');
  const [rightTab, setRightTab] = useState<'history' | 'projects' | 'config'>('history');

  /* ── Chat state ── */
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /* ── Files state ── */
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [selectedFileContent, setSelectedFileContent] = useState<string | null>(null);
  const [selectedFileLanguage, setSelectedFileLanguage] = useState<string | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(['src', 'src/components']));

  /* ── Docs state ── */
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null);

  /* ── History state ── */
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);

  /* ── Config state ── */
  const [model, setModel] = useState('claude-sonnet-4');
  const [temperature, setTemperature] = useState(0.7);
  const [systemPrompt, setSystemPrompt] = useState(
    'You are DragonDev, an elite AI development agent integrated into Kali Linux. You are a master software engineer capable of creating ANY type of software, system, game, script, tool, interface, antivirus, AI agent, or any other project the user needs.'
  );
  const [autoSave, setAutoSave] = useState(true);
  const [contextWindow, setContextWindow] = useState(50);
  const [codeTheme, setCodeTheme] = useState('dark');
  const [verboseOutput, setVerboseOutput] = useState(true);
  const [lineNumbers, setLineNumbers] = useState(true);
  const [autoExecute, setAutoExecute] = useState(false);

  /* ── Auto-scroll ── */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  /* ── Filter sessions ── */
  const filteredSessions = useMemo(
    () =>
      searchQuery
        ? MOCK_SESSIONS.filter(
            (s) =>
              s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
              s.lastMessage.toLowerCase().includes(searchQuery.toLowerCase())
          )
        : MOCK_SESSIONS,
    [searchQuery]
  );

  /* ── Folder toggle ── */
  const toggleFolder = useCallback((path: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  }, []);

  /* ── File select ── */
  const handleSelectFile = useCallback((path: string, file: ProjectFile) => {
    setSelectedFile(path);
    setSelectedFileContent(file.content || null);
    setSelectedFileLanguage(file.language || null);
  }, []);

  /* ── Send message ── */
  const sendMessage = useCallback(async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: trimmed,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    try {
      const allMessages = [...messages, userMessage]
        .filter((m) => m.role !== 'system')
        .map((m) => ({ role: m.role, content: m.content }));

      // Obtener config del proveedor activo
      const { connectionMode, activeLlmProvider, providers } = useProvidersStore.getState();
      const activeProvider = providers.find((p) => p.id === activeLlmProvider);

      const providerPayload = connectionMode === 'cloud' && activeProvider?.enabled && activeProvider.apiKey
        ? {
            id: activeProvider.id,
            name: activeProvider.name,
            apiKey: activeProvider.apiKey,
            baseUrl: activeProvider.baseUrl,
            model: activeProvider.model,
            connectionMode,
          }
        : { connectionMode: 'local' };

      const res = await fetch('/api/devlab/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: allMessages, provider: providerPayload }),
      });

      const data = await res.json();

      const assistantMessage: ChatMessage = {
        id: `msg-${Date.now()}-resp`,
        role: 'assistant',
        content: data.content || 'No response generated.',
        timestamp: data.timestamp || new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      const errorMessage: ChatMessage = {
        id: `msg-${Date.now()}-err`,
        role: 'assistant',
        content: 'Error de conexion con el endpoint local. Verifica que el servidor esta ejecutandose.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, messages]);

  /* ── Keyboard handler ── */
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    },
    [sendMessage]
  );

  /* ── Auto-resize textarea ── */
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    const el = e.target;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 144) + 'px'; // max ~6 lines
  }, []);

  /* ── Clear chat ── */
  const clearChat = useCallback(() => {
    setMessages([WELCOME_MESSAGE]);
    toast({ title: 'Chat cleared', description: 'Conversation has been reset.' });
  }, [toast]);

  /* ── Format timestamp ── */
  const formatTime = useCallback((ts: string) => {
    try {
      return new Date(ts).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    } catch {
      return '';
    }
  }, []);

  /* ── Selected doc ── */
  const selectedDoc = useMemo(() => MOCK_DOCS.find((d) => d.id === selectedDocId), [selectedDocId]);

  /* ═══════════════════════════════════════════════════════════
     RENDER
     ═══════════════════════════════════════════════════════════ */
  return (
    <TooltipProvider delayDuration={300}>
      <div className="h-full w-full flex bg-surface-0 relative overflow-hidden">
        {/* ─── LEFT PANEL ─── */}
        <div
          className={`shrink-0 border-r border-border bg-surface-1 flex flex-col transition-all duration-300 overflow-hidden ${
            leftOpen ? 'w-[300px]' : 'w-0'
          }`}
        >
          {/* Left Panel Tabs */}
          <div className="flex items-center border-b border-border px-1 shrink-0">
            {(['preview', 'files', 'docs'] as const).map((tab) => {
              const icons = { preview: Eye, files: FolderTree, docs: FileText };
              const labels = { preview: 'Preview', files: 'Files', docs: 'Docs' };
              const Icon = icons[tab];
              return (
                <button
                  key={tab}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 text-xs font-medium transition-colors ${
                    leftTab === tab
                      ? 'text-cyber-cyan border-b-2 border-cyber-cyan'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                  onClick={() => setLeftTab(tab)}
                >
                  <Icon className="h-3.5 w-3.5" />
                  <span className="hidden xl:inline">{labels[tab]}</span>
                </button>
              );
            })}
          </div>

          {/* Left Panel Content */}
          <div className="flex-1 overflow-hidden flex flex-col">
            {/* PREVIEW TAB */}
            {leftTab === 'preview' && (
              <div className="flex flex-col h-full">
                {/* URL bar */}
                <div className="flex items-center gap-2 px-3 py-2 border-b border-border shrink-0">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="ghost" size="sm" className="h-6 w-6 p-0 text-muted-foreground hover:text-foreground">
                        <RefreshCw className="h-3.5 w-3.5" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Refresh</TooltipContent>
                  </Tooltip>
                  <div className="flex-1 flex items-center gap-2 px-3 py-1 rounded-md bg-surface-2 border border-border text-xs font-mono text-muted-foreground">
                    <Globe className="h-3 w-3 text-cyber-cyan/60" />
                    <span>localhost:3000</span>
                  </div>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="ghost" size="sm" className="h-6 w-6 p-0 text-muted-foreground hover:text-foreground">
                        <ExternalLink className="h-3.5 w-3.5" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Open in new tab</TooltipContent>
                  </Tooltip>
                </div>
                {/* Preview area */}
                <div className="flex-1 flex items-center justify-center p-4">
                  <div className="text-center space-y-3">
                    <div className="w-16 h-16 rounded-xl bg-surface-2 border border-border flex items-center justify-center mx-auto">
                      <Globe className="h-8 w-8 text-muted-foreground/40" />
                    </div>
                    <p className="text-sm text-muted-foreground">Live preview will appear here</p>
                    <p className="text-xs text-muted-foreground/60">when you deploy a project</p>
                  </div>
                </div>
              </div>
            )}

            {/* FILES TAB */}
            {leftTab === 'files' && (
              <div className="flex flex-col h-full">
                {/* Toolbar */}
                <div className="flex items-center gap-2 px-3 py-2 border-b border-border shrink-0">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 w-6 p-0 text-muted-foreground hover:text-cyber-cyan"
                        onClick={() => toast({ title: 'New File', description: 'File creation dialog coming soon.' })}
                      >
                        <Plus className="h-3.5 w-3.5" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>New File</TooltipContent>
                  </Tooltip>
                  <span className="text-xs font-mono text-muted-foreground truncate">
                    {MOCK_FILE_TREE.name}/
                  </span>
                </div>

                {/* File tree + content split */}
                <div className="flex-1 flex flex-col overflow-hidden">
                  {/* File tree */}
                  <div className="flex-1 overflow-y-auto py-1 min-h-0">
                    <FileTreeItem
                      node={MOCK_FILE_TREE}
                      path={[MOCK_FILE_TREE.name]}
                      depth={0}
                      expandedFolders={expandedFolders}
                      toggleFolder={toggleFolder}
                      selectedFile={selectedFile}
                      onSelectFile={handleSelectFile}
                    />
                  </div>

                  {/* File content preview */}
                  {selectedFileContent !== null && (
                    <div className="border-t border-border shrink-0 max-h-[50%] flex flex-col">
                      <div className="flex items-center gap-2 px-3 py-1.5 bg-surface-2 border-b border-border">
                        <File className="h-3 w-3 text-muted-foreground" />
                        <span className="text-xs font-mono text-muted-foreground truncate">{selectedFile}</span>
                        <div className="ml-auto">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-5 w-5 p-0 text-muted-foreground hover:text-foreground"
                            onClick={() => {
                              setSelectedFile(null);
                              setSelectedFileContent(null);
                              setSelectedFileLanguage(null);
                            }}
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                      <ScrollArea className="flex-1">
                        <pre className="p-3 text-xs font-mono text-foreground/80 leading-relaxed whitespace-pre-wrap">
                          {selectedFileContent}
                        </pre>
                      </ScrollArea>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* DOCS TAB */}
            {leftTab === 'docs' && (
              <div className="flex flex-col h-full">
                {/* Toolbar */}
                <div className="flex items-center gap-2 px-3 py-2 border-b border-border shrink-0">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 w-6 p-0 text-muted-foreground hover:text-cyber-cyan"
                        onClick={() => toast({ title: 'New Document', description: 'Document creation coming soon.' })}
                      >
                        <Plus className="h-3.5 w-3.5" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>New Document</TooltipContent>
                  </Tooltip>
                </div>

                <div className="flex-1 overflow-y-auto">
                  {!selectedDocId ? (
                    /* Doc list */
                    <div className="p-2 space-y-1">
                      {MOCK_DOCS.map((doc) => {
                        const DocIcon = doc.icon;
                        return (
                          <button
                            key={doc.id}
                            className="w-full text-left px-3 py-2.5 rounded-lg hover:bg-surface-2 transition-colors group"
                            onClick={() => setSelectedDocId(doc.id)}
                          >
                            <div className="flex items-start gap-2.5">
                              <DocIcon className="h-4 w-4 text-cyber-cyan/70 mt-0.5 shrink-0" />
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-foreground group-hover:text-cyber-cyan transition-colors truncate">
                                  {doc.title}
                                </p>
                                <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{doc.snippet}</p>
                                <div className="flex items-center gap-1 mt-1 text-[10px] text-muted-foreground/60">
                                  <Clock className="h-2.5 w-2.5" />
                                  {doc.date}
                                </div>
                              </div>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  ) : (
                    /* Doc content */
                    <div className="h-full flex flex-col">
                      <div className="flex items-center gap-2 px-3 py-2 border-b border-border shrink-0">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 w-6 p-0 text-muted-foreground hover:text-foreground"
                          onClick={() => setSelectedDocId(null)}
                        >
                          <ChevronLeft className="h-3.5 w-3.5" />
                        </Button>
                        <span className="text-xs font-medium text-foreground truncate">{selectedDoc?.title}</span>
                      </div>
                      <ScrollArea className="flex-1 p-4">
                        {selectedDoc && <MarkdownContent content={selectedDoc.content} />}
                      </ScrollArea>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Left panel toggle */}
        {!leftOpen && (
          <Tooltip>
            <TooltipTrigger asChild>
              <button
                className="absolute left-0 top-1/2 -translate-y-1/2 z-10 w-6 h-16 flex items-center justify-center bg-surface-1 border border-border border-l-0 rounded-r-md text-muted-foreground hover:text-cyber-cyan transition-colors"
                onClick={() => setLeftOpen(true)}
              >
                <ChevronRight className="h-3.5 w-3.5" />
              </button>
            </TooltipTrigger>
            <TooltipContent side="right">Open files panel</TooltipContent>
          </Tooltip>
        )}

        {/* ─── CENTER PANEL — CHAT ─── */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Chat Header */}
          <div className="flex items-center gap-3 px-4 py-3 border-b border-border bg-surface-1 shrink-0">
            {/* Agent avatar */}
            <div className="w-8 h-8 rounded-full bg-cyber-cyan/10 border border-cyber-cyan/30 flex items-center justify-center shrink-0">
              <Flame className="h-4 w-4 text-cyber-cyan" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <h2 className="text-sm font-semibold text-foreground">DragonDev Agent</h2>
                <Badge
                  variant="outline"
                  className="h-5 text-[10px] font-normal px-1.5 border-emerald-500/30 text-emerald-400"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1 animate-status-pulse" />
                  Online — Ready to build
                </Badge>
              </div>
              <p className="text-[11px] text-muted-foreground font-mono">Claude Sonnet 4</p>
            </div>

            {/* Clear chat */}
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 p-0 text-muted-foreground hover:text-destructive"
                  onClick={clearChat}
                >
                  <RotateCcw className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Clear chat</TooltipContent>
            </Tooltip>

            {/* Panel toggles */}
            <Separator orientation="vertical" className="h-5" />
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className={`h-8 w-8 p-0 ${leftOpen ? 'text-cyber-cyan' : 'text-muted-foreground'}`}
                  onClick={() => setLeftOpen(!leftOpen)}
                >
                  <ChevronLeft className={`h-4 w-4 transition-transform ${leftOpen ? '' : 'rotate-180'}`} />
                </Button>
              </TooltipTrigger>
              <TooltipContent>{leftOpen ? 'Hide files panel' : 'Show files panel'}</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className={`h-8 w-8 p-0 ${rightOpen ? 'text-cyber-cyan' : 'text-muted-foreground'}`}
                  onClick={() => setRightOpen(!rightOpen)}
                >
                  <ChevronRight className={`h-4 w-4 transition-transform ${rightOpen ? '' : '-rotate-180'}`} />
                </Button>
              </TooltipTrigger>
              <TooltipContent>{rightOpen ? 'Hide history panel' : 'Show history panel'}</TooltipContent>
            </Tooltip>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-4">
            <div className="max-w-3xl mx-auto space-y-4">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-xl px-4 py-3 ${
                      msg.role === 'user'
                        ? 'bg-surface-2 border border-border'
                        : 'bg-surface-1 border border-border border-l-2 border-l-cyber-cyan/40'
                    }`}
                  >
                    {/* Agent header */}
                    {msg.role === 'assistant' && (
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-5 h-5 rounded-full bg-cyber-cyan/10 flex items-center justify-center">
                          <Bot className="h-3 w-3 text-cyber-cyan" />
                        </div>
                        <span className="text-xs font-medium text-cyber-cyan">DragonDev</span>
                        <span className="text-[10px] text-muted-foreground ml-auto">{formatTime(msg.timestamp)}</span>
                      </div>
                    )}

                    {/* Message content */}
                    {msg.role === 'assistant' ? (
                      <div className="text-sm">
                        <MarkdownContent content={msg.content} />
                      </div>
                    ) : (
                      <div className="text-sm text-foreground/90 whitespace-pre-wrap">{msg.content}</div>
                    )}

                    {/* User timestamp */}
                    {msg.role === 'user' && (
                      <div className="flex justify-end mt-1">
                        <span className="text-[10px] text-muted-foreground">{formatTime(msg.timestamp)}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Loading indicator */}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-surface-1 border border-border border-l-2 border-l-cyber-cyan/40 rounded-xl px-4 py-3">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-5 h-5 rounded-full bg-cyber-cyan/10 flex items-center justify-center">
                        <Bot className="h-3 w-3 text-cyber-cyan" />
                      </div>
                      <span className="text-xs font-medium text-cyber-cyan">DragonDev</span>
                    </div>
                    <LoadingDots />
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input Area */}
          <div className="shrink-0 border-t border-border bg-surface-1 px-4 py-3">
            <div className="max-w-3xl mx-auto">
              <div className="flex items-end gap-2">
                {/* Attachment button */}
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-9 w-9 p-0 text-muted-foreground hover:text-foreground shrink-0"
                      onClick={() => toast({ title: 'Attach File', description: 'Drag files or click to attach (coming soon).' })}
                    >
                      <Paperclip className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Attach file</TooltipContent>
                </Tooltip>

                {/* Textarea */}
                <div className="flex-1 relative">
                  <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Describe what you want to build..."
                    rows={1}
                    className="w-full resize-none rounded-xl border border-border bg-surface-2 px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-cyber-cyan/30 focus:border-cyber-cyan/50 transition-all glow-cyan"
                    style={{ minHeight: '38px', maxHeight: '144px' }}
                  />
                </div>

                {/* Send button */}
                <Button
                  size="sm"
                  className="h-9 w-9 p-0 bg-cyber-cyan/20 text-cyber-cyan hover:bg-cyber-cyan/30 border border-cyber-cyan/30 shrink-0 disabled:opacity-30 disabled:cursor-not-allowed"
                  onClick={sendMessage}
                  disabled={!input.trim() || loading}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-[10px] text-muted-foreground/50 mt-1.5 text-center">
                Enter to send · Shift+Enter for new line
              </p>
            </div>
          </div>
        </div>

        {/* ─── RIGHT PANEL ─── */}
        <div
          className={`shrink-0 border-l border-border bg-surface-1 flex flex-col transition-all duration-300 overflow-hidden ${
            rightOpen ? 'w-[300px]' : 'w-0'
          }`}
        >
          {/* Right Panel Tabs */}
          <div className="flex items-center border-b border-border px-1 shrink-0">
            {(['history', 'projects', 'config'] as const).map((tab) => {
              const icons = { history: MessageSquare, projects: FolderKanban, config: Settings };
              const labels = { history: 'History', projects: 'Projects', config: 'Config' };
              const Icon = icons[tab];
              return (
                <button
                  key={tab}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 text-xs font-medium transition-colors ${
                    rightTab === tab
                      ? 'text-cyber-cyan border-b-2 border-cyber-cyan'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                  onClick={() => setRightTab(tab)}
                >
                  <Icon className="h-3.5 w-3.5" />
                  <span className="hidden xl:inline">{labels[tab]}</span>
                </button>
              );
            })}
          </div>

          {/* Right Panel Content */}
          <div className="flex-1 overflow-hidden flex flex-col">
            {/* HISTORY TAB */}
            {rightTab === 'history' && (
              <div className="flex flex-col h-full">
                {/* Search + New Chat */}
                <div className="p-2 space-y-2 border-b border-border shrink-0">
                  <div className="flex items-center gap-2">
                    <div className="relative flex-1">
                      <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground/50" />
                      <Input
                        placeholder="Search sessions..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="h-7 pl-7 text-xs bg-surface-2 border-border"
                      />
                    </div>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-7 w-7 p-0 text-muted-foreground hover:text-cyber-cyan shrink-0"
                          onClick={() => {
                            clearChat();
                            setActiveSessionId(null);
                          }}
                        >
                          <Plus className="h-3.5 w-3.5" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>New Chat</TooltipContent>
                    </Tooltip>
                  </div>
                </div>

                {/* Sessions list */}
                <div className="flex-1 overflow-y-auto p-2 space-y-1">
                  {filteredSessions.map((session) => (
                    <div
                      key={session.id}
                      className={`group relative px-3 py-2.5 rounded-lg cursor-pointer transition-colors ${
                        activeSessionId === session.id
                          ? 'bg-cyber-cyan/5 border border-cyber-cyan/20'
                          : 'hover:bg-surface-2 border border-transparent'
                      }`}
                      onClick={() => {
                        setActiveSessionId(session.id);
                        toast({ title: 'Session loaded', description: `"${session.title}" loaded.` });
                      }}
                    >
                      <div className="flex items-start gap-2">
                        <MessageSquare className="h-4 w-4 text-muted-foreground/60 mt-0.5 shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-foreground truncate group-hover:text-cyber-cyan transition-colors">
                            {session.title}
                          </p>
                          <p className="text-xs text-muted-foreground mt-0.5 line-clamp-1">{session.lastMessage}</p>
                          <div className="flex items-center gap-2 mt-1 text-[10px] text-muted-foreground/60">
                            <span>{session.timestamp}</span>
                            <span>·</span>
                            <span>{session.messageCount} msgs</span>
                          </div>
                        </div>
                      </div>
                      {/* Delete button */}
                      <button
                        className="absolute top-2 right-2 h-5 w-5 flex items-center justify-center rounded text-muted-foreground/0 group-hover:text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all"
                        onClick={(e) => {
                          e.stopPropagation();
                          toast({ title: 'Session deleted', description: `"${session.title}" removed.` });
                        }}
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </div>
                  ))}
                  {filteredSessions.length === 0 && (
                    <p className="text-xs text-muted-foreground text-center py-8">No sessions found</p>
                  )}
                </div>
              </div>
            )}

            {/* PROJECTS TAB */}
            {rightTab === 'projects' && (
              <div className="flex flex-col h-full">
                {/* Toolbar */}
                <div className="p-2 border-b border-border shrink-0">
                  <div className="flex items-center gap-2">
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-7 w-7 p-0 text-muted-foreground hover:text-cyber-cyan shrink-0"
                          onClick={() => toast({ title: 'New Project', description: 'Project creation coming soon.' })}
                        >
                          <Plus className="h-3.5 w-3.5" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>New Project</TooltipContent>
                    </Tooltip>
                    <span className="text-xs font-medium text-foreground">Projects</span>
                    <Badge variant="secondary" className="text-[10px] h-5 ml-auto">
                      {MOCK_PROJECTS.length}
                    </Badge>
                  </div>
                </div>

                {/* Project list */}
                <div className="flex-1 overflow-y-auto p-2 space-y-2">
                  {MOCK_PROJECTS.map((project) => {
                    const langColors: Record<string, string> = {
                      Python: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
                      'TypeScript/React': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
                      Go: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
                    };
                    const langColor = langColors[project.language] || 'bg-surface-2 text-muted-foreground border-border';
                    return (
                      <div
                        key={project.id}
                        className="group px-3 py-3 rounded-lg border border-border hover:border-cyber-cyan/20 hover:bg-surface-2 transition-all cursor-pointer"
                        onClick={() => {
                          setLeftTab('files');
                          setLeftOpen(true);
                          toast({ title: 'Project loaded', description: `"${project.name}" files displayed.` });
                        }}
                      >
                        <div className="flex items-start gap-2">
                          <FolderKanban className="h-4 w-4 text-cyber-cyan/70 mt-0.5 shrink-0" />
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-foreground group-hover:text-cyber-cyan transition-colors truncate">
                              {project.name}
                            </p>
                            <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{project.description}</p>
                            <div className="flex items-center gap-2 mt-2 flex-wrap">
                              <span className={`inline-flex items-center text-[10px] px-1.5 py-0.5 rounded border ${langColor}`}>
                                {project.language}
                              </span>
                              <span className="text-[10px] text-muted-foreground/60">{project.fileCount} files</span>
                              <span className="text-[10px] text-muted-foreground/60">{project.lastModified}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* CONFIG TAB */}
            {rightTab === 'config' && (
              <ScrollArea className="flex-1">
                <div className="p-3 space-y-5">
                  {/* Model */}
                  <div className="space-y-2">
                    <Label className="text-xs text-muted-foreground font-medium">Model</Label>
                    <Select value={model} onValueChange={setModel}>
                      <SelectTrigger className="h-8 text-xs bg-surface-2 border-border">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-surface-2 border-border">
                        <SelectItem value="claude-sonnet-4">Claude Sonnet 4</SelectItem>
                        <SelectItem value="claude-opus-4">Claude Opus 4</SelectItem>
                        <SelectItem value="claude-haiku-4">Claude Haiku 4</SelectItem>
                        <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                        <SelectItem value="gpt-4o-mini">GPT-4o Mini</SelectItem>
                        <SelectItem value="deepseek-v3">DeepSeek V3</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <Separator className="bg-border" />

                  {/* Temperature */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label className="text-xs text-muted-foreground font-medium">Temperature</Label>
                      <span className="text-xs font-mono text-cyber-cyan">{temperature.toFixed(2)}</span>
                    </div>
                    <Slider
                      value={[temperature]}
                      onValueChange={([v]) => setTemperature(v)}
                      min={0}
                      max={1}
                      step={0.05}
                      className="[&_[role=slider]]:bg-cyber-cyan [&_[role=slider]]:border-cyber-cyan"
                    />
                    <div className="flex justify-between text-[10px] text-muted-foreground/50">
                      <span>Precise</span>
                      <span>Creative</span>
                    </div>
                  </div>

                  <Separator className="bg-border" />

                  {/* System Prompt */}
                  <div className="space-y-2">
                    <Label className="text-xs text-muted-foreground font-medium">System Prompt</Label>
                    <textarea
                      value={systemPrompt}
                      onChange={(e) => setSystemPrompt(e.target.value)}
                      rows={4}
                      className="w-full resize-none rounded-md border border-border bg-surface-2 px-3 py-2 text-xs font-mono text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-cyber-cyan/30 transition-all"
                    />
                  </div>

                  <Separator className="bg-border" />

                  {/* Toggles */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label className="text-xs text-muted-foreground font-medium">Auto-save</Label>
                      <Switch checked={autoSave} onCheckedChange={setAutoSave} className="data-[state=checked]:bg-cyber-cyan" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-xs text-muted-foreground font-medium">Verbose Output</Label>
                      <Switch checked={verboseOutput} onCheckedChange={setVerboseOutput} className="data-[state=checked]:bg-cyber-cyan" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-xs text-muted-foreground font-medium">Line Numbers</Label>
                      <Switch checked={lineNumbers} onCheckedChange={setLineNumbers} className="data-[state=checked]:bg-cyber-cyan" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-xs text-muted-foreground font-medium">Auto-execute</Label>
                      <Switch checked={autoExecute} onCheckedChange={setAutoExecute} className="data-[state=checked]:bg-cyber-cyan" />
                    </div>
                  </div>

                  <Separator className="bg-border" />

                  {/* Context Window */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label className="text-xs text-muted-foreground font-medium">Context Window</Label>
                      <span className="text-xs font-mono text-cyber-cyan">{contextWindow} msgs</span>
                    </div>
                    <Slider
                      value={[contextWindow]}
                      onValueChange={([v]) => setContextWindow(v)}
                      min={10}
                      max={100}
                      step={5}
                      className="[&_[role=slider]]:bg-cyber-cyan [&_[role=slider]]:border-cyber-cyan"
                    />
                    <div className="flex justify-between text-[10px] text-muted-foreground/50">
                      <span>10</span>
                      <span>100</span>
                    </div>
                  </div>

                  <Separator className="bg-border" />

                  {/* Code Theme */}
                  <div className="space-y-2">
                    <Label className="text-xs text-muted-foreground font-medium">Code Theme</Label>
                    <Select value={codeTheme} onValueChange={setCodeTheme}>
                      <SelectTrigger className="h-8 text-xs bg-surface-2 border-border">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-surface-2 border-border">
                        <SelectItem value="dark">Dark</SelectItem>
                        <SelectItem value="light">Light</SelectItem>
                        <SelectItem value="monokai">Monokai</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </ScrollArea>
            )}
          </div>
        </div>

        {/* Right panel toggle */}
        {!rightOpen && (
          <Tooltip>
            <TooltipTrigger asChild>
              <button
                className="absolute right-0 top-1/2 -translate-y-1/2 z-10 w-6 h-16 flex items-center justify-center bg-surface-1 border border-border border-r-0 rounded-l-md text-muted-foreground hover:text-cyber-cyan transition-colors"
                onClick={() => setRightOpen(true)}
              >
                <ChevronLeft className="h-3.5 w-3.5" />
              </button>
            </TooltipTrigger>
            <TooltipContent side="left">Open history panel</TooltipContent>
          </Tooltip>
        )}
      </div>
    </TooltipProvider>
  );
}
