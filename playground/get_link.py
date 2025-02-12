import requests
from bs4 import BeautifulSoup
from pprint import pprint
import sys



links_visited = []

def article_dive(article_title):
    """
    Fetch and display the contents of a Wikipedia page
    
    Args:
        article_title (str): The title of the Wikipedia article
    """
    # Format the URL
    url = f"https://en.wikipedia.org/wiki/{article_title}"
    next_article = ""
    
    try:
        
        
        # Get the page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get basic info
        title = soup.find(id="firstHeading").text
        
        # Get the first paragraph
        content = soup.find(id="mw-content-text")
        first_p = content.find('p', class_=False)  # Skip paragraphs with classes (usually not main content)
        
        print("First Paragraph:")
        print(f"{first_p.text if first_p else 'No paragraph found'}\n")
        
        # Get all links in the first paragraph
        if first_p:
            print("Links in first paragraph:")
            list_of_links = []
            for link in first_p.find_all('a'):
                href = link.get('href', '')
                # Skip links inside parentheses
                parent_text = link.parent.text
                open_count = parent_text[:parent_text.find(link.text)].count('(')
                close_count = parent_text[:parent_text.find(link.text)].count(')')
                if open_count > close_count:  # Link is inside parentheses
                    continue
                if href.startswith('/wiki/'):
                    print(f"- {link.text} -> {href}")
                    #this is where I want to keep digging
                    list_of_links.append(href)
        
                    

        
            
        for link in links_visited: # check if we have been here before
            if next_article == link:
                print(f"Article Already Visited | Exiting Program")
                return links_visited
            elif next_article == "https://en.wikipedia.org/wiki/philosophy":
                print(f"Philosophy Found | Exiting Program")
                return links_visited
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"Error processing page: {e}")

def print_results(links):
    print("================================")
    print("\tResults")
    print("================================")
    print(f"Total Links Visited: {len(links_visited)}")
    print(f"Links Visited:")
    i=1
    for link in links_visited:
        print(f"\t{i} - {link}")
        i+=1


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        article_title = sys.argv[1]
    else:
        article_title = input("Enter Wikipedia article title: ")
    links = article_dive(article_title)
    print_results(links)