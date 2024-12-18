from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_first_link(article_title):
    # Get the Wikipedia page content
    url = f"https://en.wikipedia.org/wiki/{article_title}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the main content div
    content = soup.find(id="mw-content-text")
    
    # Look for the first valid link in paragraphs
    for paragraph in content.find_all('p', recursive=False):
        # Skip paragraphs that are empty or contain only brackets
        if not paragraph.text.strip() or paragraph.text.strip().startswith('('):
            continue
            
        for link in paragraph.find_all('a'):
            href = link.get('href', '')
            # Check if it's a valid wiki link
            if (href.startswith('/wiki/') 
                and not ':' in href 
                and not '#' in href
                and not 'Main_Page' in href):
                return href.split('/wiki/')[1], link.text
    
    return None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find_path')
def find_path():
    start_article = request.args.get('start', 'Cat')
    visited = []
    current = start_article
    path = []
    
    while current and len(path) < 30:  # Limit to prevent infinite loops
        path.append(current)
        if current == 'Philosophy':
            break
            
        next_link, link_text = get_first_link(current)
        if not next_link or next_link in visited:
            break
            
        visited.append(current)
        current = next_link
        
    return jsonify({'path': path})

if __name__ == '__main__':
    app.run(debug=True) 