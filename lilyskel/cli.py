import atexit
from pathlib import Path
import click
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename", required=True, help=(
    "Name of the configuration file."
))
@click.argument("path", default=".", help=(
        "path to new directory, defaults to current working directory."))
def init(filename, path):
    if ".yaml" not in filename:
        filename = filename + ".yaml"
    filepath = Path(path, filename)
    if filepath.exists():
        overwrite = prompt("File exists. Overwrite?[y/N] ")
        if not overwrite:
            raise SystemExit(1)
    filepath.open("w").close()


@cli.command()
def edit():
    with open
