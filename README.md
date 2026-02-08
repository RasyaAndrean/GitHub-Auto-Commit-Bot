# 🤖 GitHub Auto Commit Bot

Automate your GitHub contributions with intelligent commit patterns that keep your contribution graph green while maintaining a natural appearance.

## 📁 Project Structure

```
github-auto-commit/
├── main.py                  # Interactive GitHub Auto Bot (main interface)
├── README.md                # Root project overview
├── requirements.txt         # System requirements
├── LICENSE                  # License information
│
├── scripts/                 # Core automation scripts
│   ├── github_auto_commit.py     # Core automation script
│   └── monitor.py               # Monitoring and analysis tool
│
├── configs/                 # Configuration files
│   ├── config1.json              # Main configuration
│   ├── config2.json              # Secondary configuration
│   └── config.example.json       # Example configuration
│
├── docs/                    # Documentation
│   ├── README.md                # Detailed documentation
│   ├── QUICK_START.md           # Quick start guide
│   └── PROJECT_SUMMARY.md       # Project overview
│
├── logs/                    # Log files
│   ├── activity_log.txt          # Activity logs
│   └── auto_commit.log           # Auto commit logs
│
├── activity_tracking/       # Generated tracking files
│   ├── activity_log.txt         # Activity log (generated during runtime)
│   ├── progress_tracker.md      # Progress tracking (generated during runtime)
│   ├── development_notes.txt    # Development notes (generated during runtime)
│   └── changelog.md             # Change log (generated during runtime)
│
```

## 🚀 Quick Start

### 1. Run the Interactive GitHub Auto Bot (Recommended)
```bash
# Direct command - Linux/macOS
python3 main.py

# Direct command - Windows
python main.py
```

### 2. Test the Setup
```bash
# Direct command - Linux/macOS
cd scripts && python3 github_auto_commit.py --dry-run

# Direct command - Windows
cd scripts && python github_auto_commit.py --dry-run
```

### 3. Run Daily Commits
```bash
# Linux/macOS
cd scripts && python3 github_auto_commit.py --mode daily

# Windows
cd scripts && python github_auto_commit.py --mode daily
```

### 3. GitHub Auto Bot (Interactive Mode) ⭐ MAIN FEATURE
```bash
# Direct command - Linux/macOS
python3 main.py

# Direct command - Windows
python main.py
```

The GitHub Auto Bot provides an interactive menu with these features:
- 🔐 **GitHub Authentication** - Secure token-based login
- 📚 **Repository Management** - List and select from your GitHub repositories
- 🎯 **Targeted Commits** - Commit to specific repositories only
- 🔄 **Bulk Operations** - Commit to all repositories at once
- ⚙️ **Configuration Management** - Save and load credentials

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
✅ **Interactive GitHub Bot** - Menu-driven repository management ⭐ NEW  

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
1. **Run the main interactive bot**: `python main.py` - Provides easy access to all functions
2. Check the [documentation](docs/README.md)
3. Review logs in the `logs/` directory
4. Run the monitor script: `python scripts/monitor.py`

---

**License**: MIT with ethical usage notice  
**Disclaimer**: Use only on your own repositories and in accordance with platform terms of service