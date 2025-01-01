# Website to GPT

A Python tool that converts your website content into GPT-friendly text files by scraping your sitemap. This tool is particularly useful for creating training data or knowledge bases for GPT models from your website content.

## Overview

Website to GPT automatically scrapes all pages listed in your website's sitemap.xml and converts them into clean text format. It handles JavaScript-rendered content and offers two output options:
- Individual text files for each page
- A single merged file with clear page separators

## Requirements

### System Requirements
- Python 3.6 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- selenium
- beautifulsoup4
- requests
- lxml

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/website-to-gpt.git
cd website-to-gpt
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python scrape.py
```

2. Choose your output preference:
   - Option 1: Individual text files (one per page)
   - Option 2: Single merged file with headers

3. Enter your sitemap URL when prompted (e.g., https://example.com/sitemap.xml)

## Output

### Individual Files Mode
- Creates separate .txt files for each webpage
- Files are saved in the `output` directory
- Filenames are derived from URL paths

### Merged File Mode
- Creates a single `merged_output.txt` file
- Each page's content is separated by headers
- Headers include the original page filename

## Features

- Handles JavaScript-rendered content
- Processes complete sitemaps
- Cleans and formats text content
- Supports both individual and merged output modes
- Headless browser operation
- Built-in rate limiting to prevent server overload

## Notes

- Ensure your website has a valid sitemap.xml
- Respect robots.txt and website terms of service
- Consider rate limiting for large websites
- Some websites may block automated access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.