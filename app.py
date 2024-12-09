from flask import Flask, render_template, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
import validators
from urllib.parse import urljoin, urlparse
import mimetypes

app = Flask(__name__)

def is_valid_url(url):
    return validators.url(url)

def is_media_file(url, media_type):
    mime_type = mimetypes.guess_type(url)[0]
    if not mime_type:
        return False
    if media_type == 'photos':
        return mime_type.startswith('image/')
    elif media_type == 'videos':
        return mime_type.startswith('video/')
    else:
        return mime_type.startswith(('image/', 'video/'))

def get_links(url, visited=None):
    if visited is None:
        visited = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(url, href)
                if urlparse(absolute_url).netloc == urlparse(url).netloc:
                    links.add(absolute_url)
        return links - visited
    except:
        return set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    media_type = data.get('mediaType')
    min_size = int(data.get('minSize', 0)) * 1024  # Convert KB to bytes
    max_total_size = int(data.get('maxTotalSize', 0)) * 1024 * 1024  # Convert MB to bytes
    depth = int(data.get('depth', 1))

    if not is_valid_url(url):
        return jsonify({'error': 'Invalid URL'}), 400

    visited = set()
    to_visit = {url}
    media_files = []
    total_size = 0
    current_depth = 0

    downloads_dir = os.path.expanduser('~/Downloads/web_scraper')
    os.makedirs(downloads_dir, exist_ok=True)

    while to_visit and current_depth <= depth:
        current_url = to_visit.pop()
        if current_url in visited:
            continue

        visited.add(current_url)
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find media files
            for tag in soup.find_all(['img', 'video', 'source']):
                src = tag.get('src') or tag.get('href')
                if src:
                    media_url = urljoin(current_url, src)
                    if is_media_file(media_url, media_type):
                        try:
                            head = requests.head(media_url)
                            file_size = int(head.headers.get('content-length', 0))
                            
                            if file_size >= min_size:
                                if max_total_size and (total_size + file_size) > max_total_size:
                                    continue

                                file_name = os.path.basename(urlparse(media_url).path)
                                if not file_name:
                                    continue

                                save_path = os.path.join(downloads_dir, file_name)
                                
                                media_response = requests.get(media_url)
                                with open(save_path, 'wb') as f:
                                    f.write(media_response.content)
                                
                                total_size += file_size
                                media_files.append({
                                    'url': media_url,
                                    'size': file_size,
                                    'path': save_path
                                })
                        except:
                            continue

            # Get new links to visit
            if current_depth < depth:
                new_links = get_links(current_url, visited)
                to_visit.update(new_links)

        except:
            continue

        current_depth += 1

    return jsonify({
        'message': f'Downloaded {len(media_files)} files',
        'files': media_files,
        'total_size': total_size
    })

if __name__ == '__main__':
    app.run(debug=True)
