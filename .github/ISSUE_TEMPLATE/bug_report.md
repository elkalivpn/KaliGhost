---
name: 🐛 Bug Report
about: Reporta un problema en KaliGhost
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''

---

## 🐛 Descripción del Bug

Descripción clara y concisa del problema.

## 🔄 Pasos para Reproducir

1. Ir a '...'
2. Hacer clic en '...'
3. Ver error

## ✅ Comportamiento Esperado

Qué esperabas que sucediera.

## 📸 Capturas de Pantalla

Si aplica, añade screenshots aquí.

## 🖥️ Entorno

- **OS:** [e.g. macOS 14.2, Ubuntu 22.04]
- **Docker:** [e.g. Docker Desktop 4.21]
- **Versión KaliGhost:** [e.g. v1.0.0]
- **Arquitectura:** [e.g. Apple Silicon M2, Intel x64]

## 📋 Logs

```bash
# Output de docker logs
docker logs kali-ghost

# Logs del agente
docker exec -it kali-ghost tail -f /root/KaliGhost/YrYs-Agent/logs/agent.log
```

Pegar logs relevantes aquí (usa ```log``` blocks).

## 🔍 Debug Info

```bash
# Ejecutar y pegar output:
docker exec -it kali-ghost uname -a
docker exec -it kali-ghost cat /etc/os-release
```

## 📌 Additional Context

Cualquier otra información relevante.

---

**💡 Tip:** Antes de reportar, revisa:
- [ ] El bug no está ya reportado (busca en Issues)
- [ ] Has probado en modo `--debug`
- [ ] Has revisado `docs/TROUBLESHOOTING.md`