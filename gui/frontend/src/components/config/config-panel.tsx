'use client';

import { useState } from 'react';
import { Settings, Save, RotateCcw, ChevronDown, ChevronRight, ToggleLeft } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Switch } from '@/components/ui/switch';

interface ConfigSection {
  title: string;
  icon: React.ReactNode;
  settings: {
    key: string;
    label: string;
    description?: string;
    type: 'toggle' | 'number' | 'text' | 'select';
    value: string | number | boolean;
    options?: { label: string; value: string }[];
  }[];
}

const configSections: ConfigSection[] = [
  {
    title: 'General',
    icon: <Settings className="h-4 w-4" />,
    settings: [
      { key: 'projectName', label: 'Project Name', value: 'KaliGhost', type: 'text' },
      { key: 'darkMode', label: 'Dark Mode', description: 'Always use dark theme', value: true, type: 'toggle' },
      { key: 'autoSave', label: 'Auto-save', description: 'Save changes automatically', value: true, type: 'toggle' },
    ],
  },
  {
    title: 'Performance',
    icon: <ToggleLeft className="h-4 w-4" />,
    settings: [
      { key: 'maxAgents', label: 'Max Concurrent Agents', value: 10, type: 'number' },
      { key: 'memoryLimit', label: 'Memory Limit (MB)', value: 6144, type: 'number' },
      { key: 'requestTimeout', label: 'Request Timeout (s)', value: 30, type: 'number' },
      { key: 'gpu', label: 'GPU Acceleration', description: 'Use GPU for inference', value: false, type: 'toggle' },
    ],
  },
  {
    title: 'Network',
    icon: <Settings className="h-4 w-4" />,
    settings: [
      { key: 'proxyUrl', label: 'Proxy URL', value: 'socks5://127.0.0.1:9050', type: 'text' },
      { key: 'tlsVerify', label: 'Verify TLS Certificates', value: true, type: 'toggle' },
      { key: 'dnsOverHttps', label: 'DNS over HTTPS', value: true, type: 'toggle' },
    ],
  },
];

interface SectionState {
  [key: string]: {
    [key: string]: string | number | boolean;
  };
}

export function ConfigPanel() {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({
    General: true,
    Performance: false,
    Network: false,
  });

  const [settings, setSettings] = useState<SectionState>(
    configSections.reduce((acc, section) => ({
      ...acc,
      [section.title]: section.settings.reduce((s, setting) => ({
        ...s,
        [setting.key]: setting.value,
      }), {}),
    }), {})
  );

  const toggleSection = (title: string) => {
    setExpanded((prev) => ({ ...prev, [title]: !prev[title] }));
  };

  const updateSetting = (section: string, key: string, value: string | number | boolean) => {
    setSettings((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value,
      },
    }));
  };

  const handleReset = () => {
    setSettings(
      configSections.reduce((acc, section) => ({
        ...acc,
        [section.title]: section.settings.reduce((s, setting) => ({
          ...s,
          [setting.key]: setting.value,
        }), {}),
      }), {})
    );
  };

  return (
    <div className="h-full overflow-y-auto p-4 space-y-3 grid-bg">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-foreground">Configuration</h3>
          <p className="text-[10px] text-muted-foreground mt-0.5">System settings and preferences</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleReset}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-2 border border-border text-[10px] text-muted-foreground hover:text-foreground transition-all"
          >
            <RotateCcw className="h-3 w-3" /> Reset
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/30 text-[10px] text-cyber-cyan hover:bg-cyber-cyan/20 transition-all">
            <Save className="h-3 w-3" /> Save
          </button>
        </div>
      </div>

      {/* Sections */}
      {configSections.map((section) => (
        <div key={section.title} className="cyber-panel overflow-hidden">
          <button
            onClick={() => toggleSection(section.title)}
            className="w-full flex items-center justify-between px-4 py-3 hover:bg-surface-2/50 transition-colors"
          >
            <div className="flex items-center gap-2.5">
              <span className="text-cyber-cyan">{section.icon}</span>
              <span className="text-xs font-medium text-foreground">{section.title}</span>
            </div>
            {expanded[section.title] ? (
              <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
            ) : (
              <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
            )}
          </button>

          {expanded[section.title] && (
            <div className="px-4 pb-4 border-t border-border pt-3 space-y-3">
              {section.settings.map((setting) => (
                <div key={setting.key} className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <label className="text-[11px] text-foreground font-medium">{setting.label}</label>
                    {setting.type === 'toggle' && (
                      <Switch
                        checked={Boolean(settings[section.title][setting.key])}
                        onCheckedChange={(value) =>
                          updateSetting(section.title, setting.key, value)
                        }
                      />
                    )}
                  </div>
                  {setting.description && (
                    <p className="text-[9px] text-muted-foreground">{setting.description}</p>
                  )}
                  {setting.type === 'text' && (
                    <input
                      type="text"
                      value={String(settings[section.title][setting.key])}
                      onChange={(e) =>
                        updateSetting(section.title, setting.key, e.target.value)
                      }
                      className="w-full h-7 px-3 text-xs bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-cyber-cyan/50 transition-all"
                    />
                  )}
                  {setting.type === 'number' && (
                    <input
                      type="number"
                      value={String(settings[section.title][setting.key])}
                      onChange={(e) =>
                        updateSetting(section.title, setting.key, Number(e.target.value))
                      }
                      className="w-full h-7 px-3 text-xs bg-surface-0 border border-border rounded-md text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-cyber-cyan/50 transition-all"
                    />
                  )}
                  {setting.type === 'select' && setting.options && (
                    <select
                      value={String(settings[section.title][setting.key])}
                      onChange={(e) =>
                        updateSetting(section.title, setting.key, e.target.value)
                      }
                      className="w-full h-7 px-3 text-xs bg-surface-0 border border-border rounded-md text-foreground focus:outline-none focus:border-cyber-cyan/50 transition-all"
                    >
                      {setting.options.map((opt) => (
                        <option key={opt.value} value={opt.value} className="bg-surface-1">
                          {opt.label}
                        </option>
                      ))}
                    </select>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}

      {/* Info */}
      <div className="cyber-panel p-3 text-[10px] text-muted-foreground space-y-1">
        <p>✓ All settings are saved automatically</p>
        <p>✓ Changes take effect immediately</p>
        <p>✓ Use Reset to restore defaults</p>
      </div>
    </div>
  );
}
