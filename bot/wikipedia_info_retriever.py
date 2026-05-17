from urllib import parse
import datetime
import logging
import requests

# 1. Define a compliant User-Agent header according to Wikipedia's policy
HEADERS = {
    "User-Agent": "ChuiniBot/1.0 (contact: munozfernandezandres@gmail.com) Python-Requests",
    "Accept-Encoding": "gzip"  # Explicitly tells Wikipedia you prefer compressed data
}

def get_random_link_from_wikipedia():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 10,  # Number of random pages to retrieve
        "rnnamespace": 0,  # Only retrieve pages in the main namespace
    }
    
    # Pass the headers parameter here
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Throws an error early if HTTP status is 4xx or 5xx
    
    data = response.json()
    pages = data["query"]["random"]
    logging.debug(pages)

    # Print the page titles and links
    links = list()
    for page in pages:
        title = page["title"]
        page_views = get_page_views(title)
        quoted_title = parse.quote(title)
        
        link = {
            "link": f"https://en.wikipedia.org/wiki/{quoted_title}",
            "title": title,
            "page_views": page_views,
        }
        links.append(link)
        
    links = sorted(links, key=lambda x: x["page_views"], reverse=True)
    logging.debug(links)
    return links


def get_page_views(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "pageviews",
    }
    
    # Pass the headers parameter here as well
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    total_views = 0
    pages_dict = data.get("query", {}).get("pages", {})
    
    # Wikipedia returns page IDs as dynamic keys (e.g. {"12345": {...}})
    for page_id, page_data in pages_dict.items():
        # Safeguard against pages without 'pageviews' field
        page_views = page_data.get("pageviews", {})
        if page_views:
            total_views += sum(views for views in page_views.values() if views is not None)
            
    return total_views


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    random_links = get_random_link_from_wikipedia()
    print(random_links)