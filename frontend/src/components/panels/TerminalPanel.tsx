import { useState, useRef, useEffect } from 'react'
import { useAppStore } from '../../store/appStore'
import { Send, Terminal, X, Maximize2, Minimize2 } from 'lucide-react'

export function TerminalPanel() {
  const { terminalHistory, addToTerminal, clearTerminal, activePanels, togglePanel } = useAppStore()
  const [input, setInput] = useState('')
  const [isMaximized, setIsMaximized] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [terminalHistory])
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return
    
    addToTerminal(`\x1b[1;36muser@kalighost\x1b[0m:\x1b[1;34m~\x1b[0m$ ${input}`)
    
    // Simulate command processing (would connect to backend in production)
    setTimeout(() => {
      if (input.startsWith('help')) {
        addToTerminal('\x1b[1;32mAvailable commands:\x1b[0m')
        addToTerminal('  sandbox <file>     - Analyze malware in sandbox')
        addToTerminal('  purple-team <target> - Start purple team operation')
        addToTerminal('  exploit-gen <cve>  - Generate exploit for CVE')
        addToTerminal('  stego hide <file>  - Hide data using steganography')
        addToTerminal('  ram-exec <binary>  - Execute in RAM only')
        addToTerminal('  route set <mode>   - Set network routing (tor/vpn/direct)')
        addToTerminal('  cve-search <query> - Search CVE database')
        addToTerminal('  clear              - Clear terminal')
      } else if (input === 'clear') {
        clearTerminal()
      } else {
        addToTerminal(`\x1b[1;31mCommand not recognized: ${input}\x1b[0m`)
        addToTerminal('Type "help" for available commands')
      }
    }, 100)
    
    setInput('')
  }
  
  return (
    <div className={`flex flex-col bg-bg-primary border border-border-color rounded-lg overflow-hidden glow-border transition-all ${
      isMaximized ? 'fixed inset-4 z-50' : 'h-full'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-bg-tertiary border-b border-border-color">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-accent-cyan" />
          <span className="text-sm font-bold">Terminal</span>
          {activePanels.includes('terminal') && (
            <span className="px-2 py-0.5 bg-accent-green/20 text-accent-green text-xs rounded">
              ACTIVE
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsMaximized(!isMaximized)}
            className="p-1 hover:bg-bg-secondary rounded transition-colors"
          >
            {isMaximized ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
          <button
            onClick={() => togglePanel('terminal')}
            className="p-1 hover:bg-accent-red/20 hover:text-accent-red rounded transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      {/* Terminal Output */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-sm bg-black/50">
        {terminalHistory.length === 0 && (
          <div className="text-text-secondary opacity-50">
            KaliGhost IDE v1.0.0 - Advanced Cybersecurity Environment<br />
            Type "help" for available commands<br />
            <br />
          </div>
        )}
        
        {terminalHistory.map((line, index) => (
          <div
            key={index}
            dangerouslySetInnerHTML={{ __html: line }}
            className="whitespace-pre-wrap break-all"
          />
        ))}
        <div ref={bottomRef} />
      </div>
      
      {/* Input */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2 p-3 bg-bg-tertiary border-t border-border-color">
        <span className="text-accent-green font-mono">{'>'}</span>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter command..."
          className="flex-1 bg-transparent outline-none text-text-primary font-mono text-sm"
          autoFocus
        />
        <button
          type="submit"
          className="p-2 bg-accent-cyan/20 hover:bg-accent-cyan/30 text-accent-cyan rounded transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  )
}
