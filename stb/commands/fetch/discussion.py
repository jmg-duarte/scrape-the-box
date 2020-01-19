import requests
import sys

from bs4 import BeautifulSoup

from stb.htb import DISCUSSION_URL
from stb.htb.comment import Comment
from stb.commands.fetch import io


def scrape(tid, output=sys.stdout, fmt="text"):
    comments = scrape_comments(tid)
    if not output:
        print_comments(comments)
    else:
        dump_comments(comments, output)


def print_comments(comments):
    for comment in comments:
        print(comment)


def dump_comments(comments, fname):
    with open(fname, "w") as file:
        io.write_file(comments, file)


def extract_page_comments(page_url):
    html = io.fetch_page(page_url)
    soup = BeautifulSoup(html, "html.parser")
    soup_comments = soup.find_all(class_="Comment")
    page_comments = []
    for c in soup_comments:
        page_comments.append(Comment.extract_comment(c))
        # print(f"{page_name} #{page}\n{comment}")
    return page_comments


def scrape_comments(thread_id):
    html = _get_discussion_page(thread_id)
    soup = BeautifulSoup(html, "html.parser")
    page_name = soup.find_all(class_="PageTitle", limit=1)[0].text
    print(page_name)
    soup_last_page = soup.find_all(class_="LastPage", limit=1)
    if not soup_last_page:
        last_page = 1
    else:
        last_page = int(soup_last_page[0].text)
    comments = []
    for page_number in range(1, last_page + 1):
        page_url = f"{DISCUSSION_URL}/{thread_id}/{page_name}/p{page_number}"
        page_comments = extract_page_comments(page_url)
        comments.extend(page_comments)
    return comments


def _get_discussion_page(tid):
    return io.fetch_page(f"{DISCUSSION_URL}/{tid}")
