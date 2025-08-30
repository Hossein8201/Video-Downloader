#!/usr/bin/env python3
"""
Main Entry Point for 7learn Video Downloader
Provides a unified interface for video scraping and download management
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from video_scraper import VideoScraper
from download_manager import DownloadManager
from config import *


def setup_logging():
    """Setup comprehensive logging for the main application."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / 'main.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def show_main_menu():
    """Display the main application menu."""
    print("\n" + "="*70)
    print("🎬 7learn Video Downloader - 7learn Video Download Manager")
    print("="*70)
    print("📁 Available videos: ", end="")
    
    # Check if download links file exists and count videos
    if os.path.exists(DOWNLOAD_LINKS_FILE):
        try:
            with open(DOWNLOAD_LINKS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                video_count = content.count('out=')
                print(f"{video_count}")
        except:
            print("0")
    else:
        print("0")
    
    print("\nChoose an option:")
    print("1. 🔍 Scrape Video Links")
    print("2. 📥 Download Management")
    print("3. ⚙️ Configuration")
    print("4. 📊 Project Status")
    print("5. 🆘 Help")
    print("0. ❌ Exit")
    
    choice = input("\nYour choice: ").strip()
    return choice


def scrape_videos():
    """Handle video scraping workflow."""
    print("\n🔍 Scraping Video Links")
    print("="*50)
    
    # Show current configuration
    print(f"📍 Base URL: {BASE_URL}")
    print(f"🎬 Video Range: {START_VIDEO_ID} - {END_VIDEO_ID}")
    print(f"📺 Starting: Season {STARTING_SEASON}, Episode {STARTING_EPISODE}")
    print(f"⏱️ Delay: {MIN_DELAY}-{MAX_DELAY} seconds")
    print(f"🔄 Max Retries: {MAX_RETRIES}")
    
    # Confirm before proceeding
    confirm = input("\nDo you want to continue? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return
    
    try:
        # Initialize scraper
        scraper = VideoScraper()
        
        # Start scraping
        print("\n🚀 Starting scraping...")
        videos = scraper.scrape_videos()
        
        if videos:
            # Save download links
            scraper.save_download_links(videos)
            print(f"\n🎉 Success!")
            print(f"✅ {len(videos)} videos extracted")
            print(f"📁 Links saved to: {DOWNLOAD_LINKS_FILE}")
        else:
            print("\n❌ No videos extracted")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        logging.error(f"Scraping error: {e}")


def manage_downloads():
    """Handle download management workflow."""
    if not os.path.exists(DOWNLOAD_LINKS_FILE):
        print("\n❌ Download links file not found!")
        print("💡 First extract video links")
        return
    
    print("\n📥 Download Management")
    print("="*50)
    
    # Initialize download manager
    downloader = DownloadManager()
    
    if not downloader.download_links:
        print("❌ No download links found in file")
        return
    
    # Run download manager
    downloader.run()


def show_configuration():
    """Display current configuration and allow basic modifications."""
    print("\n⚙️ Configuration")
    print("="*50)
    
    print("📋 Current settings:")
    print(f"  • Base URL: {BASE_URL}")
    print(f"  • Video Range: {START_VIDEO_ID} - {END_VIDEO_ID}")
    print(f"  • Starting Season: {STARTING_SEASON}")
    print(f"  • Starting Episode: {STARTING_EPISODE}")
    print(f"  • Seasons: {SEASON_EPISODES}")
    print(f"  • Destination_path: {DESTINATION_PATH}")
    print(f"  • Delay: {MIN_DELAY}-{MAX_DELAY} seconds")
    print(f"  • Timeout: {REQUEST_TIMEOUT} seconds")
    print(f"  • Max Retries: {MAX_RETRIES}")
    
    print("\n💡 To change settings, edit the config.py file")
    print("To change settings, edit the config.py file")
    
    print("\n🔐 Authentication cookies:")
    for key, value in AUTH_COOKIES.items():
        # Show only first 20 characters of sensitive data
        display_value = value[:20] + "..." if len(value) > 20 else value
        print(f"  • {key}: {display_value}")


def show_project_status():
    """Display project status and statistics."""
    print("\n📊 Project Status")
    print("="*50)
    
    # Check files
    files_status = {
        "config.py": "✅ Available",
        "video_scraper.py": "✅ Available", 
        "download_manager.py": "✅ Available",
        "requirements.txt": "✅ Available",
        "README.md": "✅ Available"
    }
    
    # Check generated files
    if os.path.exists(DOWNLOAD_LINKS_FILE):
        try:
            with open(DOWNLOAD_LINKS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                video_count = content.count('out=')
                files_status[DOWNLOAD_LINKS_FILE] = f"✅ Available ({video_count} videos)"
        except:
            files_status[DOWNLOAD_LINKS_FILE] = "⚠️ Error reading"
    else:
        files_status[DOWNLOAD_LINKS_FILE] = "❌ Not found"
    
    # Check log files
    log_files = ["scraper.log", "download_manager.log", "logs/main.log"]
    for log_file in log_files:
        if os.path.exists(log_file):
            files_status[log_file] = "✅ Available"
        else:
            files_status[log_file] = "❌ Not found"
    
    # Display status
    for file_path, status in files_status.items():
        print(f"  {file_path}: {status}")
    
    # Check dependencies
    print("\n📦 Dependencies:")
    try:
        import requests
        print("  • requests: ✅ Installed")
    except ImportError:
        print("  • requests: ❌ Not installed")
    
    try:
        import bs4
        print("  • beautifulsoup4: ✅ Installed")
    except ImportError:
        print("  • beautifulsoup4: ❌ Not installed")
    
    try:
        import pyperclip
        print("  • pyperclip: ✅ Installed")
    except ImportError:
        print("  • pyperclip: ❌ Not installed")


def show_help():
    """Display help information."""
    print("\n🆘 Help")
    print("="*50)
    
    help_text = """
📖 How to use:

1. 🔍 Extract Links:
   • Check settings in config.py
   • Update authentication cookies
   • Choose option 1

2. 📥 Download Videos:
   • After extracting links
   • Choose option 2
   • Choose your download manager

🔧 Configuration:
• Edit config.py file
• Change base URL, video range, and other settings

🚨 Important notes:
• Only download authorized content
• Use valid authentication cookies
• Configure delays to avoid being blocked

📁 Important files:
• config.py: Project configuration
• video_scraper.py: Link extraction
• download_manager.py: Download management
• logs/: Log files
"""
    
    print(help_text)


def main():
    """Main application entry point."""
    logger = setup_logging()
    logger.info("Application started")
    
    print("🎬 Welcome to 7learn Video Downloader!")
    print("Welcome to 7learn Video Downloader!")
    
    while True:
        try:
            choice = show_main_menu()
            
            if choice == '1':
                scrape_videos()
            elif choice == '2':
                manage_downloads()
            elif choice == '3':
                show_configuration()
            elif choice == '4':
                show_project_status()
            elif choice == '5':
                show_help()
            elif choice == '0':
                logger.info("Application exited by user")
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice!")
            
            if choice != '0':
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            print(f"\n❌ Unexpected error: {e}")
            print(f"Unexpected error: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
