import atexit
import shutil
import os
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
@click.argument("filename", required=True,
                # help=( "name of the configuration file for this project.")
)
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
        shutil.copy2(filepath, Path(str(filepath) + ".bak"))
    filepath.open("w").close()
    with open(PATHSAVE, "w") as savepath:
        savepath.write(str(filepath))


@cli.command()
@click.option("-f", "--file-path", required=False,
                help="Path to yaml config file for project.")
def edit(file_path):
    if not file_path:
        try:
            with open(PATHSAVE, "r") as savepath:
                file_path = Path(savepath.read())
        except FileNotFoundError:
            file_path = prompt("No path specified or saved. Please enter the path "
                   "to the config file. ")
    try:
        piece = yaml_interface.read_config(file_path)
    except (ValueError, FileNotFoundError):
        piece = None
    edit_prompt(piece, file_path)


def edit_prompt(piece, config_path):
    """
    edit_prompt is the prompt for editing the configuration in the command line
    :param piece: the data from the piece currently being worked on
    :param config_path: The path to the configuration file being worked on.
    :return:
    """
    print(config_path)
    help = (
        "You can now add score information. Available modes are:\n"
        "header: add title, composer, etc.\n"
        "instrument: add/remove/re-order individual instruments "
        "in the score\n"
        "ensemble: add an ensemble to the score\n"
        "movement: add/remove movements (including time, key, and tempo info\n"
        "quit: write out file and exit\n"
        "help: print this message\n"
    )
    try:
        opus = piece.opus
    except AttributeError:
        opus = prompt("Please enter an opus or catalog number or the piece: ")
    print(help)
    while 1:
        try:
            command = prompt(piece.headers.title + "> ")
        except AttributeError:
            command = prompt("Untitled> ")
        if command[0].lower() == 'q':
            os.remove(PATHSAVE)
            raise SystemExit(0)
