from datetime import timedelta
import datetime
import logging
from urllib import parse
import requests


def get_random_links_from_wikipedia():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageviews",
        "list": "random",
        "rnlimit": 10,  # Number of random pages to retrieve
        "rnnamespace": 0,  # Only retrieve pages in the main namespace
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data["query"]["random"]
    logging.debug(pages)

    # Print the page titles and links
    links = list()
    for page in pages:
        title = page["title"]
        page_views = get_page_views(title)
        title = parse.quote(title)
        link = {
            "link": f"https://en.wikipedia.org/wiki/{title}",
            "title": title,
            "page_views": page_views,
        }
        links.append(link)
    links = sorted(links, key=lambda link: link["page_views"], reverse=True)
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
    response = requests.get(url, params=params)
    data = response.json()

    total_views = 0
    for page in data["query"]["pages"]:
        for views in data["query"]["pages"][page]["pageviews"].values():
            if views != None:
                total_views += views
    return total_views


if __name__ == "__main__":
    random_links = get_random_links_from_wikipedia()
    print(random_links)
