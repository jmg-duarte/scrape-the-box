import requests
from stb.htb import BASE_URL
from stb.htb.comment import Comment
from bs4 import BeautifulSoup


def scrape_thread_comments(tid, output=None):
    comments = scrape_comments(tid)
    if output is None:
        print_comments(comments)
    else:
        dump_comments(comments, output)


def print_comments(comments):
    for comment in comments:
        print(comment)


def dump_comments(comments, fname):
    with open(fname, 'w') as file:
        for comment in comments:
            file.write(str(comment))


def get_page(tid):
    page = requests.get(f"{BASE_URL}/{tid}")
    if page.status_code == 404:
        # TODO handle this better
        return None
    return page


def scrape_comments(thread_id):
    html = get_page(thread_id).content
    soup = BeautifulSoup(html, 'html.parser')
    page_name = soup.find_all(class_="PageTitle", limit=1)[0].text
    print(page_name)
    soup_last_page = soup.find_all(class_="LastPage", limit=1)
    if not soup_last_page:
        last_page = 1
    else:
        last_page = int(soup_last_page[0].text)
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
