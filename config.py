"""
Configuration file 
Easily configurable for different websites and courses
"""

# =============================================================================
# WEBSITE CONFIGURATION
# =============================================================================

# Base URL for the video pages
BASE_URL = "https://7learn.com/panel/video/"

# Video ID range to process
START_VIDEO_ID = 5627
END_VIDEO_ID = 5634

# Season configuration - number of episodes in each season
# Index 0 = Season 1, Index 1 = Season 2, etc.
SEASON_EPISODES = [19, 6, 10, 10, 7, 8]

# Starting season and episode (1-based indexing)
STARTING_SEASON = 6
STARTING_EPISODE = 1

# =============================================================================
# DOWNLOAD SETTINGS
# =============================================================================

# Output file for download links
DOWNLOAD_LINKS_FILE = "download_links.txt"

# Delay between requests to avoid rate limiting (in seconds)
MIN_DELAY = 3
MAX_DELAY = 7

# Request timeout (in seconds)
REQUEST_TIMEOUT = 120

# Maximum retry attempts for failed requests
MAX_RETRIES = 3

# =============================================================================
# AUTHENTICATION
# =============================================================================

# Authentication cookies (replace with your own)
AUTH_COOKIES = {
    "token": "186001%7CLfnfO2qDmQuQ4jEurnrp3QrHKM8uvCjBjcqe8vpz1d4a0159"
}

# User agent to mimic a real browser
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/127.0.0.0 Safari/537.36"
)

# =============================================================================
# VIDEO DETECTION PATTERNS
# =============================================================================

# Regex patterns to find video URLs in HTML
VIDEO_URL_PATTERNS = [
    r'https://s3\.7learn\.com/[^"\s]+\.mp4',  # Primary pattern for 7learn
]

# Title extraction patterns (CSS selectors)
TITLE_SELECTORS = [
    'h1',                     # Any h1 tag
]

# =============================================================================
# FILENAME SETTINGS
# =============================================================================

# Filename format: {season}-{episode}-{title}.mp4
FILENAME_FORMAT = "S{season:02d}-E{episode:02d}-{title}.mp4"

# Characters to replace in filenames (Windows safe)
FILENAME_REPLACE_CHARS = {
    '\\': '_', '/': '_', ':': '_', '*': '_', 
    '?': '_', '"': '_', '<': '_', '>': '_', '|': '_'
}

# =============================================================================
# DEBUG SETTINGS
# =============================================================================

# Save HTML content for debugging
SAVE_DEBUG_HTML = False

# Debug HTML filename format
DEBUG_HTML_FORMAT = "debug_{video_id}.html"

# Minimum HTML content length to consider page loaded
MIN_HTML_LENGTH = 1000