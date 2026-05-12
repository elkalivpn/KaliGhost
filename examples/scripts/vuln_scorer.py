#!/usr/bin/env python3
"""Puntuador automático de vulnerabilidades (CVSS-like)"""

import json

CVSS_BASE = {
    'AV:N': 0.85, 'AV:A': 0.62, 'AV:L': 0.55, 'AV:P': 0.2,
    'AC:L': 0.77, 'AC:H': 0.44,
    'PR:N': 0.85, 'PR:L': 0.62, 'PR:H': 0.27,
    'UI:N': 0.85, 'UI:R': 0.62,
    'S:U': 0.0, 'S:C': 1.0,
    'C:N': 0.0, 'C:L': 0.22, 'C:H': 0.56,
    'I:N': 0.0, 'I:L': 0.22, 'I:H': 0.56,
    'A:N': 0.0, 'A:L': 0.22, 'A:H': 0.56
}

def score_cvss(metrics):
    """Calcula CVSS v3.1 base score"""
    # Simplified – real CVSS is more complex
    impact_sub = 1 - ((1 - CVSS_BASE[metrics['C']]) * (1 - CVSS_BASE[metrics['I']]) * (1 - CVSS_BASE[metrics['A']]))
    impact = 6.42 * impact_sub
    if metrics['S'] == 'C':
        impact = min(impact + 1.764, 10)
    
    exploit = 8.22 * CVSS_BASE[metrics['AV']] * CVSS_BASE[metrics['AC']] * CVSS_BASE[metrics['PR']] * CVSS_BASE[metrics['UI']]
    
    if metrics['S'] == 'U':
        scope = 1
    else:
        scope = 1.08
    
    base = min((impact + exploit) * scope, 10)
    return round(base, 1)

if __name__ == '__main__':
    # Ejemplo: CVE-2024-XXXX
    vuln_metrics = {
        'AV': 'N',  # Network
        'AC': 'L',  # Low
        'PR': 'N',  # None
        'UI': 'N',  # None
        'S': 'U',   # Unchanged
        'C': 'H',   # High confidentiality
        'I': 'H',   # High integrity
        'A': 'H'    # High availability
    }
    score = score_cvss(vuln_metrics)
    print(f"CVSS Score: {score}/10.0")
    if score >= 9.0:
        print("🔴 CRITICAL")
    elif score >= 7.0:
        print("🟠 HIGH")
    elif score >= 4.0:
        print("🟡 MEDIUM")
    else:
        print("🟢 LOW")