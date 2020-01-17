#!/bin/python3

import requests
import argparse

from bs4 import BeautifulSoup

from comment import Comment

BASE_URL = "https://forum.hackthebox.eu/discussion"


def scrape_comments(thread_id):
    html = requests.get(f"{BASE_URL}/{thread_id}").content
    soup = BeautifulSoup(html, 'html.parser')
    page_name = soup.find_all(class_="PageTitle", limit=1).text
    print(page_name)
    soup_last_page = soup.find_all(class_="LastPage", limit=1)
    if soup_last_page is None:
        last_page = 1
    else:
        last_page = int(soup_last_page.text)
    comments = []
    for page_number in range(1, last_page + 1):
        page_url = f"{BASE_URL}/{thread_id}/{page_name}/p{page_number}"
        page_comments = extract_page_comments(page_url)
        comments.extend(page_comments)
    return comments


def extract_page_comments(page_url):
    html = requests.get(page_url).content
    soup = BeautifulSoup(html, 'html.parser')
    soup_comments = soup.find_all(class_="Comment")
    page_comments = []
    for c in soup_comments:
        page_comments.append(Comment.extract_comment(c))
        # print(f"{page_name} #{page}\n{comment}")
    return page_comments


def get_args():
    parser = argparse.ArgumentParser(
        description="Scrape the Box is an automated tool to help you read all comments from a Hack the Box thread")
    parser.add_argument('id', type=str, help="thread id")
    parser.add_argument('-o', '--output', type=str, help="output file", metavar='file', required=False)
    args = parser.parse_args()
    # parser.add_argument('-p', help="The thread page number, use for a single page")
    return args


def main():
    args = get_args()
    comments = scrape_comments(args.id)
    if args.output is not None:
        with open(args.output, "w") as output_file:
            for comment in comments:
                output_file.write(str(comment))
        print(f"Written {len(comments)} comments to {args.output}")
    else:
        print(str(comments))


if __name__ == '__main__':
    main()
