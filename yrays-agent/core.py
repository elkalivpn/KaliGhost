"""
Yrays-Agent Core Module - Enhanced with RAG and Autonomous Capabilities
Local LLM integration for security research tasks
Supports multiple backends: llama.cpp, ollama, vllm
Integrated with CVE intelligence and autonomous red team capabilities
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List, Generator, Tuple
import json
import time


class YraysAgent:
    """
    Uncensored AI Agent for Security Research
    
    Provides local LLM capabilities specialized for:
    - Vulnerability analysis
    - Exploit development assistance
    - Malware analysis
    - Code review for security issues
    - Bug bounty hunting
    - Purple team operations
    - Autonomous red team operations
    """
    
    def __init__(self, model: str = 'uncensored-v1', gpu: bool = False,
                 quantize: str = 'q4_k_m', enable_rag: bool = True):
        self.model_name = model
        self.use_gpu = gpu
        self.quantization = quantize
        self.loaded = False
        self.model_path: Optional[Path] = None
        self.engine = None
        self.enable_rag = enable_rag
        self.cve_engine = None
        
        # Autonomous mode settings
        self.autonomous_mode = False
        self.autonomous_agents: Dict[str, dict] = {}
        
        # Model configurations
        self.models = {
            'uncensored-v1': {
                'description': 'Security-focused uncensored model',
                'params': '7B',
                'context': 4096
            },
            'security-expert': {
                'description': 'Expert security consultant model',
                'params': '13B',
                'context': 8192
            },
            'malware-analyst': {
                'description': 'Specialized in malware analysis',
                'params': '7B',
                'context': 4096
            },
            'redteam-auto': {
                'description': 'Autonomous red team operations',
                'params': '13B',
                'context': 16384
            },
            'exploit-dev': {
                'description': 'Exploit development specialist',
                'params': '7B',
                'context': 8192
            }
        }
        
        # System prompts for different modes
        self.system_prompts = {
            'default': '''You are Yrays, an uncensored AI security research assistant.
You provide detailed, technical information for legitimate security research.
Always include appropriate disclaimers about ethical use.
Focus on educational and defensive security applications.''',
            
            'exploit-dev': '''You are an exploit development assistant.
Help with understanding vulnerabilities, writing PoCs, and developing exploits.
Always emphasize responsible disclosure and legal considerations.''',
            
            'malware-analysis': '''You are a malware analysis expert.
Assist with reverse engineering, behavioral analysis, and IOC extraction.
Focus on defensive applications and threat intelligence.''',
            
            'bug-bounty': '''You are a bug bounty hunting assistant.
Help identify vulnerabilities, craft payloads, and write reports.
Emphasize responsible disclosure and scope compliance.''',
            
            'redteam-auto': '''You are an autonomous red team operator.
Plan and execute authorized penetration testing operations.
Adapt tactics based on findings. Document all actions.
Stay within authorized scope at all times.''',
            
            'code-obfuscation': '''You are a code obfuscation specialist.
Help protect security tools from detection through advanced obfuscation.
Techniques include: encryption, packing, anti-analysis, polymorphism.
Always for legitimate security research purposes.'''
        }
    
    def load(self) -> bool:
        """
        Load the AI model
        
        Returns:
            Success status
        """
        try:
            # Check for model file
            model_dir = Path(__file__).parent / 'models'
            self.model_path = model_dir / f'{self.model_name}.gguf'
            
            if not self.model_path.exists():
                # Try to find any .gguf file
                gguf_files = list(model_dir.glob('*.gguf'))
                if gguf_files:
                    self.model_path = gguf_files[0]
                else:
                    print(f"[*] Model file not found, using mock mode")
                    self.loaded = True  # Mock mode
                    return True
            
            # Initialize backend (llama-cpp-python recommended)
            try:
                from llama_cpp import Llama
                
                self.engine = Llama(
                    model_path=str(self.model_path),
                    n_ctx=self.models.get(self.model_name, {}).get('context', 4096),
                    n_gpu_layers=-1 if self.use_gpu else 0,
                    verbose=False
                )
                
                self.loaded = True
                print(f"[+] Model loaded: {self.model_name}")
                return True
                
            except ImportError:
                print("[!] llama-cpp-python not installed, using mock mode")
                self.loaded = True
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to load model: {str(e)}")
            return False
    
    def unload(self):
        """Unload the model"""
        if self.engine:
            del self.engine
            self.engine = None
        self.loaded = False
        print("[*] Model unloaded")
    
    def query(self, prompt: str, context: Optional[Dict] = None,
              system_prompt: str = None, max_tokens: int = 2048,
              temperature: float = 0.7) -> str:
        """
        Query the AI agent
        
        Args:
            prompt: User prompt
            context: Additional context dictionary
            system_prompt: Override system prompt
            max_tokens: Maximum response tokens
            temperature: Response creativity (0.0-1.0)
            
        Returns:
            AI response string
        """
        if not self.loaded:
            raise RuntimeError("Model not loaded")
        
        # Build full prompt
        sys_prompt = system_prompt or self.system_prompts['default']
        
        if context:
            ctx_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            full_prompt = f"{sys_prompt}\n\nContext:\n{ctx_str}\n\nUser: {prompt}"
        else:
            full_prompt = f"{sys_prompt}\n\nUser: {prompt}"
        
        # Generate response
        if self.engine:
            response = self.engine(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=['User:', '\n\n']
            )
            return response['choices'][0]['text'].strip()
        else:
            # Mock response for when no model is available
            return self._mock_response(prompt)
    
    def query_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """
        Query with streaming response
        
        Yields:
            Response chunks
        """
        if not self.loaded:
            raise RuntimeError("Model not loaded")
        
        if self.engine:
            for token in self.engine(
                prompt,
                max_tokens=kwargs.get('max_tokens', 2048),
                temperature=kwargs.get('temperature', 0.7),
                stream=True
            ):
                yield token['choices'][0]['text']
        else:
            yield self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """Generate mock response when model unavailable"""
        return f"""[Mock Response - No Model Loaded]

Your query: {prompt[:100]}...

To enable full AI capabilities:
1. Install llama-cpp-python: pip install llama-cpp-python
2. Download a model to yrays-agent/models/
3. Restart KaliGhost IDE

Available models:
- uncensored-v1: General security research
- security-expert: Advanced security consulting  
- malware-analyst: Malware analysis specialist

For now, I can only provide this placeholder response."""
    
    def analyze_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """
        Analyze code for security vulnerabilities
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Analysis results
        """
        prompt = f"""Analyze this {language} code for security vulnerabilities:

```{language}
{code}
```

Provide:
1. Identified vulnerabilities (CWE IDs if applicable)
2. Severity ratings (Critical/High/Medium/Low)
3. Remediation recommendations
4. Secure code examples"""
        
        response = self.query(prompt, system_prompt=self.system_prompts['default'])
        
        return {
            'code_snippet': code[:100],
            'language': language,
            'analysis': response
        }
    
    def generate_exploit_poc(self, vulnerability: str, target: str = None) -> str:
        """
        Generate proof-of-concept exploit code
        
        Args:
            vulnerability: Vulnerability description
            target: Target system/software (optional)
            
        Returns:
            PoC code/explanation
        """
        prompt = f"""Generate a proof-of-concept exploit for:
{vulnerability}

Target: {target or 'Generic'}

Include:
1. Vulnerability explanation
2. Prerequisites
3. Step-by-step exploitation
4. PoC code (Python/Bash)
5. Mitigation recommendations

DISCLAIMER: For educational purposes only. Use responsibly."""
        
        return self.query(prompt, system_prompt=self.system_prompts['exploit-dev'])
    
    def analyze_malware(self, sample_info: Dict) -> Dict[str, Any]:
        """
        Analyze malware sample information
        
        Args:
            sample_info: Sample metadata (hashes, strings, behaviors)
            
        Returns:
            Analysis report
        """
        prompt = f"""Analyze this malware sample:

Hashes:
- MD5: {sample_info.get('md5', 'N/A')}
- SHA256: {sample_info.get('sha256', 'N/A')}

Strings found: {', '.join(sample_info.get('strings', [])[:10])}

Behaviors observed: {', '.join(sample_info.get('behaviors', []))}

Provide:
1. Malware family identification (if possible)
2. Capabilities assessment
3. IOCs for detection
4. Mitigation recommendations"""
        
        response = self.query(prompt, system_prompt=self.system_prompts['malware-analysis'])
        
        return {
            'sample_hash': sample_info.get('sha256'),
            'analysis': response,
            'confidence': 'automated'
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'loaded': self.loaded,
            'model': self.model_name,
            'model_path': str(self.model_path) if self.model_path else None,
            'gpu_enabled': self.use_gpu,
            'quantization': self.quantization,
            'available_models': list(self.models.keys()),
            'rag_enabled': self.enable_rag,
            'autonomous_mode': self.autonomous_mode
        }
    
    def query_with_rag(self, prompt: str, context_type: str = 'cve',
                       **kwargs) -> str:
        """
        Query with RAG (Retrieval-Augmented Generation) context.
        
        Args:
            prompt: User query
            context_type: Type of context to retrieve ('cve', 'exploit', etc.)
            **kwargs: Additional query parameters
            
        Returns:
            Enhanced response with retrieved context
        """
        if not self.enable_rag:
            return self.query(prompt, **kwargs)
        
        # Initialize CVE engine if needed
        if self.cve_engine is None and context_type == 'cve':
            try:
                from backend.services.cve_intelligence import get_cve_engine
                self.cve_engine = get_cve_engine()
            except ImportError:
                pass
        
        # Retrieve relevant context
        rag_context = ""
        if context_type == 'cve' and self.cve_engine:
            rag_context = self.cve_engine.generate_rag_context(prompt)
        
        # Build enhanced prompt with context
        if rag_context:
            enhanced_prompt = f"""Context Information:
{rag_context}

User Query: {prompt}

Please use the context above to provide a more informed response."""
            return self.query(enhanced_prompt, **kwargs)
        
        return self.query(prompt, **kwargs)
    
    def enable_autonomous_mode(self, agent_configs: List[Dict] = None) -> bool:
        """
        Enable autonomous red team mode with specialized agents.
        
        Args:
            agent_configs: List of agent configurations
            
        Returns:
            Success status
        """
        try:
            self.autonomous_mode = True
            
            # Default agent configurations
            default_agents = [
                {
                    'name': 'recon_agent',
                    'role': 'Reconnaissance specialist',
                    'tasks': ['port_scan', 'service_enum', 'subdomain_discovery']
                },
                {
                    'name': 'exploit_agent',
                    'role': 'Exploitation specialist',
                    'tasks': ['vuln_matching', 'poc_generation', 'exploitation']
                },
                {
                    'name': 'post_exploit_agent',
                    'role': 'Post-exploitation specialist',
                    'tasks': ['privilege_escalation', 'lateral_movement', 'data_exfil']
                },
                {
                    'name': 'stealth_agent',
                    'role': 'Stealth and evasion specialist',
                    'tasks': ['opsec_check', 'log_cleanup', 'detection_evasion']
                }
            ]
            
            self.autonomous_agents = {
                agent['name']: agent 
                for agent in (agent_configs or default_agents)
            }
            
            print(f"[+] Autonomous mode enabled with {len(self.autonomous_agents)} agents")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to enable autonomous mode: {e}")
            return False
    
    def run_autonomous_operation(self, target: str, scope: Dict,
                                max_iterations: int = 10) -> Dict[str, Any]:
        """
        Run an autonomous red team operation.
        
        Args:
            target: Target specification
            scope: Authorized scope definition
            max_iterations: Maximum operation iterations
            
        Returns:
            Operation results and findings
        """
        if not self.autonomous_mode:
            raise RuntimeError("Autonomous mode not enabled")
        
        results = {
            'target': target,
            'scope': scope,
            'findings': [],
            'actions_taken': [],
            'iterations': 0
        }
        
        # Phase 1: Reconnaissance
        recon_prompt = f"""Plan reconnaissance for target: {target}
Authorized scope: {json.dumps(scope)}

Generate a reconnaissance plan including:
1. Passive information gathering
2. Active scanning approach
3. Service enumeration strategy
4. Initial attack surface mapping"""
        
        recon_plan = self.query(recon_prompt, system_prompt=self.system_prompts['redteam-auto'])
        results['findings'].append({'phase': 'recon', 'plan': recon_plan})
        results['actions_taken'].append('reconnaissance_planning')
        
        # Phase 2: Vulnerability Analysis
        vuln_prompt = f"""Based on reconnaissance, identify potential vulnerabilities for: {target}

Prioritize by:
1. Likelihood of success
2. Impact level
3. Detection risk
4. Available exploits"""
        
        vuln_analysis = self.query(vuln_prompt, system_prompt=self.system_prompts['redteam-auto'])
        results['findings'].append({'phase': 'analysis', 'vulnerabilities': vuln_analysis})
        results['actions_taken'].append('vulnerability_analysis')
        
        # Phase 3: Exploitation Planning
        exploit_prompt = f"""Develop exploitation strategy for identified vulnerabilities.

For each vulnerability:
1. Required tools/resources
2. Step-by-step exploitation procedure
3. Expected outcomes
4. Fallback options
5. OPSEC considerations"""
        
        exploit_plan = self.query(exploit_prompt, system_prompt=self.system_prompts['redteam-auto'])
        results['findings'].append({'phase': 'exploitation', 'plan': exploit_plan})
        results['actions_taken'].append('exploitation_planning')
        
        results['iterations'] = 3
        results['status'] = 'planning_complete'
        results['recommendation'] = 'Review generated plans before execution'
        
        return results
    
    def obfuscate_code(self, code: str, technique: str = 'polymorphic',
                      target_av: str = None) -> str:
        """
        Generate obfuscated version of security tool code.
        
        Args:
            code: Original source code
            technique: Obfuscation technique
            target_av: Specific AV to evade (optional)
            
        Returns:
            Obfuscated code
        """
        prompt = f"""Obfuscate this code using {technique} technique:

```python
{code}
```

{'Target AV: ' + target_av if target_av else ''}

Apply:
1. String encryption
2. Control flow obfuscation
3. Anti-analysis techniques
4. Packing/encoding

Provide the complete obfuscated version ready for deployment."""
        
        return self.query(prompt, system_prompt=self.system_prompts['code-obfuscation'])
    
    def generate_purple_team_report(self, red_findings: Dict,
                                   blue_detections: Dict) -> str:
        """
        Generate comprehensive purple team report.
        
        Args:
            red_findings: Red team findings and successes
            blue_detections: Blue team detections and responses
            
        Returns:
            Comprehensive report
        """
        prompt = f"""Generate a purple team assessment report.

Red Team Findings:
{json.dumps(red_findings, indent=2)}

Blue Team Detections:
{json.dumps(blue_detections, indent=2)}

Report should include:
1. Executive summary
2. Attack chain analysis
3. Detection gaps identified
4. Response effectiveness evaluation
5. Prioritized remediation recommendations
6. Detection engineering suggestions
7. Lessons learned"""
        
        return self.query(prompt, system_prompt=self.system_prompts['default'])
