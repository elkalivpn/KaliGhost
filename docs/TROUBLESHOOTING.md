# Troubleshooting – KaliGhost

> 💡 Primero, revisa `docs/INSTALLATION.md` si es problema de instalación.

## 🐛 Problemas Comunes

### Docker no inicia en macOS

**Síntoma:**
```bash
$ docker ps
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

**Soluciones:**

1. **Inicia Docker Desktop manualmente:**
   ```bash
   open -a Docker
   # Espera a que el icono deje de girar (30-60s)
   docker ps  # Ya debería funcionar
   ```

2. **Si persiste, reinicia:**
   ```bash
   killall Docker
   open -a Docker
   ```

3. **Permisos de socket:**
   ```bash
   sudo chown $USER:staff /var/run/docker.sock 2>/dev/null || true
   ```

---

### Puertos 22/80/443 ya en uso

**Síntoma:**
```bash
Error starting userland proxy: listen tcp 0.0.0.0:22: bind: address already in use
```

**Solución A – Mata proceso conflictivo:**
```bash
# Ver qué usa el puerto
lsof -i :22
lsof -i :80
lsof -i :443

# Mata proceso
kill -9 <PID>
```

**Solución B – Cambia puertos en docker-compose:**
```yaml
# En work/docker-compose.yml
ports:
  - "2222:22"   # SSH en 2222
  - "8080:80"   # HTTP en 8080
  - "8443:443"  # HTTPS en 8443
```

---

### Agente YrYs no inicia (ModuleNotFoundError)

**Síntoma:**
```bash
$ python3 agent.py
ModuleNotFoundError: No module named 'boto3'
```

**Solución:**
```bash
cd YrYs-Agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Si no hay `requirements.txt`, crea uno:
```txt
boto3>=1.34.0
pyyaml>=6.0
requests>=2.31.0
```

---

### AWS API retorna AccessDenied

**Síntoma:**
```python
botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the AssumeRole operation
```

**Verifica:**

1. **Rol IAM correcto:**
   ```bash
   aws sts get-caller-identity
   aws sts assume-role --role-arn "arn:aws:iam::233896339713:role/service-role/DevOpsAgentRole-WebappAdmin-vt2y0ajh" --role-session-name test
   ```

2. **Credenciales locales:**
   ```bash
   cat ~/.aws/credentials
   # Debe tener perfil con acceso al rol
   ```

3. **Policy del rol:**
   El rol necesita al menos:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "sts:AssumeRole",
         "Resource": "arn:aws:iam::233896339713:role/service-role/DevOpsAgentRole-WebappAdmin-vt2y0ajh"
       }
     ]
   }
   ```

---

### Web no carga (HTML 404 en local)

**Síntoma:** Abres `web_monetizacion/index.html` en navegador y falla.

**Causas comunes:**

1. **Ruta relativa incorrecta** – Abre desde dentro de `web_monetizacion/`:
   ```bash
   cd ~/KaliGhost/web_monetizacion
   open index.html  # macOS
   # o
   xdg-open index.html  # Linux
   ```

2. **Servidor local necesario** (algunos JS features):
   ```bash
   cd ~/KaliGhost/web_monetizacion
   python3 -m http.server 8080
   # http://localhost:8080
   ```

---

### Agent falla en modo AUTO (se queda stuck)

**Síntoma:** Agente ejecuta pero nunca completa tarea.

**Debug:**

1. **Log level debug:**
   ```bash
   python3 agent.py --auto --debug --log-level DEBUG
   ```

2. **Verificar configuración:**
   ```bash
   cat YrYs-Agent/yrays_config.yaml | grep -A 5 "mode:"
   # Debe ser "AUTO"
   ```

3. **Test de herramientas:**
   ```bash
   python3 agent.py --test-tools  # Verifica todas las tools
   ```

4. **Self-healing loop check:**
   ```bash
   grep -r "self_healing" YrYs-Agent/
   # Debe estar enabled: true
   ```

---

### Boot.sh falla (Docker compose error)

**Símtoma:** `./boot.sh` termina con error.

**Verifica:**

1. **Docker Compose v2:**
   ```bash
   docker compose version  # Not "docker-compose" (v1)
   # Si tienes v1:
   brew upgrade docker-compose  # o instala v2
   ```

2. **Permisos de archivo:**
   ```bash
   ls -la boot/boot.sh
   # Debe tener -rwxr-xr-x (755)
   chmod +x boot/boot.sh
   ```

3. **Dockerfile no encontrado:**
   ```bash
   # El script genera docker-compose en work/
   cat work/docker-compose.yml
   # Si no existe, ejecuta boot.sh manualmente
   ```

---

### Memoria/CPU alta en contenedor

**Síntoma:** Docker consume mucha RAM/CPU.

**Soluciones:**

1. **Limitar recursos Docker Desktop:**
   - Docker Desktop → Settings → Resources
   - CPUs: 2-4 (no todos)
   - Memory: 4-8GB

2. **Limitar contenedor:**
   ```yaml
   # boot/boot.sh ajustado
   deploy:
     resources:
       limits:
         cpus: '2.0'
         memory: 4G
   ```

3. **Modo sleep del agente (si no está en uso):**
   ```yaml
   agent:
     sleep_interval: 300  # 5 min entre tareas
   ```

---

### Gumroad links no funcionan

**Síntoma:** Botones de compra redirigen a error 404.

**Causa:** Usas links placeholder (`tu-producto-starter`).

**Fix:**
1. Crea productos en Gumroad
2. Copia los links reales
3. Edita `web_monetizacion/index.html`:
   ```html
   <a href="TU_LINK_REAL_GUMROAD" ...>
   ```

---

### Git no打标签 correctamente

**Síntoma:** `git tag` no muestra versión esperada.

**Fix:**
```bash
# List tags
git tag -l

# Crear tag correctamente
git tag -a v1.0.0 -m "KaliGhost v1.0.0"

# Push tag específico
git push origin v1.0.0

# Verificar
git ls-remote --tags origin
```

---

## 🩺 Commands de Diagnóstico

### Check completo del sistema

```bash
cd ~/KaliGhost

echo "=== KaliGhost System Check ==="
echo ""

echo "1. Git status:"
git status --short

echo ""
echo "2. Docker:"
docker ps --filter "name=kali-ghost" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "3. Disk space:"
df -h ~ | tail -1

echo ""
echo "4. Agent health:"
docker exec -it kali-ghost bash -c "cd /root/KaliGhost/YrYs-Agent && python3 agent.py --health"

echo ""
echo "5. Network connectivity:"
docker exec -it kali-ghost ping -c 1 8.8.8.8 > /dev/null && echo "✅ OK" || echo "❌ FAIL"

echo ""
echo "=== Done ==="
```

---

## 📂 Logs Dónde Buscar

| Componente | Log location | Cómo ver |
|------------|--------------|----------|
| **Docker** | `docker logs kali-ghost` | `docker logs -f kali-ghost` (tiempo real) |
| **Agente YrYs** | `YrYs-Agent/logs/agent.log` | `tail -f YrYs-Agent/logs/agent.log` |
| **Boot script** | `~/KaliGhost/boot.log` | `cat boot.log` |
| **Docker daemon** | macOS: `~/Library/Containers/com.docker.docker/Data/log/vm/dockerd.log` | Abre Console.app → Docker |

---

## 🔄 Reset completo (nuke & pave)

Si todo falla y quieres empezar de cero:

```bash
cd ~/KaliGhost

# 1. Kill contenedor
docker rm -f kali-ghost 2>/dev/null || true

# 2. Eliminar volúmenes
docker volume rm kali-ghost_work 2>/dev/null || true

# 3. Eliminar imágenes
docker rmi kalilinux/kali-rolling:latest 2>/dev/null || true

# 4. Limpiar trabajo local
rm -rf work/ YrYs-Agent/logs/*

# 5. Reinstalar
./boot/boot.sh
```

---

## 🆘 ¿No encuentras solución?

1. **Busca en issues existentes:** https://github.com/elkalivpn/KaliGhost/issues
2. **Abre un issue** con:
   - Output de `diagnostic.sh` (script de arriba)
   - Versión exacta (`git rev-parse HEAD`)
   - OS info (`uname -a`)
3. **Telegram:** @elkalivpn (respuesta en 24h)
4. **Email:** support@kalighost.dev

---

**⚠️ Aún atascado?** Proporciona:
- Steps exactos para reproducir
- Logs completos (sin sanitizar –必要 para debug)
- Tu `yrays_config.yaml` (sin secrets)

We'll help.