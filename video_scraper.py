"""
Video Scraper Module
Handles video URL extraction and metadata parsing
"""

import os
import re
import time
import random
import logging
from typing import Optional, Tuple, Dict, List
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import *


class VideoScraper:
    """
    A clean and configurable video scraper for extracting video URLs and metadata
    from web pages.
    """
    
    def __init__(self):
        """Initialize the video scraper with configuration."""
        self.session = self._create_session()
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _create_session(self) -> requests.Session:
        """Create and configure a requests session."""
        session = requests.Session()
        
        # Set headers to mimic a real browser
        session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        
        # Set authentication cookies
        session.cookies.update(AUTH_COOKIES)
        
        return session
    
    def _is_page_loaded(self, html_content: str) -> bool:
        """Check if the page content is fully loaded."""
        return len(html_content) >= MIN_HTML_LENGTH
    
    def _save_debug_html(self, video_id: int, html_content: str) -> None:
        """Save HTML content for debugging purposes."""
        if not SAVE_DEBUG_HTML:
            return
        
        debug_filename = DEBUG_HTML_FORMAT.format(video_id=video_id)
        try:
            with open(debug_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.debug(f"Debug HTML saved to {debug_filename}")
        except Exception as e:
            self.logger.error(f"Failed to save debug HTML: {e}")
    
    def _extract_video_url(self, html_content: str) -> Optional[str]:
        """Extract video URL using configured patterns."""
        for pattern in VIDEO_URL_PATTERNS:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                # Handle capture groups in regex patterns
                video_url = matches[0] if isinstance(matches[0], str) else matches[0][0]
                self.logger.info(f"Video URL found using pattern: {pattern}")
                return video_url
        
        self.logger.warning("No video URL found with any pattern")
        return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract video title using configured selectors."""
        for selector in TITLE_SELECTORS:
            try:
                if selector.startswith('.'):
                    title_element = soup.select_one(selector)
                else:
                    title_element = soup.find(selector)
                
                if title_element and title_element.text.strip():
                    title = title_element.text.strip()
                    self.logger.info(f"Title extracted using selector: {selector}")
                    return self._sanitize_filename(title)
            except Exception as e:
                self.logger.debug(f"Failed to extract title with selector {selector}: {e}")
                continue
        
        self.logger.warning("No title found with any selector")
        return "Unknown_Title"
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for Windows compatibility."""
        for char, replacement in FILENAME_REPLACE_CHARS.items():
            filename = filename.replace(char, replacement)
        
        # Remove extra spaces and normalize
        filename = ' '.join(filename.split())
        return filename
    
    def _create_filename(self, season: int, episode: int, title: str) -> str:
        """Create standardized filename."""
        return FILENAME_FORMAT.format(
            season=season,
            episode=episode,
            title=title
        )
    
    def _handle_request_error(self, response: requests.Response, video_id: int) -> bool:
        """Handle HTTP request errors and return whether to retry."""
        if response.status_code != 200:
            self.logger.error(f"HTTP {response.status_code} for video {video_id}")
            return True
        
        if not self._is_page_loaded(response.text):
            self.logger.warning(f"Page content too short ({len(response.text)} chars) for video {video_id}")
            return True
        
        return False
    
    def get_video_info(self, video_id: int, season: int, episode: int) -> Optional[Tuple[str, str]]:
        """
        Extract video information from a video page.
        
        Args:
            video_id: The video ID to scrape
            season: The season number
            episode: The episode number
            
        Returns:
            Tuple of (video_url, filename) or None if failed
        """
        url = f"{BASE_URL}{video_id}"
        
        for attempt in range(MAX_RETRIES):
            try:
                self.logger.info(f"Attempt {attempt + 1}/{MAX_RETRIES} for video {video_id}")
                
                # Make request with timeout
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                
                # Check for errors
                if self._handle_request_error(response, video_id):
                    if attempt < MAX_RETRIES - 1:
                        delay = random.uniform(2, 4)
                        self.logger.info(f"Retrying in {delay:.1f} seconds...")
                        time.sleep(delay)
                        continue
                    return None
                
                # Parse HTML content
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Save debug HTML on last attempt
                if attempt == MAX_RETRIES - 1:
                    self._save_debug_html(video_id, response.text)
                
                # Extract video URL
                video_url = self._extract_video_url(response.text)
                if not video_url:
                    if attempt < MAX_RETRIES - 1:
                        delay = random.uniform(2, 4)
                        self.logger.info(f"Retrying in {delay:.1f} seconds...")
                        time.sleep(delay)
                        continue
                    return None
                
                # Extract title
                title = self._extract_title(soup)
                
                # Create filename
                filename = self._create_filename(season, episode, title)
                
                self.logger.info(f"Successfully extracted video {video_id}: {filename}")
                return video_url, filename
                
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout on attempt {attempt + 1} for video {video_id}")
                if attempt < MAX_RETRIES - 1:
                    delay = random.uniform(5, 8)
                    self.logger.info(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                    continue
            except Exception as e:
                self.logger.error(f"Error on attempt {attempt + 1} for video {video_id}: {e}")
                if attempt < MAX_RETRIES - 1:
                    delay = random.uniform(2, 4)
                    self.logger.info(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                    continue
        
        self.logger.error(f"All attempts failed for video {video_id}")
        return None
    
    def scrape_videos(self) -> List[Dict[str, str]]:
        """
        Scrape all videos in the configured range.
        
        Returns:
            List of dictionaries containing video information
        """
        videos = []
        season = STARTING_SEASON
        episode = STARTING_EPISODE
        
        self.logger.info(f"Starting video scraping from ID {START_VIDEO_ID} to {END_VIDEO_ID}")
        
        for video_id in range(START_VIDEO_ID, END_VIDEO_ID + 1):
            video_info = self.get_video_info(video_id, season, episode)
            
            if video_info:
                video_url, filename = video_info
                videos.append({
                    'url': video_url,
                    'filename': filename,
                    'video_id': video_id,
                    'season': season,
                    'episode': episode
                })
                
                self.logger.info(f"✅ Found: {filename}")
            else:
                self.logger.warning(f"⚠️ Failed to extract video {video_id}")
            
            # Update episode and season counters
            episode += 1
            if episode > SEASON_EPISODES[season - 1]:
                episode = 1
                season += 1
                if season > len(SEASON_EPISODES):
                    self.logger.warning("Season count exceeded configured seasons")
                    break
            
            # Add delay between requests
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            self.logger.info(f"Waiting {delay:.1f} seconds before next request...")
            time.sleep(delay)
        
        self.logger.info(f"Scraping completed. Found {len(videos)} videos.")
        return videos
    
    def save_download_links(self, videos: List[Dict[str, str]], filename: str = None) -> None:
        """
        Save download links to a file for use with download managers.
        
        Args:
            videos: List of video dictionaries
            filename: Output filename (uses config default if None)
        """
        if filename is None:
            filename = DOWNLOAD_LINKS_FILE
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for video in videos:
                    f.write(f"{video['url']}\n")
                    f.write(f"  out={video['filename']}\n\n")
            
            self.logger.info(f"Download links saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save download links: {e}")


def main():
    """Main function to run the video scraper."""
    scraper = VideoScraper()
    videos = scraper.scrape_videos()
    
    if videos:
        scraper.save_download_links(videos)
        print(f"\n🎉 Successfully scraped {len(videos)} videos!")
        print(f"📁 Download links saved to {DOWNLOAD_LINKS_FILE}")
    else:
        print("\n❌ No videos were scraped successfully.")


if __name__ == "__main__":
    main()
