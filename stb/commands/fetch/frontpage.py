import requests
import sys
import json

from bs4 import BeautifulSoup

from typing import Iterable

from stb.htb import DISCUSSIONS_URL
from stb.htb.discussion import Discussion


def scrape(output, all=False, fmt="text"):
    frontpage = get_frontpage()
    if all:
        soup = BeautifulSoup(frontpage, "html.parser")
        last_page = get_last_page(soup)
        discussions = []
        for page in range(1, last_page + 1):
            frontpage = get_frontpage(page)
            soup = BeautifulSoup(frontpage, "html.parser")
            discussions.extend(get_discussions(soup))
    else:
        discussions = scrape_page_discussions(frontpage)
    dump_discussions(discussions, output, fmt=fmt)


def get_frontpage(page_number=1):
    frontpage = requests.get(f"{DISCUSSIONS_URL}/p{page_number}")
    if frontpage.status_code == 404:
        # TODO handle this better
        return None
    return frontpage.content


def scrape_page_discussions(page):
    soup = BeautifulSoup(page, "html.parser")
    last_page = get_last_page(soup)
    return get_discussions(soup)


def get_last_page(soup) -> int:
    soup_lpage = soup.find_all(class_="LastPage")
    if soup_lpage:
        return int(soup_lpage[0].text)
    return 1


def get_discussions(soup):
    discussions = []
    for item in soup.find_all(class_="ItemDiscussion"):
        discussions.append(Discussion.from_item(item))
    return discussions


def dump_discussions(discussions: Iterable[Discussion], file, fmt="text"):
    if file:
        with open(file, "w") as output_file:
            write_discussions(discussions, file=file, fmt=fmt)
    else:
        write_discussions(discussions, fmt=fmt)


def write_discussions(discussions: Iterable[Discussion], file=sys.stdout, fmt="text"):
    if fmt == "text":
        discussions = map(str, discussions)
        for discussion in discussions:
            file.write(discussion)
    elif fmt == "json":
        # TODO there has to be a better way to do this
        json.dump(discussions, file, default=lambda x: x.__dict__)
    else:
        raise RuntimeError(f"unknown format: {fmt}")
