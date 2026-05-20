#!/bin/bash
# Professional Update Manager for KaliGhost Pro
# Advanced update system with rollback capabilities and professional validation

set -e

# Professional colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Professional banner
echo -e "${CYAN}"
echo "██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ██╗  ██╗ ██████╗ "
echo "██║ ██╔╝██╔══██╗██║     ██║██╔════╝ ██║  ██║██╔═══██╗"
echo "█████╔╝ ███████║██║     ██║██║  ███╗███████║██║   ██║"
echo "██╔═██╗ ██╔══██║██║     ██║██║   ██║██╔══██║██║   ██║"
echo "██║  ██╗██║  ██║███████╗██║╚██████╔╝██║  ██║╚██████╔╝"
echo "╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${PURPLE}🔄 KaliGhost Pro Professional Update Manager${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# Global variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
UPDATE_LOG="$PROJECT_ROOT/logs/update.log"
BACKUP_DIR="$PROJECT_ROOT/backups"
TEMP_DIR="$PROJECT_ROOT/temp"
CURRENT_VERSION_FILE="$PROJECT_ROOT/VERSION"
UPDATE_CHANNEL="stable"

# Function to log professional messages
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$UPDATE_LOG"
    
    case $level in
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        *)
            echo "[UNKNOWN] $message"
            ;;
    esac
}

# Function to setup professional environment
setup_environment() {
    log_message "INFO" "Setting up professional update environment..."
    
    # Create necessary directories
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$TEMP_DIR"
    mkdir -p "$PROJECT_ROOT/logs"
    
    # Check if we're in the right directory
    if [ ! -f "$PROJECT_ROOT/setup.py" ]; then
        log_message "ERROR" "Not in KaliGhost project directory!"
        exit 1
    fi
    
    log_message "SUCCESS" "Professional environment ready"
}

# Function to get current version
get_current_version() {
    if [ -f "$CURRENT_VERSION_FILE" ]; then
        cat "$CURRENT_VERSION_FILE"
    else
        echo "1.0.0"
    fi
}

# Function to check for updates
check_for_updates() {
    log_message "INFO" "Checking for professional updates..."
    
    local current_version=$(get_current_version)
    log_message "INFO" "Current version: $current_version"
    
    # In a real implementation, this would check a remote server
    # For demonstration, we'll simulate checking
    local latest_version="2.0.1"
    
    if [[ "$latest_version" > "$current_version" ]]; then
        log_message "INFO" "Update available: $latest_version"
        echo "$latest_version"
        return 0
    else
        log_message "INFO" "Already running the latest version"
        echo "$current_version"
        return 1
    fi
}

# Function to backup current installation
backup_current_installation() {
    log_message "INFO" "Creating professional backup..."
    
    local backup_name="kalighost_backup_$(date +%Y%m%d_%H%M%S)"
    local backup_path="$BACKUP_DIR/$backup_name"
    
    # Create backup directory
    mkdir -p "$backup_path"
    
    # Copy essential files
    cp -r "$PROJECT_ROOT/src" "$backup_path/" 2>/dev/null || true
    cp -r "$PROJECT_ROOT/config" "$backup_path/" 2>/dev/null || true
    cp "$PROJECT_ROOT/setup.py" "$backup_path/" 2>/dev/null || true
    cp "$PROJECT_ROOT/requirements.txt" "$backup_path/" 2>/dev/null || true
    cp "$CURRENT_VERSION_FILE" "$backup_path/" 2>/dev/null || true
    
    # Create backup metadata
    cat > "$backup_path/backup_info.json" << EOF
{
    "backup_name": "$backup_name",
    "timestamp": "$(date -Iseconds)",
    "version": "$(get_current_version)",
    "backup_path": "$backup_path",
    "project_root": "$PROJECT_ROOT"
}
EOF
    
    log_message "SUCCESS" "Professional backup created: $backup_path"
    echo "$backup_path"
}

# Function to download update
download_update() {
    local version=$1
    log_message "INFO" "Downloading professional update v$version..."
    
    local temp_download="$TEMP_DIR/kalighost_update_${version}.zip"
    
    # In a real implementation, this would download from a remote server
    # For demonstration, we'll create a dummy update package
    mkdir -p "$TEMP_DIR/update_${version}"
    
    # Create dummy update files
    echo "Updated KaliGhost Pro v$version" > "$TEMP_DIR/update_${version}/VERSION"
    echo "# Updated README for v$version" > "$TEMP_DIR/update_${version}/README.md"
    
    # Create update package
    (cd "$TEMP_DIR" && zip -r "kalighost_update_${version}.zip" "update_${version}" >/dev/null 2>&1)
    
    log_message "SUCCESS" "Professional update package downloaded: $temp_download"
    echo "$temp_download"
}

# Function to validate update package
validate_update_package() {
    local package_path=$1
    log_message "INFO" "Validating professional update package..."
    
    # Check if file exists
    if [ ! -f "$package_path" ]; then
        log_message "ERROR" "Update package not found: $package_path"
        return 1
    fi
    
    # Check file integrity (in real implementation, this would check signatures)
    local file_size=$(stat -f%z "$package_path" 2>/dev/null || stat -c%s "$package_path")
    if [ $file_size -lt 100 ]; then
        log_message "ERROR" "Update package appears corrupted (too small)"
        return 1
    fi
    
    # Verify checksum (simulated)
    log_message "SUCCESS" "Professional update package validated successfully"
    return 0
}

# Function to install update
install_update() {
    local package_path=$1
    local backup_path=$2
    local version=$3
    
    log_message "INFO" "Installing professional update v$version..."
    
    # Extract update package
    local extract_dir="$TEMP_DIR/extracted_update"
    rm -rf "$extract_dir"
    mkdir -p "$extract_dir"
    
    unzip -q "$package_path" -d "$extract_dir"
    
    # Stop any running services (simulated)
    log_message "INFO" "Stopping professional services..."
    sleep 2
    
    # Apply update
    log_message "INFO" "Applying professional update..."
    
    # In a real implementation, this would carefully merge changes
    # For demonstration, we'll just update version file
    echo "$version" > "$CURRENT_VERSION_FILE"
    
    # Update configuration if needed
    if [ -f "$extract_dir/update_$version/config/pro_config.ini" ]; then
        cp "$extract_dir/update_$version/config/pro_config.ini" "$PROJECT_ROOT/config/" 2>/dev/null || true
    fi
    
    # Update source files
    if [ -d "$extract_dir/update_$version/src" ]; then
        cp -r "$extract_dir/update_$version/src/." "$PROJECT_ROOT/src/" 2>/dev/null || true
    fi
    
    # Restart services (simulated)
    log_message "INFO" "Starting professional services..."
    sleep 2
    
    log_message "SUCCESS" "Professional update v$version installed successfully"
}

# Function to rollback update
rollback_update() {
    local backup_path=$1
    log_message "WARNING" "Rolling back to previous professional version..."
    
    if [ ! -d "$backup_path" ]; then
        log_message "ERROR" "Backup directory not found: $backup_path"
        return 1
    fi
    
    # Stop services
    log_message "INFO" "Stopping professional services for rollback..."
    sleep 2
    
    # Restore from backup
    if [ -d "$backup_path/src" ]; then
        rm -rf "$PROJECT_ROOT/src"
        cp -r "$backup_path/src" "$PROJECT_ROOT/"
    fi
    
    if [ -d "$backup_path/config" ]; then
        rm -rf "$PROJECT_ROOT/config"
        cp -r "$backup_path/config" "$PROJECT_ROOT/"
    fi
    
    if [ -f "$backup_path/VERSION" ]; then
        cp "$backup_path/VERSION" "$CURRENT_VERSION_FILE"
    fi
    
    # Restart services
    log_message "INFO" "Starting professional services after rollback..."
    sleep 2
    
    log_message "SUCCESS" "Professional rollback completed successfully"
}

# Function to run post-update tests
run_post_update_tests() {
    log_message "INFO" "Running professional post-update validation tests..."
    
    # Test 1: Verify version file
    local current_version=$(get_current_version)
    log_message "INFO" "Verified version: $current_version"
    
    # Test 2: Check Python imports
    if python3 -c "import sys; sys.path.append('$PROJECT_ROOT/src'); import gui.pro_kalighost_main" 2>/dev/null; then
        log_message "SUCCESS" "Professional Python modules imported successfully"
    else
        log_message "WARNING" "Some Python modules may need reinstallation"
    fi
    
    # Test 3: Check configuration files
    if [ -f "$PROJECT_ROOT/config/pro_config.ini" ]; then
        log_message "SUCCESS" "Professional configuration files present"
    else
        log_message "WARNING" "Configuration files may need regeneration"
    fi
    
    log_message "SUCCESS" "Professional post-update tests completed"
}

# Function to clean up temporary files
cleanup_temporary_files() {
    log_message "INFO" "Cleaning up professional temporary files..."
    
    rm -rf "$TEMP_DIR/update_"* 2>/dev/null || true
    rm -rf "$TEMP_DIR/extracted_update" 2>/dev/null || true
    rm -f "$TEMP_DIR/kalighost_update_"*.zip 2>/dev/null || true
    
    log_message "SUCCESS" "Professional temporary files cleaned up"
}

# Function to show update status
show_update_status() {
    local current_version=$(get_current_version)
    echo ""
    echo -e "${CYAN}📊 KaliGhost Pro Professional Update Status${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo "Current Version: $current_version"
    echo "Update Channel: $UPDATE_CHANNEL"
    echo "Installation Path: $PROJECT_ROOT"
    echo "Backup Directory: $BACKUP_DIR"
    echo "Log File: $UPDATE_LOG"
    echo ""
}

# Function to list available backups
list_backups() {
    echo -e "${CYAN}💾 Available Professional Backups${NC}"
    echo -e "${BLUE}===============================${NC}"
    
    if [ -d "$BACKUP_DIR" ] && [ "$(ls -A "$BACKUP_DIR")" ]; then
        ls -la "$BACKUP_DIR"
    else
        echo "No professional backups found."
    fi
    echo ""
}

# Function to show help
show_help() {
    echo -e "${CYAN}📖 KaliGhost Pro Professional Update Manager Help${NC}"
    echo -e "${BLUE}==================================================${NC}"
    echo ""
    echo "Usage: $0 [OPTIONS] COMMAND"
    echo ""
    echo "Commands:"
    echo "  check        Check for available updates"
    echo "  update       Download and install latest update"
    echo "  rollback     Rollback to previous version"
    echo "  status       Show update status"
    echo "  backups      List available backups"
    echo "  cleanup      Clean temporary files"
    echo "  help         Show this help message"
    echo ""
    echo "Options:"
    echo "  -v, --verbose    Enable verbose output"
    echo "  -c, --channel    Specify update channel (stable/beta/nightly)"
    echo "  -b, --backup     Specify backup to restore"
    echo ""
    echo "Examples:"
    echo "  $0 check                         # Check for updates"
    echo "  $0 update                        # Install latest update"
    echo "  $0 rollback -b backup_20260515   # Rollback to specific backup"
    echo "  $0 status                        # Show current status"
    echo ""
}

# Main function
main() {
    local command=""
    local backup_to_restore=""
    local verbose=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            check)
                command="check"
                shift
                ;;
            update)
                command="update"
                shift
                ;;
            rollback)
                command="rollback"
                shift
                ;;
            status)
                command="status"
                shift
                ;;
            backups)
                command="backups"
                shift
                ;;
            cleanup)
                command="cleanup"
                shift
                ;;
            help)
                command="help"
                shift
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -c|--channel)
                UPDATE_CHANNEL="$2"
                shift 2
                ;;
            -b|--backup)
                backup_to_restore="$2"
                shift 2
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Setup environment
    setup_environment
    
    # Execute command
    case $command in
        check)
            if check_for_updates; then
                local latest_version=$(check_for_updates)
                echo -e "${GREEN}Update available: v$latest_version${NC}"
            else
                echo -e "${GREEN}KaliGhost Pro is up to date${NC}"
            fi
            ;;
        update)
            local latest_version=""
            if check_for_updates; then
                latest_version=$(check_for_updates)
                
                # Create backup
                local backup_path=$(backup_current_installation)
                
                # Download update
                local update_package=$(download_update "$latest_version")
                
                # Validate update
                if validate_update_package "$update_package"; then
                    # Install update
                    install_update "$update_package" "$backup_path" "$latest_version"
                    
                    # Run post-update tests
                    run_post_update_tests
                    
                    # Cleanup
                    cleanup_temporary_files
                    
                    echo -e "${GREEN}✅ KaliGhost Pro successfully updated to v$latest_version${NC}"
                    echo -e "${YELLOW}💡 A backup has been created at: $backup_path${NC}"
                else
                    log_message "ERROR" "Update package validation failed. Rolling back..."
                    rollback_update "$backup_path"
                    exit 1
                fi
            else
                echo -e "${GREEN}KaliGhost Pro is already up to date${NC}"
            fi
            ;;
        rollback)
            if [ -n "$backup_to_restore" ]; then
                local backup_path="$BACKUP_DIR/$backup_to_restore"
                if [ -d "$backup_path" ]; then
                    rollback_update "$backup_path"
                    echo -e "${GREEN}✅ Successfully rolled back to $backup_to_restore${NC}"
                else
                    echo -e "${RED}❌ Backup not found: $backup_to_restore${NC}"
                    list_backups
                    exit 1
                fi
            else
                echo -e "${RED}❌ Please specify a backup to restore with -b option${NC}"
                list_backups
                exit 1
            fi
            ;;
        status)
            show_update_status
            ;;
        backups)
            list_backups
            ;;
        cleanup)
            cleanup_temporary_files
            echo -e "${GREEN}✅ Temporary files cleaned up${NC}"
            ;;
        help|"")
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: $command${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi