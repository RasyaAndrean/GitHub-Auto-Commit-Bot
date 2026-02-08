#!/usr/bin/env python3
"""
GitHub Auto Commit Monitor
Monitoring and analysis tool for the auto commit system
"""

import json
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
import argparse


class CommitMonitor:
    def __init__(self, log_file="auto_commit.log", config_file="config.json"):
        self.log_file = log_file
        self.config_file = config_file
        self.stats = defaultdict(int)
        self.daily_stats = defaultdict(lambda: defaultdict(int))
        
    def parse_log(self):
        """Parse the log file and extract statistics."""
        if not os.path.exists(self.log_file):
            print("No log file found")
            return
            
        with open(self.log_file, 'r') as f:
            for line in f:
                self._parse_line(line.strip())
    
    def _parse_line(self, line):
        """Parse individual log line."""
        # Extract timestamp and message
        timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if not timestamp_match:
            return
            
        timestamp = timestamp_match.group(1)
        date = timestamp.split()[0]
        
        # Count different types of activities
        if "Created commit:" in line:
            self.stats['total_commits'] += 1
            self.daily_stats[date]['commits'] += 1
        elif "DRY RUN" in line:
            self.stats['dry_runs'] += 1
        elif "ERROR" in line:
            self.stats['errors'] += 1
        elif "SKIP" in line or "Skipping" in line:
            self.stats['skipped'] += 1
    
    def analyze_patterns(self):
        """Analyze commit patterns for naturalness."""
        print("📈 Commit Pattern Analysis")
        print("=" * 50)
        
        if not self.daily_stats:
            print("No commit data available")
            return
            
        # Calculate daily statistics
        daily_counts = [stats['commits'] for stats in self.daily_stats.values() if stats['commits'] > 0]
        
        if not daily_counts:
            print("No successful commits recorded")
            return
            
        avg_commits = sum(daily_counts) / len(daily_counts)
        max_commits = max(daily_counts)
        min_commits = min(daily_counts)
        
        print(f"Average commits per active day: {avg_commits:.1f}")
        print(f"Maximum commits in a day: {max_commits}")
        print(f"Minimum commits in a day: {min_commits}")
        print(f"Total active days: {len(daily_counts)}")
        print(f"Total commits: {sum(daily_counts)}")
        
        # Check for unnatural patterns
        self._check_naturalness(daily_counts)
    
    def _check_naturalness(self, daily_counts):
        """Check if commit patterns look natural."""
        print("\n🔍 Naturalness Assessment")
        print("-" * 30)
        
        issues = []
        
        # Check for too many consecutive days with commits
        consecutive_days = self._count_consecutive_active_days()
        if consecutive_days > 30:
            issues.append(f"⚠ Long streak of {consecutive_days} consecutive days")
        
        # Check for uniform commit counts
        if len(set(daily_counts)) < len(daily_counts) * 0.3:
            issues.append("⚠ Too many days with identical commit counts")
        
        # Check for weekend activity (if configured to avoid)
        weekend_activity = self._check_weekend_activity()
        if weekend_activity > 0.8:
            issues.append("⚠ High weekend activity (>80%)")
        
        if issues:
            print("Potential unnatural patterns detected:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("✅ Commit patterns appear natural")
    
    def _count_consecutive_active_days(self):
        """Count maximum consecutive active days."""
        dates = sorted(self.daily_stats.keys())
        if not dates:
            return 0
            
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            current_date = datetime.strptime(dates[i], "%Y-%m-%d")
            prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d")
            
            if (current_date - prev_date).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
                
        return max_streak
    
    def _check_weekend_activity(self):
        """Calculate weekend activity ratio."""
        weekend_commits = 0
        total_commits = 0
        
        for date_str, stats in self.daily_stats.items():
            if stats['commits'] > 0:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                # Saturday = 5, Sunday = 6
                if date.weekday() >= 5:
                    weekend_commits += stats['commits']
                total_commits += stats['commits']
        
        return weekend_commits / total_commits if total_commits > 0 else 0
    
    def show_recent_activity(self, days=7):
        """Show recent commit activity."""
        print(f"\n📅 Recent Activity (Last {days} Days)")
        print("-" * 40)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_activity = {}
        
        for date_str, stats in self.daily_stats.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date >= cutoff_date:
                recent_activity[date_str] = stats
        
        if not recent_activity:
            print("No recent activity found")
            return
            
        for date_str in sorted(recent_activity.keys(), reverse=True):
            stats = recent_activity[date_str]
            if stats['commits'] > 0:
                print(f"{date_str}: {stats['commits']} commits")
    
    def check_safety_metrics(self):
        """Check various safety metrics."""
        print("\n🛡 Safety Metrics")
        print("-" * 20)
        
        # Error rate
        total_attempts = self.stats['total_commits'] + self.stats['errors'] + self.stats['skipped']
        error_rate = (self.stats['errors'] / total_attempts * 100) if total_attempts > 0 else 0
        
        print(f"Error rate: {error_rate:.1f}%")
        print(f"Dry runs performed: {self.stats['dry_runs']}")
        print(f"Operations skipped: {self.stats['skipped']}")
        
        if error_rate > 5:
            print("⚠ High error rate detected")
        else:
            print("✅ Good error rate")
    
    def generate_report(self):
        """Generate comprehensive monitoring report."""
        self.parse_log()
        
        print("🤖 GitHub Auto Commit Monitor Report")
        print("=" * 50)
        print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Log file: {self.log_file}")
        print()
        
        self.analyze_patterns()
        self.check_safety_metrics()
        self.show_recent_activity()


def main():
    parser = argparse.ArgumentParser(description="GitHub Auto Commit Monitor")
    parser.add_argument("--log-file", default="auto_commit.log", help="Log file path")
    parser.add_argument("--config-file", default="config.json", help="Config file path")
    parser.add_argument("--days", type=int, default=7, help="Days of recent activity to show")
    
    args = parser.parse_args()
    
    monitor = CommitMonitor(args.log_file, args.config_file)
    monitor.generate_report()


if __name__ == "__main__":
    main()