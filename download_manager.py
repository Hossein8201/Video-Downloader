"""
Download Manager Module for 7learn Video Downloader
Handles sending video links to various download managers
"""

import os
import subprocess
import webbrowser
import time
import logging
from typing import List, Dict, Optional
from pathlib import Path

import pyperclip

from config import DESTINATION_PATH, DOWNLOAD_LINKS_FILE


class DownloadManager:
    """
    A clean and extensible download manager that can send video links
    to various download manager applications.
    """
    
    def __init__(self, links_file: str = None):
        """
        Initialize the download manager.
        
        Args:
            links_file: Path to the download links file
        """
        self.links_file = links_file or DOWNLOAD_LINKS_FILE
        self.download_links = []
        self._setup_logging()
        self.load_links()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('download_manager.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_links(self) -> None:
        """Load download links from the specified file."""
        if not os.path.exists(self.links_file):
            self.logger.error(f"File {self.links_file} not found!")
            print(f"❌ File {self.links_file} not found!")
            return
        
        self.logger.info(f"Reading {self.links_file}...")
        print(f"📖 Reading {self.links_file}...")
        
        try:
            with open(self.links_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse links and filenames
            lines = content.strip().split('\n')
            current_url = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('https://'):
                    current_url = line
                elif line.startswith('out=') and current_url:
                    filename = line[4:]  # Remove "out="
                    self.download_links.append({
                        'url': current_url,
                        'filename': filename
                    })
                    current_url = None
            
            self.logger.info(f"Loaded {len(self.download_links)} download links")
            print(f"✅ {len(self.download_links)} download links found")
            
        except Exception as e:
            self.logger.error(f"Failed to load links: {e}")
            print(f"❌ Error reading file: {e}")
    
    def show_menu(self) -> str:
        """Display the main menu and get user choice."""
        print("\n" + "="*60)
        print("🎬 7learn Download Manager")
        print("="*60)
        print(f"📁 Number of files: {len(self.download_links)}")
        print("\nChoose an option:")
        print("1. 📥 Download with IDM (Internet Download Manager)")
        print("2. 📋 Copy links to Clipboard")
        print("3. 🌍 Open links in browser")
        print("4. 📝 Show file list")
        print("5. 🔧 Download manager settings")
        print("0. ❌ Exit")
        
        choice = input("\nYour choice: ").strip()
        return choice
    
    def download_with_idm(self) -> None:
        """Send download links to Internet Download Manager."""
        if not self._validate_links():
            return
        
        self.logger.info("Starting download with IDM...")
        print("🚀 Starting download with IDM...")
        
        success_count = 0
        for i, item in enumerate(self.download_links, 1):
            try:
                # IDM command for download
                cmd = [
                    "idman",         # Run IDM
                    "/d",            # Add download link
                    item['url'],     # Video URL
                    "/f",            # Set output filename
                    item['filename'],# Output filename
                    "/p",            # Set destination path
                    DESTINATION_PATH,# Destination path
                    "/a"             # Add to download list
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info(f"IDM download queued: {item['filename']}")
                    print(f"✅ {i}/{len(self.download_links)}: {item['filename']}")
                    success_count += 1
                else:
                    self.logger.warning(f"IDM command failed: {result.stderr}")
                    print(f"❌ {i}/{len(self.download_links)}: Error in {item['filename']}")
                
                time.sleep(0.5)  # Wait between downloads
                
            except FileNotFoundError:
                self.logger.error("IDM not found in PATH")
                print("❌ IDM is not installed or not in PATH!")
                print("💡 Please install IDM or add its path to the system PATH")
                return
            except Exception as e:
                self.logger.error(f"Error with IDM: {e}")
                print(f"❌ Error downloading {item['filename']}: {e}")
        
        subprocess.run(["idman", "/s"])             # Start downloading lists
        
        self.logger.info(f"IDM download completed. {success_count}/{len(self.download_links)} queued")
        print(f"🎉 IDM download started! {success_count}/{len(self.download_links)} files")
    
    def copy_to_clipboard(self) -> None:
        """Copy download links to clipboard."""
        if not self._validate_links():
            return
        
        try:
            # Build text for clipboard
            clipboard_text = ""
            for item in self.download_links:
                clipboard_text += f"{item['url']}\n"
            
            pyperclip.copy(clipboard_text)
            
            self.logger.info(f"Copied {len(self.download_links)} links to clipboard")
            print(f"📋 {len(self.download_links)} links copied to Clipboard!")
            print("💡 Now you can paste them in your download manager")
            
        except ImportError:
            self.logger.error("pyperclip not installed")
            print("❌ pyperclip is not installed!")
            print("💡 Install it: pip install pyperclip")
        except Exception as e:
            self.logger.error(f"Failed to copy to clipboard: {e}")
            print(f"❌ Error copying: {e}")
    
    def open_in_browser(self) -> None:
        """Open download links in browser."""
        if not self._validate_links():
            return
        
        self.logger.info("Opening links in browser...")
        print("🌐 Opening links in browser...")
        
        success_count = 0
        for i, item in enumerate(self.download_links, 1):
            try:
                webbrowser.open(item['url'])
                self.logger.info(f"Opened in browser: {item['filename']}")
                print(f"✅ {i}/{len(self.download_links)}: {item['filename']}")
                success_count += 1
                time.sleep(1)  # Wait between opening tabs
                
            except Exception as e:
                self.logger.error(f"Failed to open {item['filename']}: {e}")
                print(f"❌ Error opening {item['filename']}: {e}")
        
        self.logger.info(f"Browser operation completed. {success_count}/{len(self.download_links)} opened")
        print(f"🎉 Links opened in browser! {success_count}/{len(self.download_links)} files")
    
    def show_file_list(self) -> None:
        """Display the list of files to be downloaded."""
        if not self._validate_links():
            return
        
        print("\n📋 File list:")
        print("-" * 80)
        
        for i, item in enumerate(self.download_links, 1):
            print(f"{i:2d}. {item['filename']}")
            print(f"    🔗 {item['url']}")
            print()
    
    def configure_download_manager(self) -> None:
        """Configure download manager paths and settings."""
        print("\n🔧 Download Manager Configuration")
        print("="*50)
        print("To configure download managers, add their paths to your system PATH.")
        print("\nDefault paths:")
        print("• IDM: C:\\Program Files (x86)\\Internet Download Manager\\")
        print("\nHow to add to PATH:")
        print("1. System Properties > Environment Variables")
        print("2. Edit PATH variable")
        print("3. Add the download manager folder path")
        print("4. Restart terminal/command prompt")
    
    def _validate_links(self) -> bool:
        """Validate that download links are available."""
        if not self.download_links:
            self.logger.warning("No download links available")
            print("❌ No download links available!")
            return False
        return True
    
    def run(self) -> None:
        """Main program execution loop."""
        if not self.download_links:
            self.logger.error("No download links found")
            print("❌ No download links found!")
            return
        
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.download_with_idm()
            elif choice == '2':
                self.copy_to_clipboard()
            elif choice == '3':
                self.open_in_browser()
            elif choice == '4':
                self.show_file_list()
            elif choice == '5':
                self.configure_download_manager()
            elif choice == '0':
                self.logger.info("User exited the program")
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice!")
            
            input("\nPress Enter to continue...")


def main():
    """Main function to run the download manager."""
    try:
        downloader = DownloadManager()
        downloader.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
