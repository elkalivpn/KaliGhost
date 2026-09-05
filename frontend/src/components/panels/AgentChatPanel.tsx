import { useState } from 'react'
import { useAppStore } from '../../store/appStore'
import { MessageSquare, Play, Save, Copy, Trash2 } from 'lucide-react'

export function AgentChatPanel() {
  const { agentConfig, addToTerminal } = useAppStore()
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([
    {
      role: 'assistant',
      content: `Yrays Agent initialized. Model: ${agentConfig.model}\n\nReady to assist with:\n• Zero-day exploit development\n• Malware analysis and reverse engineering\n• Red team operations\n• Bug bounty hunting\n• Steganography and covert comms\n• Anti-forensics\n\nHow can I help you today?`,
    },
  ])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isProcessing) return
    
    const userMessage = input.trim()
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setInput('')
    setIsProcessing(true)
    
    // Simulate AI response (would connect to backend in production)
    setTimeout(() => {
      let response = ''
      
      if (userMessage.toLowerCase().includes('exploit')) {
        response = `Analyzing exploit requirements...\n\nBased on your request, I can help develop a proof-of-concept exploit. Please provide:\n1. Target software/version\n2. Vulnerability type (buffer overflow, RCE, etc.)\n3. Desired payload type\n\nExample command:\n\x1b[1;36mexploit-gen --cve CVE-2024-1234 --payload reverse_shell\x1b[0m`
      } else if (userMessage.toLowerCase().includes('malware')) {
        response = `Malware analysis capabilities ready.\n\nI can:\n• Perform static analysis (strings, imports, sections)\n• Execute in isolated sandbox\n• Monitor behavior (registry, network, files)\n• Generate YARA rules\n• Extract IOCs\n\nUpload sample or provide hash for analysis.`
      } else if (userMessage.toLowerCase().includes('cve')) {
        response = `CVE Intelligence Engine active.\n\nSearching local database with semantic matching...\n\nProvide CVE ID or vulnerability description for:\n• Technical details\n• Affected versions\n• Exploit availability\n• Mitigation strategies\n• Related advisories`
      } else if (userMessage.toLowerCase().includes('stego')) {
        response = `Steganography module initialized.\n\nAvailable techniques:\n• LSB (Least Significant Bit)\n• DCT (Discrete Cosine Transform)\n• Spread Spectrum\n• Audio steganography\n• Video steganography\n\nCommand format:\n\x1b[1;36mstego hide --input secret.txt --cover image.png --output output.png\x1b[0m`
      } else {
        response = `Received: "${userMessage}"\n\nI'm ready to assist with advanced cybersecurity operations. My capabilities include:\n\n\x1b[1;32m✓\x1b[0m Exploit development (0-day research)\n\x1b[1;32m✓\x1b[0m Malware analysis & RE\n\x1b[1;32m✓\x1b[0m Red/Purple team automation\n\x1b[1;32m✓\x1b[0m Steganography & covert channels\n\x1b[1;32m✓\x1b[0m Anti-forensics & OPSEC\n\x1b[1;32m✓\x1b[0m CVE intelligence with RAG\n\nWhat's your objective?`
      }
      
      setMessages((prev) => [...prev, { role: 'assistant', content: response }])
      addToTerminal(`[AI] ${response}`)
      setIsProcessing(false)
    }, 800)
  }
  
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }
  
  return (
    <div className="flex flex-col h-full bg-bg-secondary border border-border-color rounded-lg overflow-hidden glow-border">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-bg-tertiary border-b border-border-color">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-accent-purple" />
          <div>
            <h3 className="font-bold glow-text">Yrays Agent</h3>
            <p className="text-xs text-text-secondary">
              {agentConfig.model} • Temp: {agentConfig.temperature} • {agentConfig.uncensored ? 'Uncensored' : 'Restricted'}
            </p>
          </div>
        </div>
        {agentConfig.autonomousMode && (
          <span className="px-2 py-1 bg-accent-red/20 text-accent-red text-xs rounded animate-pulse">
            AUTONOMOUS
          </span>
        )}
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-lg p-3 ${
                msg.role === 'user'
                  ? 'bg-accent-purple/20 border border-accent-purple/50'
                  : 'bg-bg-tertiary border border-border-color'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className={`text-xs font-bold ${
                  msg.role === 'user' ? 'text-accent-purple' : 'text-accent-cyan'
                }`}>
                  {msg.role === 'user' ? 'YOU' : 'YRAYS'}
                </span>
                {msg.role === 'assistant' && (
                  <div className="flex gap-1">
                    <button
                      onClick={() => copyToClipboard(msg.content)}
                      className="p-1 hover:bg-bg-secondary rounded transition-colors"
                      title="Copy"
                    >
                      <Copy className="w-3 h-3 text-text-secondary" />
                    </button>
                  </div>
                )}
              </div>
              <pre
                className="text-sm whitespace-pre-wrap break-words font-mono"
                dangerouslySetInnerHTML={{ __html: msg.content }}
              />
            </div>
          </div>
        ))}
        
        {isProcessing && (
          <div className="flex justify-start">
            <div className="bg-bg-tertiary border border-border-color rounded-lg p-3">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-accent-purple rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-accent-purple rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-accent-purple rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Input */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2 p-3 bg-bg-tertiary border-t border-border-color">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your operation..."
          className="flex-1 bg-bg-primary border border-border-color rounded px-3 py-2 text-sm outline-none focus:border-accent-purple transition-colors"
          disabled={isProcessing}
        />
        <button
          type="submit"
          disabled={isProcessing || !input.trim()}
          className="p-2 bg-accent-purple hover:bg-accent-purple/80 disabled:bg-bg-secondary disabled:text-text-secondary rounded transition-colors"
        >
          <Play className="w-4 h-4" />
        </button>
      </form>
    </div>
  )
}
