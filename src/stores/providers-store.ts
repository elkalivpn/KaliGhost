'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

/* ══════════════════════════════════════════════════════════
 *  Provider Store — Persiste en localStorage
 *  Gestiona claves API de LLM y tools. Default: todo local.
 * ══════════════════════════════════════════════════════════ */

export type ConnectionMode = 'local' | 'cloud';
export type ProviderStatus = 'disconnected' | 'testing' | 'connected' | 'error';

export interface ProviderConfig {
  id: string;
  name: string;
  category: 'llm' | 'tool';
  description: string;
  icon: string;           // emoji para identificar visualmente
  apiKey: string;
  baseUrl: string;        // endpoint personalizable
  model: string;          // modelo por defecto del proveedor
  enabled: boolean;
  status: ProviderStatus;
  isPaid: boolean;        // requiere subscripcion
  docsUrl: string;        // enlace a la documentacion
}

export interface ProvidersState {
  connectionMode: ConnectionMode;
  providers: ProviderConfig[];
  activeLlmProvider: string;   // id del proveedor LLM activo
  setConnectionMode: (mode: ConnectionMode) => void;
  setActiveLlmProvider: (id: string) => void;
  updateProvider: (id: string, partial: Partial<ProviderConfig>) => void;
  resetProvider: (id: string) => void;
  resetAll: () => void;
  getActiveLlm: () => ProviderConfig | undefined;
}

const defaultProviders: ProviderConfig[] = [
  /* ── LLM Providers ── */
  {
    id: 'ollama',
    name: 'Ollama (Local)',
    category: 'llm',
    description: 'Modelos locales. Sin API key necesaria. Solo necesitas Ollama instalado.',
    icon: '🦙',
    apiKey: '',
    baseUrl: 'http://localhost:11434',
    model: 'llama3',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://ollama.ai',
  },
  {
    id: 'anthropic',
    name: 'Anthropic (Claude)',
    category: 'llm',
    description: 'Claude Opus 4, Sonnet 4, Haiku 4. Requiere subscripcion.',
    icon: '🤖',
    apiKey: '',
    baseUrl: 'https://api.anthropic.com',
    model: 'claude-sonnet-4-20250514',
    enabled: false,
    status: 'disconnected',
    isPaid: true,
    docsUrl: 'https://console.anthropic.com',
  },
  {
    id: 'openai',
    name: 'OpenAI',
    category: 'llm',
    description: 'GPT-4o, GPT-4o Mini, o1, o3. Requiere subscripcion.',
    icon: '⚡',
    apiKey: '',
    baseUrl: 'https://api.openai.com/v1',
    model: 'gpt-4o',
    enabled: false,
    status: 'disconnected',
    isPaid: true,
    docsUrl: 'https://platform.openai.com/api-keys',
  },
  {
    id: 'google',
    name: 'Google AI (Gemini)',
    category: 'llm',
    description: 'Gemini 2.5 Pro, Flash. Requiere API key de Google AI Studio.',
    icon: '💎',
    apiKey: '',
    baseUrl: 'https://generativelanguage.googleapis.com/v1beta',
    model: 'gemini-2.5-pro',
    enabled: false,
    status: 'disconnected',
    isPaid: true,
    docsUrl: 'https://aistudio.google.com/apikey',
  },
  {
    id: 'mistral',
    name: 'Mistral AI',
    category: 'llm',
    description: 'Mistral Large, Medium, Small. Plan gratuito disponible.',
    icon: '🌊',
    apiKey: '',
    baseUrl: 'https://api.mistral.ai/v1',
    model: 'mistral-large-latest',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://console.mistral.ai',
  },
  {
    id: 'deepseek',
    name: 'DeepSeek',
    category: 'llm',
    description: 'DeepSeek V3, R1. Muy economico. Compatible con API OpenAI.',
    icon: '🔍',
    apiKey: '',
    baseUrl: 'https://api.deepseek.com/v1',
    model: 'deepseek-chat',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://platform.deepseek.com/api_keys',
  },
  {
    id: 'groq',
    name: 'Groq',
    category: 'llm',
    description: 'Llama 3, Mixtral. Inferencia ultra-rapida. Plan gratuito.',
    icon: '🚀',
    apiKey: '',
    baseUrl: 'https://api.groq.com/openai/v1',
    model: 'llama-3.1-70b-versatile',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://console.groq.com/keys',
  },
  {
    id: 'together',
    name: 'Together AI',
    category: 'llm',
    description: 'Modelos open-source hosted. Llama, Qwen, FLUX. Plan gratuito.',
    icon: '🤝',
    apiKey: '',
    baseUrl: 'https://api.together.xyz/v1',
    model: 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://api.together.xyz/settings/api-keys',
  },
  {
    id: 'lmstudio',
    name: 'LM Studio (Local)',
    category: 'llm',
    description: 'Modelos locales via LM Studio. Sin API key necesaria.',
    icon: '🖥️',
    apiKey: '',
    baseUrl: 'http://localhost:1234/v1',
    model: 'local-model',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://lmstudio.ai',
  },
  {
    id: 'custom',
    name: 'Custom OpenAI-Compatible',
    category: 'llm',
    description: 'Cualquier endpoint compatible con OpenAI (vLLM, text-generation-webui, etc.)',
    icon: '🔧',
    apiKey: '',
    baseUrl: 'http://localhost:8080/v1',
    model: 'default',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: '',
  },

  /* ── Tool Providers ── */
  {
    id: 'shodan',
    name: 'Shodan',
    category: 'tool',
    description: 'Busqueda de dispositivos y servicios expuestos en internet.',
    icon: '📡',
    apiKey: '',
    baseUrl: 'https://api.shodan.io',
    model: '',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://account.shodan.io',
  },
  {
    id: 'virustotal',
    name: 'VirusTotal',
    category: 'tool',
    description: 'Analisis de archivos, URLs e IPs contra multiples antivirus.',
    icon: '🛡️',
    apiKey: '',
    baseUrl: 'https://www.virustotal.com/api/v3',
    model: '',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://www.virustotal.com/gui/my-apikey',
  },
  {
    id: 'securitytrails',
    name: 'SecurityTrails',
    category: 'tool',
    description: 'Historial de DNS, WHOIS, y datos de infraestructura.',
    icon: '🗺️',
    apiKey: '',
    baseUrl: 'https://api.securitytrails.com/v1',
    model: '',
    enabled: false,
    status: 'disconnected',
    isPaid: true,
    docsUrl: 'https://securitytrails.com/corp/api',
  },
  {
    id: 'hunter',
    name: 'Hunter.io',
    category: 'tool',
    description: 'Búsqueda de correos corporativos y perfiles de dominios.',
    icon: '📧',
    apiKey: '',
    baseUrl: 'https://api.hunter.io/v2',
    model: '',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://hunter.io/api',
  },
  {
    id: 'censys',
    name: 'Censys',
    category: 'tool',
    description: 'Escaneo de hosts, certificados SSL y datos de internet.',
    icon: '🌐',
    apiKey: '',
    baseUrl: 'https://search.censys.io/api',
    model: '',
    enabled: false,
    status: 'disconnected',
    isPaid: false,
    docsUrl: 'https://censys.io/account/api',
  },
];

export const useProvidersStore = create<ProvidersState>()(
  persist(
    (set, get) => ({
      connectionMode: 'local' as ConnectionMode,
      providers: defaultProviders,
      activeLlmProvider: 'ollama',

      setConnectionMode: (mode) => set({ connectionMode: mode }),

      setActiveLlmProvider: (id) => set({ activeLlmProvider: id }),

      updateProvider: (id, partial) =>
        set((state) => ({
          providers: state.providers.map((p) =>
            p.id === id ? { ...p, ...partial, status: partial.status ?? p.status } : p
          ),
        })),

      resetProvider: (id) =>
        set((state) => ({
          providers: state.providers.map((p) =>
            p.id === id
              ? { ...defaultProviders.find((d) => d.id === id)!, status: 'disconnected' }
              : p
          ),
        })),

      resetAll: () =>
        set({
          connectionMode: 'local' as ConnectionMode,
          providers: defaultProviders.map((p) => ({ ...p, status: 'disconnected' })),
          activeLlmProvider: 'ollama',
        }),

      getActiveLlm: () => {
        const state = get();
        if (state.connectionMode === 'local') return undefined;
        return state.providers.find((p) => p.id === state.activeLlmProvider && p.enabled && p.apiKey);
      },
    }),
    {
      name: 'dragon-providers-config',
      version: 1,
    }
  )
);
