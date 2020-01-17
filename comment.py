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

    @staticmethod
    def extract_comment(c):
        import scrapper
        username = c.find(class_="Username").text
        message = c.find(class_="Message").text
        permalink_html = c.find(class_="Permalink")
        permalink = permalink_html["href"]
        datetime = f"{scrapper.BASE_URL}/{permalink_html.time['datetime']}"
        # print(permalink)
        return Comment(username, message, datetime, permalink)
