import click
import sys

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


def print_all_warning(ctx, param, all):
    if all:
        r = click.confirm(
            "This will scrape all discussions from the forum. Are you sure you want to continue?",
            default=False,
            show_default=True,
        )
        if not r:
            ctx.abort()
        return r


@fetch.command("front")
@click.option(
    "-f", "--fmt", "--format", type=click.Choice(["text", "json"]),
)
@click.option("-o", "--output", type=str, default=sys.stdout)
@click.option(
    "-a",
    "--all",
    "scrape_all",
    flag_value=True,
    is_flag=True,
    callback=print_all_warning,
)
def fetch_frontpage(output, scrape_all, fmt):
    frontpage.scrape(output, scrape_all, fmt)


@fetch.command("thread")
@click.argument("tid", type=str)
@click.option(
    "-f", "--fmt", "--format", type=click.Choice(["text", "json"]),
)
@click.option("-o", "--output", type=str)
def fetch_thread(tid, output, fmt):
    discussion.scrape(tid, output, fmt)
