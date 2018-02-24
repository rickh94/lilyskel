import atexit
import shutil
import os
from pathlib import Path
import click
import tempfile
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from lilyskel import yaml_interface, info, db_interface

TEMP = tempfile.gettempdir()
PATHSAVE = Path(TEMP, "lilyskel_path")
BOLD = "\033[1m"
END = "\033[0m"

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
@click.option("-d", "--db-path", required=False, default=None,
              help="Path to tinydb.")
def edit(file_path, db_path):
    if not file_path:
        try:
            with open(PATHSAVE, "r") as savepath:
                file_path = Path(savepath.read())
        except FileNotFoundError:
            file_path = prompt("No path specified or saved. Please enter the path "
                   "to the config file. ")
    try:
        piece = yaml_interface.read_config(Path(file_path))
    except (ValueError, FileNotFoundError, AttributeError):
        piece = None
    db = db_interface.init_db(db_path)
    tables = db_interface.explore_db(db)
    if "composers" not in tables or "instruments" not in tables:
        bootstrap = prompt("Lilyskel supports a small database to help with "
                           "commonly used items (such as instruments and "
                           "composers). You do not appear to have one. "
                           "Would you like to copy the included one? [Y/n]",
                           default='Y')
        if bootstrap.lower()[0] == 'y':
            db_interface.bootstrap_db(db_path)
    edit_prompt(piece, Path(file_path), db)


def edit_prompt(piece, config_path, db):
    """
    edit_prompt is the prompt for editing the configuration in the command line
    :param piece: the data from the piece currently being worked on
    :param config_path: The path to the configuration file being worked on.
    :return:
    """
    print(config_path)
    help = (
        "\nYou can now add score information. Available modes are:\n"
        f"{BOLD}header:{END}\t\tadd title, composer, etc.\n"
        f"{BOLD}instrument:{END}\tadd/remove/re-order individual instruments "
        "in the score\n"
        f"{BOLD}ensemble:{END}\tadd an ensemble to the score\n"
        f"{BOLD}movement:{END}\tadd/remove movements (including time, key, "
        f"and tempo info\n"
        f"{BOLD}quit:{END}\t\twrite out file and exit\n"
        f"{BOLD}help:{END}\t\tprint this message\n"
    )
    infodict = {}
    if isinstance(piece, info.Piece):
        infodict = {
            "headers": piece.headers,
            "instruments": piece.instruments,
            "opus": piece.opus,
            "movements": piece.movements,
        }
    if "opus" not in infodict:
        infodict["opus"] = prompt(
            "Please enter an opus or catalog number or the piece: ")
    print(help)
    while 1:
        try:
            command = prompt(piece["headers"].title + "> ")
        except (AttributeError, KeyError, TypeError):
            command = prompt("Untitled> ")
        if len(command) == 0:
            continue
        if command[0].lower() == 'q':
            try:
                os.remove(PATHSAVE)
            except FileNotFoundError:
                pass
            raise SystemExit(0)
        elif command.lower().strip() == "help":
            print(help)
        elif "header" in command.lower():
            edit_header(infodict, db)
        elif command.lower()[0] == 'i':
            edit_instruments(infodict, db)


def edit_header(infodict, db):
    help = (
        "You may edit any of the following headers:\n"
        "title\t\tcomposer\n"
        "dedication\t\tsubtitle\n"
        "subsubtitle\tpoet\n"
        "meter\t\tarranger\n"
        "tagline\t\tcopyright\n"
        "You may also enter \"mutopia\" to enter headers for submission"
        "to the mutopia project or \"done\" to finish."
    )
    titlewords = WordCompleter(db_interface.explore_table(
        db.table("titlewords"), search=("word", "")))
    if "headers" not in infodict:
        composer = composer_prompt(db)
        title = prompt("Enter Title: ", completer=titlewords)
        infodict["headers"] = info.Headers(title=title, composer=composer)
    while 1:
        # DEBUG LINE
        print(infodict["headers"])
        field = prompt("Headers> ")
        if len(field) == 0:
            continue
        if field.lower().strip() == "title":
            title = prompt(
                "Current title is \"{}\" enter a new title or press "
                "enter to keep the current one: ".format(
                    infodict["headers"].title
                )
            )
            if len(title) != 0:
                infodict["headers"].title = title
        elif "comp" in field.lower():
            yn = prompt("Current composer is {}. Would you like to change it? "
                        "[y/N] ".format(
                infodict["headers"].composer.name
            ), default='N')
            if yn.lower()[0] == 'y':
                infodict["headers"].composer = composer_prompt(db)
        # elif "mutopia" in field.lower():
        #     infodict["headers"].mutopiaheaders = mutopia_prompt(db, )


def composer_prompt(db):
    composers = db_interface.explore_table(db.table("composers"),
                                           search=("name", ""))
    composer_completer = WordCompleter(composers)
    comp = prompt("Enter Composer: ", completer=composer_completer)
    if comp in composers:
        load = prompt(f"{comp} is in the database, would you like to load it? "
                      "[Y/n] ", default='Y')
        if load.lower()[0] == 'y':
            return info.Composer.load_from_db(comp, db)
    # TODO: add guessing of mutopianame etc.
    return info.Composer(comp)

