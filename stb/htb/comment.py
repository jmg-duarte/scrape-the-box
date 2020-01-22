from stb.htb import *


class Comment(object):
    def __init__(self, author, message, datetime, permalink):
        self.author = author
        self.message = message.strip()
        self.datetime = datetime
        self.permalink = permalink

    def __str__(self) -> str:
        return (
            f"---\n"
            f"author: {self.author}\n"
            f"datetime: {self.datetime}\n"
            f"permalink: {self.permalink}\n"
            f"message: {self.message}\n"
            f"---\n"
        )

    def __contains__(self, text_query):
        return text_query in self.message

    def as_tuple(self):
        return (self.author, self.message, self.datetime, self.permalink)

    @staticmethod
    def extract_comment(soup):
        username = soup.find(class_="Username").text
        message = soup.find(class_="Message").text
        permalink_html = soup.find(class_="Permalink")
        permalink = f"{BASE_URL}{permalink_html['href']}"
        datetime = f"{permalink_html.time['datetime']}"
        # print(permalink)
        return Comment(username, message, datetime, permalink)
