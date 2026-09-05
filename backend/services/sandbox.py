"""
Malware Sandbox Module
Isolated environment for malware analysis with behavioral monitoring
"""

import os
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import tempfile
import shutil


class MalwareSandbox:
    """
    Provides isolated sandbox environment for malware analysis
    Monitors file behavior, network activity, and system changes
    """
    
    def __init__(self, isolate: bool = True, network_monitor: bool = True,
                 timeout: int = 300):
        self.isolate = isolate
        self.network_monitor = network_monitor
        self.timeout = timeout
        self.sandbox_dir: Optional[Path] = None
        self.analysis_log: List[Dict] = []
        self.processes: List[int] = []
    
    def analyze(self, sample_path: str) -> Dict[str, Any]:
        """
        Analyze a malware sample in sandbox
        
        Args:
            sample_path: Path to malware sample
            
        Returns:
            Analysis results dictionary
        """
        sample = Path(sample_path)
        if not sample.exists():
            raise FileNotFoundError(f"Sample not found: {sample_path}")
        
        # Create sandbox environment
        self._setup_sandbox()
        
        try:
            # Calculate hashes
            result = {
                'filename': sample.name,
                'md5': self._hash_file(sample, 'md5'),
                'sha256': self._hash_file(sample, 'sha256'),
                'file_type': self._detect_file_type(sample),
                'file_size': sample.stat().st_size,
                'analysis_time': datetime.now().isoformat(),
                'behaviors': [],
                'network_activity': [],
                'files_created': [],
                'registry_changes': [],  # Windows only
                'threat_score': 0
            }
            
            # Static analysis
            result['strings'] = self._extract_strings(sample)
            result['imports'] = self._analyze_imports(sample)
            
            # Dynamic analysis (if safe to execute)
            if self._is_safe_to_execute(sample):
                dynamic_results = self._execute_and_monitor(sample)
                result['behaviors'].extend(dynamic_results.get('behaviors', []))
                result['network_activity'].extend(dynamic_results.get('network', []))
                result['files_created'].extend(dynamic_results.get('files', []))
                
                # Calculate threat score
                result['threat_score'] = self._calculate_threat_score(result)
            
            # Log analysis
            self.analysis_log.append({
                'timestamp': datetime.now().isoformat(),
                'sample': sample.name,
                'sha256': result['sha256'],
                'threat_score': result['threat_score']
            })
            
            return result
            
        finally:
            # Cleanup handled by explicit cleanup() call
            pass
    
    def _setup_sandbox(self):
        """Setup isolated sandbox environment"""
        self.sandbox_dir = Path(tempfile.mkdtemp(prefix='kg_sandbox_'))
        
        # Create monitoring directories
        (self.sandbox_dir / 'output').mkdir()
        (self.sandbox_dir / 'logs').mkdir()
        (self.sandbox_dir / 'captures').mkdir()
        
        # Start network monitoring if enabled
        if self.network_monitor:
            self._start_network_capture()
    
    def _hash_file(self, path: Path, algorithm: str) -> str:
        """Calculate file hash"""
        hash_func = getattr(hashlib, algorithm)()
        
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def _detect_file_type(self, path: Path) -> str:
        """Detect file type using magic bytes"""
        try:
            result = subprocess.run(
                ['file', '-b', str(path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except:
            return 'Unknown'
    
    def _extract_strings(self, path: Path, min_length: int = 6) -> List[str]:
        """Extract printable strings from file"""
        try:
            result = subprocess.run(
                ['strings', '-n', str(min_length), str(path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            strings = result.stdout.strip().split('\n')
            return [s for s in strings if len(s) >= min_length][:100]  # Limit to 100
        except:
            return []
    
    def _analyze_imports(self, path: Path) -> Dict[str, List[str]]:
        """Analyze imported functions (for PE/ELF files)"""
        imports = {'functions': [], 'libraries': []}
        
        try:
            # Try objdump for ELF/PE analysis
            result = subprocess.run(
                ['objdump', '-T', str(path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if '@' in line:
                        parts = line.split()
                        if len(parts) > 5:
                            imports['functions'].append(parts[-1].split('@')[0])
        except:
            pass
        
        return imports
    
    def _is_safe_to_execute(self, path: Path) -> bool:
        """Determine if sample is safe to execute in sandbox"""
        # In production, implement proper safety checks
        # For now, only execute known safe test files
        return False
    
    def _execute_and_monitor(self, path: Path) -> Dict[str, Any]:
        """Execute sample and monitor behavior"""
        results = {
            'behaviors': [],
            'network': [],
            'files': []
        }
        
        # This would run the sample in a VM or container
        # and monitor its behavior
        
        return results
    
    def _start_network_capture(self):
        """Start network traffic capture"""
        # Would start tcpdump or similar in real implementation
        pass
    
    def _stop_network_capture(self) -> List[Dict]:
        """Stop network capture and return results"""
        # Would parse pcap and return network activity
        return []
    
    def _calculate_threat_score(self, result: Dict) -> int:
        """Calculate threat score based on analysis"""
        score = 0
        
        # Suspicious imports
        suspicious_imports = [
            'VirtualAlloc', 'WriteProcessMemory', 'CreateRemoteThread',
            'InternetOpen', 'URLDownloadToFile', 'WinExec', 'ShellExecute'
        ]
        
        for imp in result.get('imports', {}).get('functions', []):
            if any(sus in imp for sus in suspicious_imports):
                score += 10
        
        # Suspicious strings
        suspicious_strings = [
            'cmd.exe', 'powershell', 'regsvr32', 'mimikatz',
            'password', 'credential', 'bitcoin'
        ]
        
        for string in result.get('strings', []):
            if any(sus.lower() in string.lower() for sus in suspicious_strings):
                score += 5
        
        # Network activity
        score += len(result.get('network_activity', [])) * 15
        
        # Cap at 100
        return min(score, 100)
    
    def cleanup(self):
        """Cleanup sandbox environment"""
        if self.sandbox_dir and self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir, ignore_errors=True)
        
        self.sandbox_dir = None
        
        # Kill any remaining processes
        for pid in self.processes:
            try:
                os.kill(pid, 9)
            except:
                pass
        
        self.processes = []
    
    def get_analysis_history(self) -> List[Dict]:
        """Get analysis history"""
        return self.analysis_log
    
    def save_report(self, output_path: str, results: Dict):
        """Save analysis report to file"""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
