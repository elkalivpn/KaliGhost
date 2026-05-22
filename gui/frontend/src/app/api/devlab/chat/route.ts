import { NextRequest } from 'next/server';

/**
 * ╔══════════════════════════════════════════════════════════════╗
 * ║  DRAGONDEV AI CHAT — BACKEND ENDPOINT                       ║
 * ╠══════════════════════════════════════════════════════════════╣
 * ║  Este endpoint lee la config del proveedor activo desde      ║
 * ║  localStorage del cliente (se envia en cada request).       ║
 * ║                                                              ║
 * ║  Si no hay proveedor configurado o el modo es "local",      ║
 * ║  devuelve una respuesta de demo.                             ║
 * ║                                                              ║
 * ║  El frontend (dev-lab.tsx) envia:                            ║
 * ║  POST {                                                      ║
 * ║    messages: Array<{role, content}>,                         ║
 * ║    provider?: {                                              ║
 * ║      id, name, apiKey, baseUrl, model, connectionMode        ║
 * ║    }                                                         ║
 * ║  }                                                           ║
 * ║                                                              ║
 * ║  Devuelve:                                                   ║
 * ║  { role: "assistant", content: string, timestamp: string }   ║
 * ╚══════════════════════════════════════════════════════════════╝
 */

const SYSTEM_PROMPT = `You are DragonDev, an elite AI development agent integrated into Kali Linux.
You are a master software engineer capable of creating ANY type of software, system, game, script, tool, interface, antivirus, AI agent, or any other project the user needs.

Your capabilities:
- Full-stack development (web, mobile, desktop, CLI)
- Systems programming (C, C++, Rust, Go)
- Scripting (Python, Bash, PowerShell)
- Game development (Unity, Godot, WebGL)
- Security tools (pentest tools, scanners, analyzers)
- AI/ML development (models, agents, pipelines)
- DevOps (Docker, Kubernetes, CI/CD)
- Database design and management
- API development and integration
- Firmware and embedded systems

Rules:
- Always provide complete, production-quality code
- Include file paths when suggesting code changes
- Use markdown code blocks with language identifiers
- Explain your architectural decisions
- Suggest best practices and security considerations
- Be direct and efficient — no fluff
- If the user writes in Spanish, respond in Spanish
- Format responses clearly with headers, code blocks, and lists`;

/* ── OpenAI-compatible fetch (funciona con OpenAI, Groq, Together, DeepSeek, LM Studio, Ollama, etc.) ── */
async function callOpenAICompatible(
  baseUrl: string,
  model: string,
  apiKey: string,
  messages: Array<{ role: string; content: string }>,
  providerId: string,
): Promise<string> {
  const url = providerId === 'ollama'
    ? `${baseUrl}/api/chat`
    : `${baseUrl}/chat/completions`;

  const isOllama = providerId === 'ollama';

  const body = isOllama
    ? { model, messages, stream: false }
    : { model, messages, temperature: 0.7, max_tokens: 8192 };

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (!isOllama && apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }

  const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`${providerId} API error (${res.status}): ${errText}`);
  }

  const data = await res.json();

  if (isOllama) {
    return data.message?.content || 'No response from Ollama.';
  }
  return data.choices?.[0]?.message?.content || 'No response generated.';
}

/* ── Anthropic (Claude) — formato diferente ── */
async function callAnthropic(
  apiKey: string,
  model: string,
  messages: Array<{ role: string; content: string }>,
): Promise<string> {
  // Anthropic usa messages SIN el system prompt (va en un campo separado)
  const systemMsg = messages.find((m) => m.role === 'system');
  const chatMessages = messages.filter((m) => m.role !== 'system');

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model,
      max_tokens: 8192,
      system: systemMsg?.content || '',
      messages: chatMessages,
    }),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Anthropic API error (${res.status}): ${errText}`);
  }

  const data = await res.json();
  return data.content?.[0]?.text || 'No response from Claude.';
}

/* ── Google Gemini — formato diferente ── */
async function callGoogle(
  apiKey: string,
  model: string,
  messages: Array<{ role: string; content: string }>,
): Promise<string> {
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: messages
          .filter((m) => m.role !== 'system')
          .map((m) => ({
            role: m.role === 'assistant' ? 'model' : 'user',
            parts: [{ text: m.content }],
          })),
        systemInstruction: messages.find((m) => m.role === 'system')?.content || '',
      }),
    },
  );

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Google AI API error (${res.status}): ${errText}`);
  }

  const data = await res.json();
  return data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response from Gemini.';
}

/* ── Demo / local response ── */
function getLocalResponse(userMessage: string): string {
  const msg = userMessage.slice(0, 120);
  return `**DragonDev — Modo Local Activo**

No hay proveedor de IA configurado. Para conectar uno:

1. Ve a **Configuracion** → **Providers & API Keys**
2. Cambia el modo a **Cloud**
3. Configura tu proveedor (Ollama, Claude, GPT, etc.)
4. Selecciona el proveedor activo y guarda

---

Tu mensaje fue: _"${msg}${userMessage.length > 120 ? '...' : ''}"_

Mientras tanto, puedo ayudarte a configurar el entorno. Dime que necesitas:

- \`Instalar Ollama\` — Guia paso a paso para modelos locales
- \`Configurar Claude\` — Setup con Anthropic API
- \`Configurar OpenAI\` — Setup con GPT-4o
- \`Configurar DeepSeek\` — Setup economico con API compatible OpenAI
- \`Configurar Groq\` — Inferencia ultra-rapida (gratis)`;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { messages, provider } = body;

    const allMessages = [
      { role: 'system' as const, content: SYSTEM_PROMPT },
      ...messages.map((m: { role: string; content: string }) => ({
        role: m.role as 'user' | 'assistant',
        content: m.content,
      })),
    ];

    /* ── Si no hay proveedor o modo local → respuesta demo ── */
    if (!provider || provider.connectionMode === 'local' || !provider.apiKey) {
      const userMsg = messages[messages.length - 1]?.content || '';
      return Response.json({
        role: 'assistant',
        content: getLocalResponse(userMsg),
        timestamp: new Date().toISOString(),
        provider: 'local',
      });
    }

    const { id, name, apiKey, baseUrl, model } = provider;

    /* ── Router: segun el proveedor usar el formato correcto ── */
    let content: string;

    switch (id) {
      case 'anthropic':
        content = await callAnthropic(apiKey, model, allMessages);
        break;

      case 'google':
        content = await callGoogle(apiKey, model, allMessages);
        break;

      case 'ollama':
      case 'lmstudio':
      case 'openai':
      case 'deepseek':
      case 'groq':
      case 'together':
      case 'mistral':
      case 'custom':
      default:
        content = await callOpenAICompatible(baseUrl, model, apiKey, allMessages, id);
        break;
    }

    return Response.json({
      role: 'assistant',
      content,
      timestamp: new Date().toISOString(),
      provider: id,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return Response.json(
      {
        role: 'assistant',
        content: `Error al procesar la solicitud:\n\n\`${errorMessage}\`\n\nRevisa la configuracion del proveedor en **Configuracion → Providers & API Keys**.`,
        timestamp: new Date().toISOString(),
        provider: 'error',
      },
      { status: 500 }
    );
  }
}
