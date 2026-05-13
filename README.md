# KaliGhost - Sistema Operativo de Pentesting Autónomo

![KaliGhost Logo](assets/logo.png)

KaliGhost es un sistema operativo de bolsillo diseñado para desarrolladores y pentesters. Vive en un USB, VM o contenedor y ofrece IA autónoma con total privacidad.

## Características

- ✅ 100% local - No requiere internet ni APIs
- ✅ IA autónoma con jailbreaks integrados
- ✅ Funciona desde USB en modo efímero
- ✅ Mínimo footprint, máximo poder
- ✅ Altamente configurable para cualquier entorno
- ✅ Protección avanzada con Proton

## Arquitectura

```bash
kali-ghost/
├── src/
│   ├── agent/           # Código del agente YrYs
│   └── docker/          # Configuración de contenedor
├── assets/              # Recursos estáticos
├── docs/                # Documentación
└── vendor/              # Dependencias precompiladas
```

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/elkalivpn/KaliGhost.git
```

2. Configura tus credenciales:
```bash
cp .env.example .env
# Edita .env con tus claves
```

3. Inicia el sistema:
```bash
./src/docker/start_docker.sh build
./src/docker/start_docker.sh start
```

## Contribuir

1. Forkea el repositorio
2. Crea una rama (`git checkout -b feat/feature-name`)
3. Haz commit (`git commit -am 'Añade feature x'`)
4. Push (`git push origin feat/feature-name`)
5. Crea un Pull Request

## Licencia

MIT © 2026 theKalivpn