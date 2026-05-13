# Security Policy

## 📅 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v1.x.x  | ✅ Active support  |
| v0.9.x  | ⚠️ Security only   |
| < v0.9  | ❌ Unsupported     |

## 🐛 Reporting a Vulnerability

**Por favor, reporta vulnerabilidades de manera privada.**

### Métodos de Reporte (orden de preferencia)

1. **Email encriptado (recomendado):**
   ```
   security@kalighost.dev
   PGP Key: https://kalighost.dev/security.asc
   Fingerprint: ABCD 1234 EFGH 5678 IJKL 9012 MNOP 3456 QRST 7890
   ```

2. **GitHub Private Advisory:**
   - Ve a [Security Advisories](https://github.com/elkalivpn/KaliGhost/security/advisories)
   - Clica "New draft security advisory"
   - Marca como "Private" hasta patch disponible

3. **Telegram (solo emergencias críticas):**
   - @elkalivpn (solo si no respondemos email en 48h)

### ⏱️ Timeline de Respuesta

| Severidad | Meta inicial | Meta resolución |
|-----------|--------------|-----------------|
| **CRITICAL** (RCE, data breach) | 4h | 48h |
| **HIGH** (auth bypass, privilege escalation) | 24h | 7 días |
| **MEDIUM** (XSS, CSRF, info disclosure) | 48h | 30 días |
| **LOW** (security headers, best practices) | 7 días | Sin fecha fija |

### 📋 Qué incluir en el reporte

- Versión afectada (git commit SHA o tag)
- Pasos exactos para reproducir
- Impacto real (qué puede hacer un atacante)
- Si tienes un PoC (proof-of-concept), inclúyelo
- Si es privado/zero-day, NO lo publiques hasta patch

### 🔐 No reportes públicamente

- **NO** abras GitHub Issue para vulnerabilities
- **NO** twittees/twitch sobre bugs de security
- **NO** shared en Discord/Telegram canales públicos

Esperamos 90 días desde reporte privado antes de disclosure público coordinated.

---

## 🏆 Hall of Fame

Agradecemos a investigadores responsables que han reportado vulnerabilities:

- @investigator1 – CVE-2024-XXXX (reportado 2026-01-15, parcheado v1.0.1)
- @pentester2 – Authentication bypass (reportado 2025-12-01, parcheado v0.9.2)

*(Se añade nombre/alias tras resolución y publicación del advisory)*

---

## 🔍 Auditorías Externas

KaliGhost ha pasado auditorías de:

- [ ] [Owasp ASVS](https://owasp.org/www-project-application-security-vocabulary/) – Pendiente
- [ ] [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/) – Pendiente
- [ ] Pentest interno (Q2 2026) – En progreso

Reportes públicos disponibles en `docs/audits/` tras finalización.

---

## 📦 Dependencias Seguras

Usamos:
- **Dependabot** – Para dependencias en requirements.txt, package.json
- **Snyk** – Escaneo de vulnerabilidades en imágenes Docker
- **Trivy** – Scaneo de contenedores en CI/CD

Actualizamos parches de seguridad dentro de 7 días de release upstream.

---

## 🔒 Hardening Recomendado

Para entornos de producción:

```yaml
# YrYs-Agent/yrays_config.yaml
security:
  audit_logging: true          # Logs inmutable
  network_policy: deny_all     # Política de red restrictiva
  secrets_vault: "hashicorp"   # Usar Vault para secrets
  runtime_sandbox: "firejail"  # Sandbox adicional
  credential_rotation: "7d"    # Rotar claves cada 7 días
```

---

## 💼 Bug Bounty (próximamente)

Estamos preparando un programa de bug bounty en **HackerOne** para:

- Vulnerabilidades críticas: hasta **$10,000 USD**
- Vulnerabilidades altas: hasta **$2,500 USD**
- Vulnerabilidades medias: hasta **$500 USD**

*Disponible para v1.1.0+*

---

**📧 Contacto seguridad:** `security@kalighost.dev` (PGP encrypted preferred)

*Por favor, no reportes vulnerabilities en GitHub Issues públicas.*