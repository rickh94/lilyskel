import atexit
from pathlib import Path
import click
import tempfile
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from lilyskel import yaml_interface

TEMP = tempfile.gettempdir()
PATHSAVE = Path(TEMP, "lilyskel_path")

@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename", required=True, help=(
    "Name of the configuration file for this project."
))
@click.option("--path", "-p", default=".", help=(
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
    with open(PATHSAVE, "w") as savepath:
        savepath.write(str(filepath))


@cli.command()
@click.option("-f", "--file", required=False,
                help="Path to yaml config file for project.")
def edit(filepath):
    if not filepath:
        with open(PATHSAVE, "r") as savepath:
            filepath = Path(savepath.read())
    try:
        piece = yaml_interface.read_config(filepath)
    except (ValueError, FileNotFoundError):
        piece = None
