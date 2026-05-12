#!/bin/bash

# KaliGhost Release Automation Script
# Usage: ./release.sh [major|minor|patch|vX.Y.Z]

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prereqs() {
    log_info "Verificando prerequisites..."
    
    if ! command -v git &> /dev/null; then
        log_error "git no está instalado"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        log_warn "docker no está instalado (opcional para release)"
    fi
    
    if ! command -v gh &> /dev/null; then
        log_warn "gh (GitHub CLI) no instalado – algunas funciones no estarán disponibles"
    fi
    
    # Verify we're in KaliGhost dir
    if [ ! -f "README.md" ] || ! grep -q "KaliGhost" README.md; then
        log_error "No estás en el directorio raíz de KaliGhost"
        exit 1
    fi
    
    log_success "Prerequisitos OK"
}

# Check for uncommitted changes
check_git_status() {
    log_info "Verificando estado de git..."
    
    if [ -n "$(git status --porcelain)" ]; then
        log_error "Hay cambios sin commit. Por favor commit o stash."
        git status
        exit 1
    fi
    
    log_success "Directorio limpio"
}

# Bump version
bump_version() {
    local current_tag
    current_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    
    log_info "Versión actual: $current_tag"
    
    case "$1" in
        major)
            # Increment major: v1.2.3 -> v2.0.0
            IFS='.' read -r major minor patch <<< "$(echo $current_tag | tr -d 'v')"
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            # Increment minor: v1.2.3 -> v1.3.0
            IFS='.' read -r major minor patch <<< "$(echo $current_tag | tr -d 'v')"
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            # Increment patch: v1.2.3 -> v1.2.4
            IFS='.' read -r major minor patch <<< "$(echo $current_tag | tr -d 'v')"
            patch=$((patch + 1))
            ;;
        v*)
            # Specific version provided
            NEW_VERSION="$1"
            ;;
        *)
            log_error "Uso: $0 [major|minor|patch|vX.Y.Z]"
            exit 1
            ;;
    esac
    
    if [ -z "$NEW_VERSION" ]; then
        NEW_VERSION="v${major}.${minor}.${patch}"
    fi
    
    log_info "Nueva versión: $NEW_VERSION"
}

# Update CHANGELOG
update_changelog() {
    log_info "Actualizando CHANGELOG.md..."
    
    # Get commits since last tag
    LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
    COMMITS=$(git log --pretty=format:"- %s" ${LAST_TAG}..HEAD)
    
    # Insert new section after [Unreleased]
    TEMP_FILE=$(mktemp)
    
    awk -v commits="$COMMITS" '
    /^## \[Unreleased\]/ {
        print;
        print "";
        print "## ['$NEW_VERSION'] - '$(date +%Y-%m-%d)'";
        print "";
        print commits;
        next;
    }
    { print }
    ' CHANGELOG.md > "$TEMP_FILE"
    
    mv "$TEMP_FILE" CHANGELOG.md
    
    log_success "CHANGELOG actualizado"
}

# Update README version badge
update_readme() {
    log_info "Actualizando versión en README..."
    
    # Update version badge
    sed -i '' "s/\*\*v[0-9]*\.[0-9]*\.[0-9]*\*\*/**$NEW_VERSION**/" README.md
    
    # Update date if present
    sed -i '' "s/Released: [0-9]*-[0-9]*-[0-9]*/Released: $(date +%Y-%m-%d)/" README.md
    
    log_success "README actualizado"
}

# Build Docker image
build_docker() {
    log_info "Construyendo imagen Docker..."
    
    docker build -t "kalighost:$NEW_VERSION" -t "kalighost:latest" .
    
    log_success "Imagen Docker construida"
}

# Run tests
run_tests() {
    log_info "Ejecutando tests pre-release..."
    
    if [ -d "tests" ]; then
        cd YrYs-Agent && python3 -m pytest tests/ -v || {
            log_error "Tests fallaron – abortando release"
            exit 1
        }
        cd ..
    else
        log_warn "Directorio tests/ no encontrado – omitiendo"
    fi
    
    log_success "Tests pasaron"
}

# Create git tag and push
git_release() {
    log_info "Creando tag git $NEW_VERSION..."
    
    # Commit version bumps
    git add CHANGELOG.md README.md
    git commit -m "chore: bump version to $NEW_VERSION"
    
    # Create annotated tag
    git tag -a "$NEW_VERSION" -m "KaliGhost $NEW_VERSION"
    
    # Push
    git push origin main
    git push origin "$NEW_VERSION"
    
    log_success "Tag $NEW_VERSION creado y pusheado"
}

# Create GitHub release
github_release() {
    if ! command -v gh &> /dev/null; then
        log_warn "gh CLI no disponible – saltando GitHub release automático"
        log_info "Crea release manualmente en: https://github.com/elkalivpn/KaliGhost/releases/new?tag=$NEW_VERSION"
        return
    fi
    
    log_info "Creando GitHub release..."
    
    # Generate release notes from CHANGELOG
    RELEASE_NOTES=$(awk "/^## \[$NEW_VERSION\]/,/^## / { if (!/^## \(?!\[Unreleased\])/) print }" CHANGELOG.md | head -n -1)
    
    gh release create "$NEW_VERSION" \
        --title "KaliGhost $NEW_VERSION" \
        --notes "$RELEASE_NOTES" \
        --latest
    
    log_success "GitHub release creada"
}

# Main flow
main() {
    echo ""
    echo "╔══════════════════════════════════════════╗"
    echo "║   KaliGhost Release Automation v1.0     ║"
    echo "╚══════════════════════════════════════════╝"
    echo ""
    
    check_prereqs
    check_git_status
    bump_version "$1"
    
    log_info " Preparando release $NEW_VERSION..."
    echo ""
    
    read -p "¿Continuar? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warn "Release cancelada"
        exit 0
    fi
    
    update_changelog
    update_readme
    run_tests
    
    # Preguntar por Docker build
    read -p "¿Construir imagen Docker? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        build_docker
    fi
    
    git_release
    github_release
    
    echo ""
    echo "╔══════════════════════════════════════════╗"
    echo "║ ✅ Release $NEW_VERSION completada!       ║"
    echo "╚══════════════════════════════════════════╝"
    echo ""
    echo "Próximos pasos:"
    echo "  1. Verifica la release: https://github.com/elkalivpn/KaliGhost/releases/tag/$NEW_VERSION"
    echo "  2. Anuncia en Telegram: @elkalivpn"
    echo "  3. Actualiza Gumroad links si es needed"
    echo ""
}

# Run
main "$1"
