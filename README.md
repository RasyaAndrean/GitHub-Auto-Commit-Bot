# 🤖 GitHub Auto Commit Bot

Automate your GitHub contributions with intelligent commit patterns that keep your contribution graph green while maintaining a natural appearance.

## 📁 Project Structure

```
github-auto-commit/
├── launcher.bat             # Windows launcher menu
├── launcher.sh              # Linux/macOS launcher menu
├── README.md                # Root project overview
├── requirements.txt         # System requirements
├── LICENSE                  # License information
│
├── scripts/                 # Main executable scripts
│   ├── github_auto_commit.py     # Core automation script
│   ├── monitor.py               # Monitoring and analysis tool
│   ├── setup.sh                 # Linux/macOS setup script
│   ├── setup.bat                # Windows setup script
│   ├── scheduler_helper.sh      # Linux/macOS scheduling helper
│   └── scheduler_helper.bat     # Windows scheduling helper
│
├── configs/                 # Configuration files
│   ├── config.json              # Main configuration (auto-generated)
│   └── config.example.json      # Example configuration
│
├── docs/                    # Documentation
│   ├── README.md                # Detailed documentation
│   ├── QUICK_START.md           # Quick start guide
│   └── PROJECT_SUMMARY.md       # Project overview
│
├── logs/                    # Log files
│   └── auto_commit.log          # Activity logs
│
├── test/                    # Test scripts
│   ├── test_setup.sh            # Linux/macOS test script
│   └── test_setup.bat           # Windows test script
│
├── activity_tracking/       # Generated tracking files
│   ├── activity_log.txt         # Activity log (generated during runtime)
│   ├── progress_tracker.md      # Progress tracking (generated during runtime)
│   ├── development_notes.txt    # Development notes (generated during runtime)
│   └── changelog.md             # Change log (generated during runtime)
│
└── .qoder/                  # Qoder IDE configuration
```

## 🚀 Quick Start

### 1. One-Click Setup
```bash
# Linux/macOS
chmod +x launcher.sh && ./launcher.sh
# Or directly: cd scripts && chmod +x setup.sh && ./setup.sh

# Windows
launcher.bat
# Or directly: cd scripts && setup.bat
```

### 2. Test the Setup
```bash
# Using launcher (recommended)
# Select option 2 in the launcher menu

# Direct command - Linux/macOS
cd scripts && python3 github_auto_commit.py --dry-run

# Direct command - Windows
cd scripts && python github_auto_commit.py --dry-run

# Using test scripts
cd test && ./test_setup.sh    # Linux/macOS
cd test && test_setup.bat     # Windows
```

### 3. Run Daily Commits
```bash
# Linux/macOS
cd scripts && python3 github_auto_commit.py --mode daily

# Windows
cd scripts && python github_auto_commit.py --mode daily
```

## 📖 Documentation

- **[Full Documentation](docs/README.md)** - Complete guide with all features
- **[Quick Start Guide](docs/QUICK_START.md)** - Fast setup instructions
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Overview and features

## ⚡ Key Features

✅ **Cross-platform** - Works on Windows, Linux, and macOS  
✅ **Natural patterns** - Randomized timing and commit frequency  
✅ **Safety features** - Anti-spam measures and pattern analysis  
✅ **Easy scheduling** - Automatic cron/Task Scheduler setup  
✅ **Comprehensive monitoring** - Activity tracking and analysis  
✅ **Flexible configuration** - Customizable settings via JSON  

## 🛡 Safety & Ethics

This tool includes built-in safety features to maintain natural-looking contribution patterns:
- Time-based commit restrictions
- Random delays between commits
- Variable daily commit counts
- Pattern analysis to detect unnatural behavior
- Comprehensive logging for monitoring

**Important**: Use responsibly and combine with genuine contributions.

## 📞 Support

For issues and questions:
1. **Use the launcher menu** - It provides easy access to all functions
2. Check the [documentation](docs/README.md)
3. Review logs in the `logs/` directory
4. Run the monitor script: `python scripts/monitor.py`

---

**License**: MIT with ethical usage notice  
**Disclaimer**: Use only on your own repositories and in accordance with platform terms of service