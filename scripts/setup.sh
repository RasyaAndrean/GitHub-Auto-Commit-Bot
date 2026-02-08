#!/bin/bash
# Setup script for GitHub Auto Commit (Linux/macOS)

set -e

echo "🚀 Setting up GitHub Auto Commit Script..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    print_status "Detected OS: $OS"
}

# Check Python installation
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_status "Found Python 3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1)
        if [ "$PYTHON_VERSION" -ge "3" ]; then
            PYTHON_CMD="python"
            print_status "Found Python"
        else
            print_error "Python 3 is required"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        print_warning "Please install Python 3 and try again"
        exit 1
    fi
}

# Check Git installation
check_git() {
    if command -v git &> /dev/null; then
        print_status "Found Git"
    else
        print_error "Git is not installed"
        print_warning "Please install Git and try again"
        exit 1
    fi
}

# Install required Python packages
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_warning "pip not found, attempting to install..."
        if [[ "$OS" == "Linux" ]]; then
            sudo apt-get update
            sudo apt-get install -y python3-pip
        elif [[ "$OS" == "macOS" ]]; then
            brew install python
        fi
    fi
    
    print_status "Dependencies installed successfully"
}

# Create initial files
create_initial_files() {
    print_status "Creating initial tracking files..."
    
    # Create activity log
    touch activity_log.txt
    echo "# Activity Log" > activity_log.txt
    echo "This file tracks automated activities." >> activity_log.txt
    echo "" >> activity_log.txt
    
    # Create progress tracker
    touch progress_tracker.md
    echo "# Progress Tracker" > progress_tracker.md
    echo "" >> progress_tracker.md
    echo "## Today's Progress" >> progress_tracker.md
    echo "" >> progress_tracker.md
    
    # Create development notes
    touch development_notes.txt
    echo "# Development Notes" > development_notes.txt
    echo "Automated development tracking file." >> development_notes.txt
    echo "" >> development_notes.txt
    
    # Create changelog
    touch changelog.md
    echo "# Changelog" > changelog.md
    echo "" >> changelog.md
    echo "All changes are tracked automatically." >> changelog.md
    echo "" >> changelog.md
    
    print_status "Initial files created"
}

# Setup cron job
setup_cron() {
    echo ""
    print_warning "Setting up scheduled execution..."
    
    # Ask user preference
    read -p "Would you like to setup automatic daily execution? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Create cron entry
        SCRIPT_PATH="$(pwd)/github_auto_commit.py"
        CONFIG_PATH="$(pwd)/config.json"
        
        # Random time between 9 AM and 9 PM
        HOUR=$((RANDOM % 12 + 9))
        MINUTE=$((RANDOM % 60))
        
        CRON_JOB="$MINUTE $HOUR * * * cd $(pwd) && $PYTHON_CMD $SCRIPT_PATH --mode daily --config $CONFIG_PATH >> auto_commit.log 2>&1"
        
        # Add to crontab
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        
        print_status "Cron job scheduled for $HOUR:$MINUTE daily"
        print_status "You can modify the schedule by running: crontab -e"
    else
        print_warning "Skipping cron setup. You can run manually or setup later."
    fi
}

# Test the setup
test_setup() {
    echo ""
    print_status "Testing the setup..."
    
    # Run a dry-run test
    if $PYTHON_CMD github_auto_commit.py --mode daily --dry-run; then
        print_status "Setup test completed successfully!"
    else
        print_error "Setup test failed"
        exit 1
    fi
}

# Main setup process
main() {
    check_os
    check_python
    check_git
    install_dependencies
    create_initial_files
    setup_cron
    test_setup
    
    echo ""
    print_status "🎉 Setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "  1. Review config.json to customize settings"
    echo "  2. Run manually: $PYTHON_CMD github_auto_commit.py --mode daily"
    echo "  3. For backfill: $PYTHON_CMD github_auto_commit.py --mode backfill --days 30"
    echo "  4. Check auto_commit.log for activity logs"
    echo ""
    print_warning "Remember to push to your GitHub repository:"
    echo "  git remote add origin https://github.com/username/repository.git"
    echo "  git push -u origin main"
}

# Run main function
main