#!/bin/bash
# Scheduling helper script for Linux/macOS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/github_auto_commit.py"
CONFIG_PATH="$SCRIPT_DIR/config.json"

show_help() {
    echo "GitHub Auto Commit Scheduler Helper"
    echo "=================================="
    echo "Usage: ./scheduler_helper.sh [command]"
    echo ""
    echo "Commands:"
    echo "  install     - Install/update cron job"
    echo "  remove      - Remove cron job"
    echo "  status      - Show current cron jobs"
    echo "  list        - List all scheduled tasks"
    echo "  run         - Run script manually"
    echo "  test        - Run in dry-run mode"
    echo "  help        - Show this help"
    echo ""
    echo "Examples:"
    echo "  ./scheduler_helper.sh install"
    echo "  ./scheduler_helper.sh run --mode backfill --days 30"
}

install_cron() {
    echo "Installing cron job..."
    
    # Generate random time (between 7 AM and 10 PM)
    HOUR=$((RANDOM % 15 + 7))
    MINUTE=$((RANDOM % 60))
    
    # Create cron entry
    CRON_JOB="$MINUTE $HOUR * * * cd $SCRIPT_DIR && python3 $SCRIPT_PATH --mode daily --config $CONFIG_PATH >> $SCRIPT_DIR/auto_commit.log 2>&1"
    
    # Add to crontab
    (crontab -l 2>/dev/null | grep -v "github_auto_commit.py"; echo "$CRON_JOB") | crontab -
    
    echo "✓ Cron job installed for $HOUR:$MINUTE daily"
    echo "Log file: $SCRIPT_DIR/auto_commit.log"
}

remove_cron() {
    echo "Removing cron job..."
    
    # Remove entries containing our script
    crontab -l 2>/dev/null | grep -v "github_auto_commit.py" | crontab -
    
    echo "✓ Cron job removed"
}

show_status() {
    echo "Current cron jobs:"
    echo "=================="
    crontab -l 2>/dev/null | grep "github_auto_commit.py" || echo "No GitHub auto commit jobs found"
}

list_tasks() {
    echo "Scheduled GitHub Auto Commit Tasks:"
    echo "==================================="
    crontab -l 2>/dev/null | grep "github_auto_commit.py" | while read line; do
        echo "$line"
    done || echo "No scheduled tasks found"
}

run_script() {
    echo "Running GitHub Auto Commit script..."
    python3 "$SCRIPT_PATH" "$@"
}

case "${1:-help}" in
    install)
        install_cron
        ;;
    remove)
        remove_cron
        ;;
    status)
        show_status
        ;;
    list)
        list_tasks
        ;;
    run)
        shift
        run_script "$@"
        ;;
    test)
        run_script --dry-run
        ;;
    help|*)
        show_help
        ;;
esac