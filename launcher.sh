#!/bin/bash
# GitHub Auto Commit Launcher for Linux/macOS

echo "🚀 GitHub Auto Commit Bot Launcher"
echo "===================================="

while true; do
    echo ""
    echo "Select an option:"
    echo "1. Quick Setup"
    echo "2. Test Installation"
    echo "3. Run Daily Commits"
    echo "4. Backfill History"
    echo "5. Monitor Activity"
    echo "6. Manage Scheduling"
    echo "7. View Documentation"
    echo "8. Exit"
    echo ""
    
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔧 Running Setup..."
            cd scripts
            chmod +x setup.sh
            ./setup.sh
            cd ..
            ;;
        2)
            echo ""
            echo "🧪 Testing Installation..."
            cd scripts
            python3 github_auto_commit.py --dry-run
            cd ..
            read -p "Press Enter to continue..."
            ;;
        3)
            echo ""
            echo "📅 Running Daily Commits..."
            cd scripts
            python3 github_auto_commit.py --mode daily
            cd ..
            read -p "Press Enter to continue..."
            ;;
        4)
            echo ""
            read -p "Enter number of days to backfill: " days
            echo "⏪ Backfilling $days days..."
            cd scripts
            python3 github_auto_commit.py --mode backfill --days $days
            cd ..
            read -p "Press Enter to continue..."
            ;;
        5)
            echo ""
            echo "📊 Monitoring Activity..."
            cd scripts
            python3 monitor.py
            cd ..
            read -p "Press Enter to continue..."
            ;;
        6)
            while true; do
                echo ""
                echo "⏰ Schedule Management"
                echo "1. Install scheduled task"
                echo "2. Remove scheduled task"
                echo "3. Check task status"
                echo "4. Back to main menu"
                read -p "Enter choice (1-4): " sched_choice
                
                case $sched_choice in
                    1)
                        cd scripts
                        chmod +x scheduler_helper.sh
                        ./scheduler_helper.sh install
                        cd ..
                        ;;
                    2)
                        cd scripts
                        ./scheduler_helper.sh remove
                        cd ..
                        ;;
                    3)
                        cd scripts
                        ./scheduler_helper.sh status
                        cd ..
                        ;;
                    4)
                        break
                        ;;
                    *)
                        echo "Invalid choice."
                        ;;
                esac
            done
            ;;
        7)
            echo ""
            echo "📖 Opening Documentation..."
            echo "Check the docs/ folder for detailed documentation"
            echo "Quick Start Guide: docs/QUICK_START.md"
            echo "Full Documentation: docs/README.md"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        8)
            echo ""
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done