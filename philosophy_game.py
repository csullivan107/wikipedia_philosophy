import requests
from bs4 import BeautifulSoup
import sys

links_visited = []

def get_random_wiki_title():
    """
    Get a random Wikipedia article title
    
    Returns:
        str: The URL path to a random Wikipedia article
    """
    random_url = "/wiki/Special:Random"
    try:
        response = requests.get(f"https://en.wikipedia.org{random_url}", allow_redirects=False)
        if response.status_code == 302:  # Wikipedia redirects to random article
            return response.headers['Location'].replace("https://en.wikipedia.org", "")
        return None
    except requests.RequestException:
        return None


def get_wiki_soup(article_title):
    """
    Get BeautifulSoup object for a Wikipedia article
    
    Args:
        article_title (str): The title of the Wikipedia article
        
    Returns:
        bs4.BeautifulSoup: Parsed Wikipedia page HTML
    """
    url = f"https://en.wikipedia.org{article_title}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    except Exception as e:
        print(f"Error processing page: {e}")
        return None


def get_first_paragraph(soup):
    """Get the first valid paragraph from Wikipedia article"""

    content = soup.find(id="mw-content-text")
    first_p = content.find('p', class_=False)
    return first_p

def get_links_from_paragraph(paragraph):
    """
    Extract all valid Wikipedia links from a paragraph that aren't in parentheses
    
    Args:
        paragraph (bs4.element.Tag): BeautifulSoup paragraph element
        
    Returns:
        list: List of Wikipedia article links found in the paragraph
    """
    if not paragraph:
        return []
        
    links = []
    for link in paragraph.find_all('a'):
        href = link.get('href', '')
        
        # Skip links inside parentheses
        parent_text = link.parent.text
        open_count = parent_text[:parent_text.find(link.text)].count('(')
        close_count = parent_text[:parent_text.find(link.text)].count(')')
        
        if open_count > close_count:  # Link is inside parentheses
            continue
            
        if href.startswith('/wiki/'):
            links.append(href)
            
    return links

def get_links_from_article(article_title):
    """
    Get all valid Wikipedia links from the first paragraph of an article
    
    Args:
        article_title (str): Title of the Wikipedia article
        
    Returns:
        list: List of Wikipedia article links found in the first paragraph
    """
    # Get the page content
    soup = get_wiki_soup(article_title)
    if not soup:
        return []
        
    # Get first paragraph
    first_p = get_first_paragraph(soup)
    
    # Extract links
    links = get_links_from_paragraph(first_p)
    
    return links

def is_philosophy_link(links):
    """
    Check if the first link in a list of Wikipedia links points to the Philosophy article
    
    Args:
        links (list): List of Wikipedia article links
        
    Returns:
        bool: True if first link is Philosophy article, False otherwise
    """
    if not links:
        return False
        
    first_link = links[0]
    # Check for exact match to avoid partial matches like 'Philosophy_of_logic'
    if first_link == '/wiki/Philosophy' and len(first_link) == 20:
        return True
    else:
        return False

def print_results(articles_visited, loop_flag):
    """
    Print summary of articles visited during the search
    
    Args:
        articles_visited (list): List of Wikipedia article links that were visited
    """
    print("\nSearch Results:")
    print(f"Visited {len(articles_visited)} articles:")
    for i, article in enumerate(articles_visited, 1):
        # Remove '/wiki/' prefix for cleaner output
        article_name = article.replace('/wiki/', '')
        print(f"{i}.\t{article_name}")
    if loop_flag:
        return None
    else:
        print(f"{len(articles_visited)+1}.\tPhilosophy")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_article = sys.argv[1]
    else:
        start_article_prompt = input("Enter Wikipedia article title: ")
    loop_flag = False

    if start_article_prompt == "r":
        start_article_title = get_random_wiki_title()
    else:
        start_article_title = "/wiki/" + start_article_prompt
    print(f"\nStarting search from: {start_article_title}")

    articles_visited = [start_article_title]
    visited_set = {start_article_title}  # For efficient lookup

    article_links = get_links_from_article(start_article_title)
    
    while not is_philosophy_link(article_links):
        if not article_links:  # No links found
            print("No valid links found - ending search")
            break
            
        # Get next article from first valid link
        next_article = article_links[0]

        # Check for loops
        if next_article in visited_set:
            print(f"Loop detected! Already visited {next_article}")
            loop_flag = True
            break
            
        # Get links from next article
        article_links = get_links_from_article(next_article)
        
        if next_article == '/wiki/Philosophy':
            print("Found \"Philosophy\"! | Search complete.")
            break
        else:
            print(f"Philosophy not found - continuing search to {next_article}")
            articles_visited.append(next_article)
            visited_set.add(next_article)  # Add to set for loop detection

    print_results(articles_visited, loop_flag)
    print("\n" + "="*50 + "\n")  # Separator between iterations

    print("Program complete")
