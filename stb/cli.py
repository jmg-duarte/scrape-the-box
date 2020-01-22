import click
import sys

from stb.commands.fetch import frontpage
from stb.commands.fetch import discussion


@click.group()
def cli():
    pass


@cli.command("search")
def search():
    """[WIP] Search downloaded pages."""
    print("search")


@cli.group("fetch")
def fetch():
    """Fetch a page."""


def print_all_warning(ctx, param, all):
    if all:
        r = click.confirm(
            (
                "This will scrape all discussions from the forum.\n"
                "Are you sure you want to continue?"
            ),
            default=False,
            show_default=True,
        )
        if not r:
            ctx.abort()
        return r


@fetch.command("front")
@click.option(
    "-f", "--fmt", "--format", type=click.Choice(["text", "json"]), default="text"
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
    """Fetch the frontpage."""
    frontpage.scrape(output, scrape_all, fmt)


@fetch.command("thread")
@click.argument("tid", type=str)
@click.option(
    "-f", "--fmt", "--format", type=click.Choice(["text", "json"]),
)
@click.option("-o", "--output", type=str, default=sys.stdout)
def fetch_thread(tid, output, fmt):
    """Fetch a discussion page."""
    discussion.scrape(tid, output, fmt)
