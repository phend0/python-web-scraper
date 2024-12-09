# Web Media Scraper

A web application that allows you to scrape and download media files (photos and videos) from websites with customizable parameters.

## Features

- Dark-themed, minimal user interface
- Download photos, videos, or both
- Set minimum file size for downloads
- Specify search depth (number of links to follow)
- Set maximum total download size
- Files are automatically saved to your Downloads folder

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Enter the website URL you want to scrape
4. Configure your preferences:
   - Select media type (photos, videos, or both)
   - Set minimum file size (in MB)
   - Set maximum total download size (in MB)
   - Choose how many links deep to search
5. Click "Start Scraping" and wait for the downloads to complete

## Notes

- Downloaded files will be saved to your Downloads folder in a "web_scraper" subdirectory
- The application respects website structures and only downloads media files
- Make sure you have permission to download content from the websites you're scraping
- Some websites may block automated requests
