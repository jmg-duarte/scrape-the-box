import requests
from bs4 import BeautifulSoup

from comment import Comment

BASE_URL = "https://forum.hackthebox.eu/discussion/"


def scrape(id):
    html = requests.get(f"{BASE_URL}{id}").content
    soup = BeautifulSoup(html, 'html.parser')
    page_name = soup.find(class_="PageTitle").text
    print(page_name)
    last_page = int(soup.find(class_="LastPage").text)
    for page in range(1, last_page + 1):
        target_url = f"{BASE_URL}{id}/{page_name}/p{page}"
        html = requests.get(target_url).content
        soup = BeautifulSoup(html, 'html.parser')
        comments = soup.find_all(class_="Comment")
        for c in comments:
            username = c.find(class_="Username").text
            message = c.find(class_="Message").text
            permalink_html = c.find(class_="Permalink")
            permalink = permalink_html["href"]
            datetime = permalink_html.time["datetime"]
            comment = Comment(username, message, datetime, permalink)
            print(f"{page_name} #{page}\n{comment}")


scrape(2427)
