class Comment(object):
    def __init__(self, author, message, datetime, permalink):
        self.author = author
        self.message = message
        self.datetime = datetime
        self.permalink = permalink

    def __str__(self) -> str:
        return (f"author: {self.author}\n"
                f"datetime: {self.datetime}\n"
                f"permalink: {self.permalink}\n"
                f"message: {self.message}")