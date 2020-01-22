import re


class Discussion(object):
    __slots__ = ["title", "author", "views", "comments", "permalink", "id"]

    def __init__(self, title, author, views, comments, permalink):
        self.title = title.strip()
        self.author = author
        self.views = views
        self.comments = comments
        self.permalink = permalink
        self.id = Discussion._get_discussion_id(permalink)

    def __str__(self) -> str:
        return (
            f"---\n"
            f"id: {self.id}\n"
            f"title: {self.title}\n"
            f"author: {self.author}\n"
            f"views: {self.views}\n"
            f"comments: {self.comments}\n"
            f"permalink: {self.permalink}\n"
            f"---\n"
        )

    @staticmethod
    def _get_discussion_id(permalink):
        if permalink[-1] == "/":
            permalink = permalink[:-1]
        return permalink.split("/")[-2]

    @staticmethod
    def from_item(item):
        soup_discussion_title = item.div.div
        soup_discussion_info = soup_discussion_title.next_sibling.next_sibling
        title = soup_discussion_title.text
        author = soup_discussion_info.find(class_="DiscussionAuthor").text
        views = soup_discussion_info.find(class_="ViewCount").text
        comments = soup_discussion_info.find(class_="CommentCount").text
        permalink = soup_discussion_title.a["href"]
        return Discussion(title, author, views, comments, permalink)
