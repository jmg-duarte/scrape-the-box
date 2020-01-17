import pprint
import requests
from bs4 import BeautifulSoup


class Comment(object):
    def __init__(self, author, message, datetime, permalink):
        self.author = author
        self.message = message
        self.datetime = datetime
        self.permalink = permalink

    def __str__(self) -> str:
        return (f"author: {self.author}\n"
                f"datetime: {self.datetime}\n"
                f"permalink: {self.permalink}\n"
                f"message: {self.message}")


url = "https://forum.hackthebox.eu/discussion/2427/traverxec"


def scrape():
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    page_name = soup.find(class_="PageTitle").text
    print(page_name)
    last_page = int(soup.find(class_="LastPage").text)
    for page in range(1, last_page + 1):
        target_url = f"https://forum.hackthebox.eu/discussion/2427/{page_name}/p{page}"
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


scrape()
