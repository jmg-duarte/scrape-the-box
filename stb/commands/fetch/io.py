import sys
import json
import requests

from bs4 import BeautifulSoup

from typing import Iterable


def write_file(iter: Iterable, file=sys.stdout, fmt="text"):
    if isinstance(file, str):
        with open(file, "w") as f:
            _write(iter, f, fmt)
    else:
        _write(iter, file, fmt)


def _write(iter: Iterable, file, fmt: str):
    if fmt == "text":
        iter = map(str, iter)
        for discussion in iter:
            file.write(discussion)
    elif fmt == "json":
        # TODO there has to be a better way to do this
        json.dump(iter, file, default=lambda x: x.__dict__, indent="    ")
    else:
        raise RuntimeError(f"unknown format: {fmt}")


def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 404:
        # TODO handle this better
        return None
    return response.content


def fetch_page_soup(url):
    """
    Fetches the page from 'url' and returns the respective 'soup'.
    """
    page = fetch_page(url)
    if page:
        return BeautifulSoup(page, "html.parser")
    return None


def get_last_page_number(soup) -> int:
    """
    Returns the last page. 

    If no class named 'LastPage' is found it returns 1.
    """
    soup_last_page = soup.find_all(class_="LastPage", limit=1)
    if soup_last_page:
        return int(soup_last_page[0].text)
    return 1
