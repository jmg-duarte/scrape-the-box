import click

from stb.commands.fetch import frontpage
from stb.commands.fetch import discussion


@click.group()
def cli():
    pass


@cli.command("search")
def search():
    print("search")


@cli.group("fetch")
def fetch():
    """Fetches pages"""


@fetch.command("front")
@click.option("-o", "--output", type=str, flag_value=None)
def fetch_frontpage(output):
    frontpage.scrape(output)


@fetch.command("thread")
@click.argument("tid", type=str)
@click.option("-o", "--output", type=str, flag_value=None)
# @click.option('-f', '--format', flag_value="text", default=True)
def fetch_thread(tid, output):
    discussion.scrape(tid, output)
