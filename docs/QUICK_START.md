# 🚀 Quick Start Guide

## 1. One-Click Setup

### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

### Windows
```cmd
setup.bat
```

## 2. Immediate Test
```bash
# Test without making real changes
python github_auto_commit.py --dry-run

# Make one actual commit
python github_auto_commit.py --mode daily
```

## 3. Setup Automatic Scheduling

### Linux/macOS
```bash
./scheduler_helper.sh install
```

### Windows
```cmd
scheduler_helper.bat install
```

## 4. Monitor Activity
```bash
# View recent activity
python monitor.py

# Check logs
tail -f auto_commit.log  # Linux/macOS
Get-Content auto_commit.log -Wait  # Windows PowerShell
```

## 5. Essential Configuration

Edit `config.json`:
```json
{
  "daily_commit_range": [1, 3],  // Start conservative
  "active_hours_start": 8,       // Work hours only
  "active_hours_end": 18,        // Work hours only
  "dry_run": false               // Set to true for testing
}
```

## 6. Connect to GitHub

```bash
# Add your GitHub remote
git remote add origin https://github.com/username/repository.git

# Push initial commits
git push -u origin main
```

## ⚡ Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `python github_auto_commit.py --dry-run` | Test without changes |
| `python github_auto_commit.py --mode daily` | Make daily commits |
| `python github_auto_commit.py --mode backfill --days 30` | Fill missing dates |
| `python monitor.py` | View activity report |
| `./scheduler_helper.sh status` | Check scheduling (Linux/macOS) |
| `scheduler_helper.bat status` | Check scheduling (Windows) |

## 🛡 Safety First

1. **Always test with `--dry-run` first**
2. **Start with 1-2 commits per day**
3. **Monitor the logs regularly**
4. **Review GitHub contribution graph weekly**

## 🆘 Need Help?

1. Check `auto_commit.log` for errors
2. Run `python monitor.py` for diagnostics
3. Review the full README.md
4. Ensure Python 3 and Git are installed

---

**Remember**: Quality contributions matter more than quantity. Use this tool responsibly! 🌟