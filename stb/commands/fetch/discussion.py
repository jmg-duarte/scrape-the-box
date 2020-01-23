import requests
import sys

from bs4 import BeautifulSoup

from stb.htb import DISCUSSION_URL
from stb.htb.comment import Comment
from stb.htb import db
from stb.commands.fetch import io


def scrape(tid, output=sys.stdout, fmt="text", db_name=None):
    comments = scrape_comments(tid)
    io.write_file(comments, output, fmt)

    if db_name:
        db.conn_use(
            db_name,
            db.load_fts(),
            db.cursor_exec(
                db.cursor_create_comments_table(),
                db.cursor_create_comments_virtual_table(tid),
                db.cursor_insert_comments(comments),
                db.cursor_insert_virtual_comments(tid, comments),
            ),
        )


def scrape_comments(discussion_id):
    soup = io.fetch_page_soup(f"{DISCUSSION_URL}/{discussion_id}")
    page_name = _extract_page_name(soup)
    print(page_name)
    last_page = io.get_last_page_number(soup)
    comments = []
    for page_number in range(1, last_page + 1):
        soup = io.fetch_page_soup(
            f"{DISCUSSION_URL}/{discussion_id}/{page_name}/p{page_number}"
        )
        comments.extend(_scrape_comments(discussion_id, soup))
    return comments


def _scrape_comments(discussion_id, soup):
    soup_comments = soup.find_all(class_="Comment")
    page_comments = []
    for c in soup_comments:
        page_comments.append(Comment.extract_comment(discussion_id, c))
        # print(f"{page_name} #{page}\n{comment}")
    return page_comments


def _extract_page_name(soup):
    return soup.find_all(class_="PageTitle", limit=1)[0].text
