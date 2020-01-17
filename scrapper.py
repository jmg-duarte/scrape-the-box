import requests
from bs4 import BeautifulSoup

from comment import Comment

BASE_URL = "https://forum.hackthebox.eu/discussion/"


def scrape(thread_id):
    html = requests.get(f"{BASE_URL}{thread_id}").content
    soup = BeautifulSoup(html, 'html.parser')
    page_name = soup.find(class_="PageTitle").text
    print(page_name)
    last_page = int(soup.find(class_="LastPage").text)
    for page_number in range(1, last_page + 1):
        page_url = f"{BASE_URL}{thread_id}/{page_name}/p{page_number}"
        extract_page_comments(page_url)


def extract_page_comments(page_url):
    html = requests.get(page_url).content
    soup = BeautifulSoup(html, 'html.parser')
    soup_comments = soup.find_all(class_="Comment")
    page_comments = []
    for c in soup_comments:
        page_comments.append(extract_comment(c))
        # print(f"{page_name} #{page}\n{comment}")
    return page_comments


def extract_comment(c):
    username = c.find(class_="Username").text
    message = c.find(class_="Message").text
    permalink_html = c.find(class_="Permalink")
    permalink = permalink_html["href"]
    datetime = permalink_html.time["datetime"]
    # print(permalink)
    return Comment(username, message, datetime, permalink)


scrape(2427)
