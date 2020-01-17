import requests
from bs4 import BeautifulSoup

from stb.htb import BASE_URL
from stb.htb.discussion import Discussion


def get_frontpage():
    frontpage = requests.get(BASE_URL)
    if frontpage.status_code == 404:
        # TODO handle this better
        return None
    return frontpage


def scrape_frontpage():
    frontpage = get_frontpage()
    soup = BeautifulSoup(frontpage.content, 'html.parser')
    for item in soup.find_all(class_="ItemDiscussion"):
        print(Discussion.from_item(item))
