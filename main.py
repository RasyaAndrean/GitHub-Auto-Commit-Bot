#!/usr/bin/env python3
"""
GitHub Auto Commit Bot - Main Interface
Interactive menu for GitHub automation with user authentication
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import requests
from typing import List, Dict, Optional

class GitHubAutoCommitBot:
    def __init__(self):
        self.github_username = ""
        self.github_token = ""
        self.repositories = []
        self.config_file = "configs/github_config.json"
        self.script_dir = Path(__file__).parent
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        self.clear_screen()
        print("=" * 60)
        print("🤖 GITHUB AUTO COMMIT BOT")
        print("=" * 60)
        print()
    
    def save_credentials(self):
        """Save GitHub credentials to config file."""
        config_data = {
            "github_username": self.github_username,
            "github_token": self.github_token,
            "last_used_repos": self.repositories
        }
        
        # Create configs directory if it doesn't exist
        config_path = Path(self.config_file)
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print("✅ Credentials saved successfully!")
    
    def load_credentials(self):
        """Load saved GitHub credentials."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.github_username = config_data.get("github_username", "")
                    self.github_token = config_data.get("github_token", "")
                    self.repositories = config_data.get("last_used_repos", [])
                return True
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
        return False
    
    def validate_github_token(self) -> bool:
        """Validate GitHub token by fetching user repos."""
        try:
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(
                f"https://api.github.com/user/repos",
                headers=headers,
                params={"per_page": 100}
            )
            
            if response.status_code == 200:
                repos_data = response.json()
                self.repositories = [
                    {
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "clone_url": repo["clone_url"],
                        "private": repo["private"]
                    }
                    for repo in repos_data
                ]
                return True
            else:
                print(f"❌ GitHub API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error validating token: {e}")
            return False
    
    def get_user_input(self):
        """Get GitHub credentials from user."""
        print("🔐 GitHub Authentication")
        print("-" * 30)
        
        # Load existing credentials
        if self.load_credentials():
            use_existing = input(f"Use existing username '{self.github_username}'? (y/n): ").lower()
            if use_existing == 'y':
                token_input = input("Enter GitHub Token (or press Enter to use saved): ")
                if token_input.strip():
                    self.github_token = token_input
                # Validate the token
                if self.validate_github_token():
                    print("✅ Authentication successful!")
                    return True
                else:
                    print("❌ Invalid token. Please enter new credentials.")
            else:
                self.github_username = ""
                self.github_token = ""
        
        # Get new credentials
        if not self.github_username:
            self.github_username = input("Enter GitHub Username: ").strip()
        
        if not self.github_token:
            self.github_token = input("Enter GitHub Personal Access Token: ").strip()
        
        # Validate credentials
        print("\n🔍 Validating credentials...")
        if self.validate_github_token():
            self.save_credentials()
            return True
        else:
            print("❌ Authentication failed. Please check your credentials.")
            return False
    
    def list_repositories(self):
        """Display list of user repositories."""
        print("\n📚 Your GitHub Repositories:")
        print("-" * 50)
        
        for i, repo in enumerate(self.repositories, 1):
            privacy = "🔒 Private" if repo["private"] else "🌐 Public"
            print(f"{i:2d}. {repo['name']} ({privacy})")
        
        print(f"\nTotal: {len(self.repositories)} repositories")
    
    def clone_repository(self, repo_full_name: str, repo_clone_url: str) -> str:
        """Clone a repository to local directory."""
        repo_name = repo_full_name.split('/')[-1]
        local_path = Path(f"repos/{repo_name}")
        
        # Create repos directory if it doesn't exist
        local_path.parent.mkdir(exist_ok=True)
        
        if local_path.exists():
            print(f"📁 Repository '{repo_name}' already exists locally")
            return str(local_path)
        
        try:
            print(f"📥 Cloning {repo_name}...")
            subprocess.run([
                "git", "clone", repo_clone_url, str(local_path)
            ], check=True, capture_output=True)
            print(f"✅ Successfully cloned {repo_name}")
            return str(local_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone {repo_name}: {e}")
            return ""
    
    def commit_to_repository(self, repo_path: str, repo_name: str) -> bool:
        """Make auto commit to a specific repository."""
        try:
            # Change to repository directory
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            # Run the auto commit script
            script_path = self.script_dir / "scripts" / "github_auto_commit.py"
            result = subprocess.run([
                sys.executable, str(script_path), 
                "--mode", "daily",
                "--config", str(self.script_dir / "configs" / "config.json")
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Successfully committed to {repo_name}")
                return True
            else:
                print(f"❌ Failed to commit to {repo_name}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error committing to {repo_name}: {e}")
            return False
        finally:
            # Return to original directory
            os.chdir(original_dir)
    
    def commit_to_all_repos(self):
        """Commit to all repositories."""
        print("\n🔄 Committing to ALL repositories...")
        print("-" * 40)
        
        success_count = 0
        total_count = len(self.repositories)
        
        for repo in self.repositories:
            print(f"\nProcessing: {repo['name']}")
            
            # Clone repository if needed
            repo_path = self.clone_repository(repo['full_name'], repo['clone_url'])
            if not repo_path:
                continue
            
            # Make commit
            if self.commit_to_repository(repo_path, repo['name']):
                success_count += 1
        
        print(f"\n📊 Summary: {success_count}/{total_count} repositories updated successfully")
    
    def commit_to_selected_repo(self):
        """Commit to a selected repository."""
        self.list_repositories()
        
        try:
            choice = int(input("\nEnter repository number: ")) - 1
            if 0 <= choice < len(self.repositories):
                selected_repo = self.repositories[choice]
                print(f"\n🎯 Selected: {selected_repo['name']}")
                
                # Clone repository if needed
                repo_path = self.clone_repository(
                    selected_repo['full_name'], 
                    selected_repo['clone_url']
                )
                
                if repo_path:
                    # Make commit
                    if self.commit_to_repository(repo_path, selected_repo['name']):
                        print("✅ Operation completed successfully!")
                    else:
                        print("❌ Commit operation failed")
                else:
                    print("❌ Failed to access repository")
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Please enter a valid number")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_menu(self):
        """Display main menu and handle user choices."""
        while True:
            self.print_header()
            print("📋 MAIN MENU")
            print("-" * 20)
            print("1. Authenticate with GitHub")
            print("2. List My Repositories")
            print("3. Commit to Specific Repository")
            print("4. Commit to ALL Repositories")
            print("5. View Saved Configuration")
            print("6. Exit")
            print()
            
            try:
                choice = input("Select option (1-6): ").strip()
                
                if choice == "1":
                    self.get_user_input()
                elif choice == "2":
                    if self.github_token:
                        self.list_repositories()
                    else:
                        print("❌ Please authenticate first (option 1)")
                elif choice == "3":
                    if self.github_token and self.repositories:
                        self.commit_to_selected_repo()
                    else:
                        print("❌ Please authenticate and list repositories first")
                elif choice == "4":
                    if self.github_token and self.repositories:
                        confirm = input("⚠️  This will commit to ALL repositories. Continue? (y/n): ")
                        if confirm.lower() == 'y':
                            self.commit_to_all_repos()
                    else:
                        print("❌ Please authenticate and list repositories first")
                elif choice == "5":
                    self.show_config()
                elif choice == "6":
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid option. Please try again.")
                
                if choice != "6":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")
    
    def show_config(self):
        """Display current configuration."""
        print("\n⚙️ Current Configuration:")
        print("-" * 30)
        print(f"Username: {self.github_username or 'Not set'}")
        print(f"Token: {'*' * 20 if self.github_token else 'Not set'}")
        print(f"Repositories: {len(self.repositories)} loaded")
        print(f"Config file: {self.config_file}")

def main():
    """Main entry point."""
    bot = GitHubAutoCommitBot()
    bot.show_menu()

if __name__ == "__main__":
    main()