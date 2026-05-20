# Skill: safe_web_analyzer
# Descripción: Herramientas seguras de análisis de tecnologías web
# Generado automáticamente por YrYs-Agent


def analyze_web_technologies(whatweb_output):
    """Analiza los resultados de whatweb"""
    if not whatweb_output:
        return "❌ No hay resultados para analizar"
    
    lines = whatweb_output.split("\n")
    technologies = []
    
    for line in lines:
        if line.strip():
            # Extraer tecnologías del formato de whatweb
            parts = line.split(" ")
            if len(parts) > 1:
                url = parts[0]
                techs = [part.strip("[]") for part in parts[1:] if part.startswith("[") and part.endswith("]")]
                if techs:
                    technologies.append(f"📱 {url}: {', '.join(techs)}")
    
    if technologies:
        return "\n".join(technologies)
    else:
        return "🔍 No se detectaron tecnologías específicas"

def check_http_headers(headers_dict):
    """Analiza headers HTTP para seguridad"""
    security_issues = []
    
    # Verificar headers de seguridad
    if "x-frame-options" not in headers_dict:
        security_issues.append("⚠️ Falta X-Frame-Options (posible riesgo de clickjacking)")
    
    if "x-content-type-options" not in headers_dict:
        security_issues.append("⚠️ Falta X-Content-Type-Options (posible riesgo de MIME-sniffing)")
    
    if "x-xss-protection" not in headers_dict:
        security_issues.append("⚠️ Falta X-XSS-Protection (posible riesgo de XSS)")
    
    if "strict-transport-security" not in headers_dict:
        security_issues.append("⚠️ Falta Strict-Transport-Security (posible riesgo de downgrade attacks)")
    
    if "content-security-policy" not in headers_dict:
        security_issues.append("⚠️ Falta Content-Security-Policy (posible riesgo de XSS)")
    
    if security_issues:
        return "\n".join(security_issues)
    else:
        return "✅ Todos los headers de seguridad presentes"
