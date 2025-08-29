# 🎬 Video Downloader

A professional, configurable video downloader for educational websites. Easily adaptable for different platforms and courses.

## ✨ Features

- **🔍 Smart Video Detection**: Multiple regex patterns for finding video URLs
- **📁 Organized Downloads**: Automatic season/episode naming (S01-E01-Title.mp4)
- **🚀 Multiple Download Managers**: Support for IDM, FDM, EagleGet, and clipboard
- **⚡ Rate Limiting Protection**: Built-in delays to avoid server blocking
- **📊 Comprehensive Logging**: Detailed logs for debugging and monitoring
- **🌍 Multi-language Support**: Persian and English interface
- **🔧 Easy Configuration**: Simple config file for different websites

## 📋 Requirements

- Python 3.7+
- Internet connection
- Valid authentication cookies for the target website

## 🚀 Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd 7learn-downloader
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the project** (see Configuration section below)

## ⚙️ Configuration

Edit `config.py` to customize the scraper for your needs:

### 🔗 Website Settings
```python
# Base URL for video pages
BASE_URL = "https://7learn.com/panel/video/"

# Video ID range to process
START_VIDEO_ID = 5504
END_VIDEO_ID = 5542

# Number of episodes in each season
SEASON_EPISODES = [13, 19, 6, 10, 10, 7]

# Starting season and episode
STARTING_SEASON = 3
STARTING_EPISODE = 1
```

### 🔐 Authentication
```python
# Your authentication cookies
AUTH_COOKIES = {
    "token": "your_token_here",
    "session_id": "your_session_id"
}
```

### 🎯 Video Detection
```python
# Regex patterns to find video URLs
VIDEO_URL_PATTERNS = [
    r'https://s3\.7learn\.com/[^"\s]+\.mp4',
    r'https://[^"\s]*\.mp4',
]

# CSS selectors for video titles
TITLE_SELECTORS = [
    'h1.t-heading',
    'h1',
    '.video-title'
]
```

### ⏱️ Performance Settings
```python
# Delay between requests (seconds)
MIN_DELAY = 3
MAX_DELAY = 7

# Request timeout (seconds)
REQUEST_TIMEOUT = 120

# Maximum retry attempts
MAX_RETRIES = 3
```

## 📖 Usage

### 1. **Scrape Video Links**
```bash
python video_scraper.py
```
This will:
- Scrape all videos in the configured range
- Extract video URLs and titles
- Save download links to `download_links.txt`
- Create debug HTML files for troubleshooting

### 2. **Download Videos**
```bash
python download_manager.py
```
Choose from:
- **IDM**: Internet Download Manager
- **FDM**: Free Download Manager  
- **EagleGet**: EagleGet Download Manager
- **Clipboard**: Copy links for any download manager
- **Browser**: Open links in web browser

## 🔧 Customization for Different Websites

### Example: Different Educational Platform
```python
# config.py
BASE_URL = "https://example.com/course/video/"
VIDEO_URL_PATTERNS = [
    r'https://cdn\.example\.com/[^"\s]+\.mp4',
    r'<video[^>]*src="([^"]*\.mp4)"',
]
TITLE_SELECTORS = [
    '.course-title',
    'h1',
    'title'
]
```

### Example: YouTube-like Platform
```python
# config.py
BASE_URL = "https://example.com/watch/"
VIDEO_URL_PATTERNS = [
    r'"url":"([^"]*\.mp4)"',
    r'<source[^>]*src="([^"]*\.mp4)"',
]
TITLE_SELECTORS = [
    '.video-title',
    'h1.title',
    'meta[property="og:title"]'
]
```

## 📁 Project Structure

```
7learn-downloader/
├── config.py              # Configuration file
├── video_scraper.py      # Video scraping module
├── download_manager.py    # Download manager interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── download_links.txt    # Generated download links
├── scraper.log          # Scraping logs
├── download_manager.log  # Download manager logs
└── debug_*.html         # Debug HTML files
```

## 🚨 Troubleshooting

### Common Issues

1. **"No video found" errors:**
   - Check if the website structure changed
   - Update `VIDEO_URL_PATTERNS` in config.py
   - Verify authentication cookies are valid

2. **Rate limiting:**
   - Increase `MIN_DELAY` and `MAX_DELAY` in config.py
   - Reduce `MAX_RETRIES` to avoid overwhelming the server

3. **Authentication issues:**
   - Update `AUTH_COOKIES` with fresh cookies
   - Check if the website requires login

4. **Download manager not found:**
   - Install the download manager
   - Add it to your system PATH
   - Use the "Clipboard" option instead

### Debug Mode

Enable debug HTML saving in `config.py`:
```python
SAVE_DEBUG_HTML = True
```

This creates `debug_{video_id}.html` files to inspect page content.

## 📝 Logs

The project creates detailed logs:
- `scraper.log`: Video scraping operations
- `download_manager.log`: Download manager activities

Check these files for detailed error information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect website terms of service and copyright laws.