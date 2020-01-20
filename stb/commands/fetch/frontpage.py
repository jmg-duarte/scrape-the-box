import requests
import sys
import json

from bs4 import BeautifulSoup

from typing import Iterable

from stb.htb import DISCUSSIONS_URL
from stb.htb.discussion import Discussion
from stb.commands.fetch import io


def scrape(output_file, all=False, fmt="text"):
    frontpage = fetch_frontpage()
    if all:
        soup = BeautifulSoup(frontpage, "html.parser")
        last_page = io.get_last_page_number(soup)
        discussions = []
        for page in range(1, last_page + 1):
            frontpage = fetch_frontpage(page)
            discussions.extend(scrape_page_discussions(frontpage))
    else:
        discussions = scrape_page_discussions(frontpage)
    io.write_file(discussions, output_file, fmt)


def fetch_frontpage(page_number=1):
    return io.fetch_page(f"{DISCUSSIONS_URL}/p{page_number}")


def scrape_page_discussions(page):
    soup = BeautifulSoup(page, "html.parser")
    return get_discussions(soup)


def get_discussions(soup):
    discussions = []
    for item in soup.find_all(class_="ItemDiscussion"):
        discussions.append(Discussion.from_item(item))
    return discussions
