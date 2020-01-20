import requests
import sys

from bs4 import BeautifulSoup

from stb.htb import DISCUSSION_URL
from stb.htb.comment import Comment
from stb.commands.fetch import io


def scrape(tid, output=sys.stdout, fmt="text"):
    comments = scrape_comments(tid)
    io.write_file(comments, output, fmt)


def extract_discussion_comments(page_url):
    html = io.fetch_page(page_url)
    soup = BeautifulSoup(html, "html.parser")
    soup_comments = soup.find_all(class_="Comment")
    page_comments = []
    for c in soup_comments:
        page_comments.append(Comment.extract_comment(c))
        # print(f"{page_name} #{page}\n{comment}")
    return page_comments


def scrape_comments(discussion_id):
    html = fetch_discussion_page(discussion_id)
    soup = BeautifulSoup(html, "html.parser")
    page_name = soup.find_all(class_="PageTitle", limit=1)[0].text
    print(page_name)
    last_page = io.get_last_page_number(soup)
    comments = []
    for page_number in range(1, last_page + 1):
        page_url = f"{DISCUSSION_URL}/{discussion_id}/{page_name}/p{page_number}"
        page_comments = extract_discussion_comments(page_url)
        comments.extend(page_comments)
    return comments


def fetch_discussion_page(tid):
    return io.fetch_page(f"{DISCUSSION_URL}/{tid}")
