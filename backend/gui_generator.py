#!/usr/bin/env python3
"""
🐉 KaliGhost GUI Generator
CLI → GUI/Web automation, UX design for complex tools
"""

import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class UIFramework(Enum):
    """UI generation frameworks"""
    REACT = "react"
    VUE = "vue"
    ELECTRON = "electron"
    TAURI = "tauri"
    FLUTTER = "flutter"


class ComponentType(Enum):
    """UI component types"""
    INPUT = "input"
    BUTTON = "button"
    SELECT = "select"
    CHECKBOX = "checkbox"
    TOGGLE = "toggle"
    TEXTAREA = "textarea"
    SLIDER = "slider"
    TABLE = "table"
    CHART = "chart"
    PROGRESS = "progress"
    ALERT = "alert"


@dataclass
class UIComponent:
    """Single UI component"""
    id: str
    type: ComponentType
    label: str
    required: bool = False
    placeholder: Optional[str] = None
    options: Optional[List[str]] = None
    validation: Optional[str] = None
    help_text: Optional[str] = None


@dataclass
class UIForm:
    """Form composed of components"""
    id: str
    title: str
    description: str
    fields: List[UIComponent]
    submit_label: str = "Submit"
    cancel_label: str = "Cancel"


@dataclass
class UIDashboard:
    """Dashboard with metrics and controls"""
    id: str
    title: str
    sections: List[Dict[str, Any]]


class GUIGenerator:
    """Generate GUI/Web interfaces from CLI tools"""

    async def analyze_cli_tool(self, cli_path: Path) -> Dict[str, Any]:
        """Analyze CLI tool to extract parameters"""
        logger.info(f"🔍 Analyzing CLI tool: {cli_path}")

        import subprocess
        try:
            result = subprocess.run(
                ["python3", str(cli_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            help_text = result.stdout
        except:
            help_text = ""

        parameters = self._parse_cli_parameters(help_text)
        logger.info(f"  📋 Found {len(parameters)} parameters")

        return {
            "tool_name": cli_path.stem,
            "help_text": help_text,
            "parameters": parameters
        }

    def _parse_cli_parameters(self, help_text: str) -> List[Dict[str, Any]]:
        """Extract parameters from help text"""
        parameters = []
        lines = help_text.split('\n')
        for line in lines:
            if line.startswith('  -'):
                param_name = line.split()[0].lstrip('-')
                param_help = ' '.join(line.split()[1:])
                parameters.append({
                    "name": param_name,
                    "help": param_help,
                    "type": "string"
                })
        return parameters

    async def generate_react_ui(
        self,
        tool_name: str,
        parameters: List[Dict[str, Any]],
        features: Optional[List[str]] = None
    ) -> str:
        """Generate React web interface"""
        logger.info(f"🎨 Generating React UI for {tool_name}")

        features = features or ["command_builder", "real_time_output", "result_export"]

        # Build form fields
        form_fields = ""
        for param in parameters:
            form_fields += f'              <div className="mb-4">\n'
            form_fields += f'                <label className="block text-white mb-2">{param["name"]}</label>\n'
            form_fields += f'                <input type="text" name="{param["name"]}" className="w-full px-3 py-2 bg-slate-600 text-white rounded" />\n'
            form_fields += f'              </div>\n'

        react_code = f'''import React, {{ useState }} from 'react';

export default function {tool_name}UI() {{
  const [formData, setFormData] = useState({{}});
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {{
    const {{ name, value }} = e.target;
    setFormData(prev => ({{ ...prev, [name]: value }}));
  }};

  const handleSubmit = async (e) => {{
    e.preventDefault();
    setLoading(true);
    try {{
      const response = await fetch('/api/execute', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ tool: '{tool_name}', params: formData }})
      }});
      const result = await response.json();
      setOutput(result.output);
    }} catch (error) {{
      setOutput(`Error: ${{error.message}}`);
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-white mb-8">{tool_name}</h1>
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-slate-700 p-6 rounded-lg">
            <form onSubmit={{handleSubmit}}>
{form_fields}
              <button type="submit" disabled={{loading}} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                {{loading ? 'Processing...' : 'Execute'}}
              </button>
            </form>
          </div>
          <div className="bg-slate-700 p-6 rounded-lg">
            <h2 className="text-white text-lg mb-4">Output</h2>
            <pre className="bg-slate-900 text-green-400 p-4 rounded h-96 overflow-auto">
              {{output || 'Waiting...'}}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}}
'''

        logger.info(f"✅ React UI generated ({len(react_code)} chars)")
        return react_code

    async def generate_tauri_desktop_app(
        self,
        tool_name: str,
        parameters: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Generate Tauri desktop application"""
        logger.info(f"🖥️  Generating Tauri desktop app for {tool_name}")

        tauri_config = {
            "productName": tool_name,
            "identifier": f"com.kalighost.{tool_name.lower()}",
            "mainFile": "index.html"
        }

        tauri_rust = f"""
use tauri::command;
use std::process::Command;

#[command]
fn execute_tool(params: std::collections::HashMap<String, String>) -> Result<String, String> {{
    let mut cmd = Command::new("python3");
    cmd.arg("/path/to/{tool_name}.py");
    for (key, value) in params {{
        cmd.arg(format!("--{{}}", key));
        cmd.arg(value);
    }}
    match cmd.output() {{
        Ok(output) => Ok(String::from_utf8_lossy(&output.stdout).to_string()),
        Err(e) => Err(e.to_string())
    }}
}}

fn main() {{
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![execute_tool])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}}
"""

        logger.info(f"✅ Tauri desktop app generated")
        return {
            "tauri_config": json.dumps(tauri_config, indent=2),
            "main_rs": tauri_rust
        }

    async def generate_dashboard(
        self,
        tool_name: str,
        metrics: List[str]
    ) -> str:
        """Generate monitoring dashboard"""
        logger.info(f"📊 Generating dashboard for {tool_name}")

        dashboard_code = f"""
import React, {{ useEffect, useState }} from 'react';

export default function {tool_name}Dashboard() {{
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {{
    const interval = setInterval(async () => {{
      const response = await fetch('/api/metrics');
      const data = await response.json();
      setMetrics(prev => [...prev.slice(-59), data]);
    }}, 1000);
    
    return () => clearInterval(interval);
  }}, []);

  return (
    <div className="bg-slate-900 p-6 rounded-lg text-white">
      <h2 className="text-2xl mb-6">{tool_name} Metrics</h2>
      <div className="grid grid-cols-2 gap-4">
        <div><h3>Performance</h3></div>
        <div><h3>Stats</h3></div>
      </div>
    </div>
  );
}}
"""

        logger.info(f"✅ Dashboard generated")
        return dashboard_code


class UXDesignEngine:
    """Design UX flows for complex tools"""

    def design_wizard_flow(
        self,
        tool_name: str,
        steps: List[str]
    ) -> List[UIForm]:
        """Create step-by-step wizard"""
        logger.info(f"🧙 Designing wizard for {tool_name} ({len(steps)} steps)")

        forms = []
        for i, step in enumerate(steps, 1):
            form = UIForm(
                id=f"step_{i}",
                title=f"Step {i}: {step}",
                description=f"Complete this step to proceed",
                fields=[],
                submit_label="Next" if i < len(steps) else "Complete"
            )
            forms.append(form)

        logger.info(f"✅ Wizard designed: {len(forms)} steps")
        return forms

    def design_dashboard_layout(
        self,
        metrics: List[str],
        controls: List[str]
    ) -> Dict[str, Any]:
        """Design security tool dashboard"""
        logger.info(f"📐 Designing dashboard layout")

        layout = {
            "header": {
                "title": "Security Control Center",
                "search_bar": True,
                "notifications": True
            },
            "sidebar": {
                "navigation": controls
            },
            "main": {
                "widgets": [
                    {"type": "metric", "name": m, "size": "half"} for m in metrics
                ]
            },
            "footer": {
                "status": "All systems operational",
                "last_update": "now"
            }
        }

        logger.info(f"✅ Dashboard layout designed")
        return layout


class GUIAutomationEngine:
    """Orchestrates GUI generation"""

    def __init__(self):
        self.gui_gen = GUIGenerator()
        self.ux_gen = UXDesignEngine()

    async def cli_to_web_ui(
        self,
        cli_tool_path: Path,
        output_dir: Path
    ) -> bool:
        """Convert CLI tool to web UI"""
        logger.info(f"🔄 Converting CLI to Web UI: {cli_tool_path}")

        analysis = await self.gui_gen.analyze_cli_tool(cli_tool_path)
        react_ui = await self.gui_gen.generate_react_ui(
            tool_name=analysis['tool_name'],
            parameters=analysis['parameters']
        )

        output_path = output_dir / f"{analysis['tool_name']}_ui.jsx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(react_ui)

        logger.info(f"✅ Web UI created: {output_path}")
        return True

    async def cli_to_desktop_app(
        self,
        cli_tool_path: Path,
        output_dir: Path
    ) -> bool:
        """Convert CLI tool to desktop app"""
        logger.info(f"🔄 Converting CLI to Desktop App: {cli_tool_path}")

        analysis = await self.gui_gen.analyze_cli_tool(cli_tool_path)
        tauri_app = await self.gui_gen.generate_tauri_desktop_app(
            tool_name=analysis['tool_name'],
            parameters=analysis['parameters']
        )

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        (output_dir_path / "tauri.conf.json").write_text(tauri_app['tauri_config'])
        (output_dir_path / "main.rs").write_text(tauri_app['main_rs'])

        logger.info(f"✅ Desktop app created in {output_dir}")
        return True


_gui_engine: Optional[GUIAutomationEngine] = None


def get_gui_automation_engine() -> GUIAutomationEngine:
    """Get or create singleton GUI engine"""
    global _gui_engine
    if _gui_engine is None:
        _gui_engine = GUIAutomationEngine()
    return _gui_engine
