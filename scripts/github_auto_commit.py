#!/usr/bin/env python3
"""
GitHub Auto Commit Script
Automatically generates commits to keep your GitHub contribution graph green
with natural-looking patterns and safety features.
"""

import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import logging
from typing import List, Dict, Optional


class GitHubAutoCommit:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the auto commit manager."""
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self) -> Dict:
        """Load configuration from JSON file."""
        default_config = {
            "repository_path": ".",
            "commit_messages": [
                "Update documentation",
                "Refactor code for better performance",
                "Add new feature implementation",
                "Fix minor bug in code",
                "Improve code readability",
                "Update dependencies",
                "Enhance user experience",
                "Optimize algorithm efficiency",
                "Add unit tests",
                "Update README file",
                "Improve error handling",
                "Add type annotations",
                "Refactor module structure",
                "Update configuration files",
                "Add logging functionality"
            ],
            "files_to_modify": ["activity_log.txt", "progress_tracker.md"],
            "daily_commit_range": [1, 5],
            "active_hours_start": 8,
            "active_hours_end": 22,
            "backfill_days": 365,
            "log_file": "auto_commit.log",
            "dry_run": False,
            "enable_randomization": True
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            else:
                # Create default config file
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                print(f"Created default config file: {self.config_path}")
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
            
        return default_config
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(self.config['log_file']),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def is_git_repository(self) -> bool:
        """Check if current directory is a git repository."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                cwd=self.config['repository_path']
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def setup_git_repository(self) -> bool:
        """Initialize git repository if it doesn't exist."""
        if self.is_git_repository():
            return True
            
        try:
            subprocess.run(['git', 'init'], cwd=self.config['repository_path'], check=True)
            subprocess.run(['git', 'checkout', '-b', 'main'], cwd=self.config['repository_path'], check=True)
            
            # Create initial commit
            readme_content = "# Auto Commit Repository\n\nThis repository is maintained by auto-commit script.\n"
            with open(os.path.join(self.config['repository_path'], 'README.md'), 'w') as f:
                f.write(readme_content)
                
            subprocess.run(['git', 'add', 'README.md'], cwd=self.config['repository_path'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=self.config['repository_path'], check=True)
            
            self.logger.info("Initialized new git repository")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup git repository: {e}")
            return False
    
    def get_random_commit_message(self) -> str:
        """Generate a random but meaningful commit message."""
        base_messages = self.config['commit_messages']
        message = random.choice(base_messages)
        
        # Add some variation
        variations = ["", " - minor update", " - improvements", " - cleanup"]
        variation = random.choice(variations)
        
        return f"{message}{variation}"
    
    def make_small_change(self, file_path: str) -> bool:
        """Make a small change to a file to create commit content."""
        try:
            full_path = os.path.join(self.config['repository_path'], file_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            change_entry = f"[{timestamp}] Automated activity entry\n"
            
            # Append to file or create new
            with open(full_path, 'a') as f:
                f.write(change_entry)
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to modify file {file_path}: {e}")
            return False
    
    def should_commit_now(self) -> bool:
        """Check if current time is appropriate for committing."""
        if not self.config['enable_randomization']:
            return True
            
        current_hour = datetime.now().hour
        
        # Don't commit during sleep hours
        if current_hour < self.config['active_hours_start'] or current_hour >= self.config['active_hours_end']:
            return False
            
        # Add some randomness to make it less predictable
        if random.random() < 0.3:  # 30% chance to skip even during active hours
            return False
            
        return True
    
    def create_commit(self, message: str) -> bool:
        """Create a single commit."""
        if self.config['dry_run']:
            self.logger.info(f"[DRY RUN] Would commit: {message}")
            return True
            
        try:
            # Select random file to modify
            file_to_modify = random.choice(self.config['files_to_modify'])
            
            # Make small change
            if not self.make_small_change(file_to_modify):
                return False
            
            # Stage changes
            subprocess.run(
                ['git', 'add', file_to_modify],
                cwd=self.config['repository_path'],
                check=True
            )
            
            # Create commit
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.config['repository_path'],
                check=True
            )
            
            self.logger.info(f"Created commit: {message}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git command failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to create commit: {e}")
            return False
    
    def run_daily_commits(self) -> int:
        """Run daily commit routine."""
        if not self.should_commit_now():
            self.logger.info("Skipping commit - not appropriate time")
            return 0
            
        # Determine number of commits for today
        min_commits, max_commits = self.config['daily_commit_range']
        num_commits = random.randint(min_commits, max_commits)
        
        commits_made = 0
        
        for i in range(num_commits):
            message = self.get_random_commit_message()
            
            if self.create_commit(message):
                commits_made += 1
                
                # Add delay between commits to look more natural
                if i < num_commits - 1:  # Don't sleep after last commit
                    delay = random.randint(30, 300)  # 30 seconds to 5 minutes
                    if not self.config['dry_run']:
                        time.sleep(delay)
        
        self.logger.info(f"Daily routine completed. Made {commits_made} commits")
        return commits_made
    
    def backfill_history(self, days: int = None) -> int:
        """Backfill commit history for specified number of days."""
        if days is None:
            days = self.config['backfill_days']
            
        commits_made = 0
        
        self.logger.info(f"Starting backfill for {days} days")
        
        for day_offset in range(days - 1, -1, -1):
            target_date = datetime.now() - timedelta(days=day_offset)
            
            # Set GIT_AUTHOR_DATE and GIT_COMMITTER_DATE
            date_str = target_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Determine number of commits for this day
            min_commits, max_commits = self.config['daily_commit_range']
            num_commits = random.randint(min_commits, max_commits)
            
            for _ in range(num_commits):
                message = self.get_random_commit_message()
                
                if self.config['dry_run']:
                    self.logger.info(f"[DRY RUN] Would backfill commit for {date_str}: {message}")
                    commits_made += 1
                    continue
                
                try:
                    # Select random file
                    file_to_modify = random.choice(self.config['files_to_modify'])
                    
                    # Make change
                    if not self.make_small_change(file_to_modify):
                        continue
                    
                    # Stage
                    subprocess.run(
                        ['git', 'add', file_to_modify],
                        cwd=self.config['repository_path'],
                        check=True
                    )
                    
                    # Commit with specific date
                    env = os.environ.copy()
                    env['GIT_AUTHOR_DATE'] = date_str
                    env['GIT_COMMITTER_DATE'] = date_str
                    
                    subprocess.run(
                        ['git', 'commit', '-m', message],
                        cwd=self.config['repository_path'],
                        env=env,
                        check=True
                    )
                    
                    commits_made += 1
                    self.logger.info(f"Backfilled commit for {date_str}: {message}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to backfill commit for {date_str}: {e}")
        
        self.logger.info(f"Backfill completed. Made {commits_made} commits")
        return commits_made
    
    def push_changes(self) -> bool:
        """Push changes to remote repository."""
        if self.config['dry_run']:
            self.logger.info("[DRY RUN] Would push changes to remote")
            return True
            
        try:
            # Check if remote exists
            result = subprocess.run(
                ['git', 'remote'],
                cwd=self.config['repository_path'],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                subprocess.run(
                    ['git', 'push', 'origin', 'main'],
                    cwd=self.config['repository_path'],
                    check=True
                )
                self.logger.info("Changes pushed to remote repository")
                return True
            else:
                self.logger.warning("No remote repository configured")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to push changes: {e}")
            return False
    
    def run(self, mode: str = "daily", backfill_days: int = None) -> int:
        """Main execution method."""
        self.logger.info(f"Starting auto commit script in {mode} mode")
        
        # Setup repository
        if not self.setup_git_repository():
            return 0
        
        commits_made = 0
        
        if mode == "daily":
            commits_made = self.run_daily_commits()
        elif mode == "backfill":
            commits_made = self.backfill_history(backfill_days)
        
        if commits_made > 0:
            self.push_changes()
        
        self.logger.info(f"Script completed. Total commits made: {commits_made}")
        return commits_made


def main():
    parser = argparse.ArgumentParser(description="GitHub Auto Commit Script")
    parser.add_argument(
        "--mode",
        choices=["daily", "backfill"],
        default="daily",
        help="Execution mode (default: daily)"
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Number of days to backfill (only for backfill mode)"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Configuration file path (default: config.json)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test mode - show what would happen without making changes"
    )
    
    args = parser.parse_args()
    
    # Create auto commit instance
    auto_commit = GitHubAutoCommit(args.config)
    
    # Override dry run setting if specified
    if args.dry_run:
        auto_commit.config['dry_run'] = True
    
    # Run the script
    try:
        commits_made = auto_commit.run(mode=args.mode, backfill_days=args.days)
        print(f"Successfully made {commits_made} commits")
        return 0
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        return 1
    except Exception as e:
        print(f"Script failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())