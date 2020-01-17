from stb.htb import *


class Comment(object):
    def __init__(self, author, message, datetime, permalink):
        self.author = author
        self.message = message
        self.datetime = datetime
        self.permalink = permalink

    def __str__(self) -> str:
        return (f"---\n"
                f"author: {self.author}\n"
                f"datetime: {self.datetime}\n"
                f"permalink: {self.permalink}\n"
                f"message: {self.message}"
                f"---\n")

    def __contains__(self, text_query):
        return text_query in self.message

    @staticmethod
    def extract_comment(c):
        username = c.find(class_="Username").text
        message = c.find(class_="Message").text
        permalink_html = c.find(class_="Permalink")
        permalink = permalink_html["href"]
        datetime = f"{BASE_URL}/{permalink_html.time['datetime']}"
        # print(permalink)
        return Comment(username, message, datetime, permalink)
