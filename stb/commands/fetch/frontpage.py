import requests
import sys
import json
import sqlite3

from bs4 import BeautifulSoup

from typing import Iterable

from stb.htb import DISCUSSIONS_URL, db
from stb.htb.discussion import Discussion
from stb.commands.fetch import io


def scrape(output_file, all=False, fmt="text", db_name=None):
    frontpage_soup = fetch_frontpage_soup()
    if all:
        last_page = io.get_last_page_number(frontpage_soup)
        discussions = []
        for page in range(1, last_page + 1):
            frontpage_soup = fetch_frontpage_soup(page)
            discussions.extend(extract_discussions(frontpage_soup))
    else:
        discussions = extract_discussions(frontpage_soup)
    io.write_file(discussions, output_file, fmt)

    if db_name:
        db.conn_use(
            db_name,
            db.load_fts(),
            db.cursor_exec(
                db.cursor_create_discussions_table(),
                db.cursor_create_discussion_virtual_table(),
                db.cursor_insert_discussions(discussions),
                db.cursor_insert_virtual_discussions(discussions),
            ),
        )


def fetch_frontpage_soup(page_number=1):
    return io.fetch_page_soup(f"{DISCUSSIONS_URL}/p{page_number}")


def extract_discussions(soup):
    discussions = []
    for item in soup.find_all(class_="ItemDiscussion"):
        discussions.append(Discussion.from_item(item))
    return discussions
