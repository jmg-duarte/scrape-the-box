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


def scrape(output):
    fp_discussions = scrape_frontpage()
    if output:
        with open(output, "w") as output_file:
            for discussion in fp_discussions:
                output_file.write(str(discussion))
    else:
        for discussion in fp_discussions:
            print(str(discussion))


def scrape_frontpage():
    frontpage = get_frontpage()
    soup = BeautifulSoup(frontpage.content, "html.parser")
    discussions = []
    for item in soup.find_all(class_="ItemDiscussion"):
        discussions.append(Discussion.from_item(item))
    return discussions
