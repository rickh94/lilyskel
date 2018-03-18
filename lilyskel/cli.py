import atexit
import shutil
import os
from pathlib import Path
import click
import tempfile
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from lilyskel import yaml_interface, info, db_interface, mutopia, exceptions

TEMP = tempfile.gettempdir()
PATHSAVE = Path(TEMP, "lilyskel_path")
BOLD = "\033[1m"
END = "\033[0m"
INVALID = "Command not recognized. Please try again."


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
    #print(config_path)
    help = (
        "\nYou can now add score information. Available modes are:\n"
        f"{BOLD}header:{END}\t\tadd title, composer, etc.\n"
        f"{BOLD}instrument:{END}\tadd/remove/re-order individual instruments "
        "in the score\n"
        f"{BOLD}ensemble:{END}\tadd an ensemble to the score\n"
        f"{BOLD}movement:{END}\tadd/remove movements (including time, key, "
        f"and tempo info\n"
        f"{BOLD}print:{END}\t\t print the current state of the score info.\n"
        f"{BOLD}quit:{END}\t\twrite out file and exit\n"
        f"{BOLD}help:{END}\t\tprint this message\n"
    )
    command_completer = WordCompleter(['header', 'instrument', 'ensemble', 'movement',
                                       'print', 'quit', 'help'])
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
        # DEBUG LINE
        print(infodict)
        try:
            command = prompt(piece["headers"].title + "> ")
        except (AttributeError, KeyError, TypeError):
            command = prompt("Untitled> ", completer=command_completer)
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
            if "headers" not in infodict:
                infodict["headers"] = None
            infodict["headers"] = edit_header(infodict["headers"], db)
        elif command.lower()[0] == 'i':
            edit_instruments(infodict, db)
        elif command.lower()[0] == 'p':
            print(infodict)
        else:
            print(INVALID)


def edit_header(curr_headers, db):
    help = (
        "You may edit any of the following headers:\n"
        "title\t\tcomposer\n"
        "dedication\tsubtitle\n"
        "subsubtitle\tpoet\n"
        "meter\t\tarranger\n"
        "tagline\t\tcopyright\n"
        "You may also enter \"mutopia\" to enter headers for submission"
        "to the mutopia project."
        "Enter \"print\" to print the current headers and \"done\" to finish"
        "and return to the main prompt."
    )
    print(help)
    titlewords = WordCompleter(db_interface.explore_table(
        db.table("titlewords"), search=("word", "")))
    field_completer = WordCompleter(["title", "composer", "subtitle", "subsubtitle",
                                     "poet", "meter", "arranger", "tagline", "copyright",
                                     "mutopia", "print", "done"])
    if curr_headers is None:
        composer = composer_prompt(db)
        title = prompt("Enter Title: ", completer=titlewords)
        curr_headers = info.Headers(title=title, composer=composer)
    while 1:
        # DEBUG LINE
        print(curr_headers)
        command = prompt("Headers> ", completer=field_completer)
        if len(command) == 0:
            continue
        field = command.lower().strip()
        if field == "title":
            title = prompt(
                "Current title is \"{}\" enter a new title or press "
                "enter to keep the current one: ".format(
                    curr_headers.title
                )
            )
            if len(title) != 0:
                curr_headers.title = title
        elif "comp" in field:
            yn = prompt("Current composer is {}. Would you like to change it? "
                        "[y/N] ".format(
                curr_headers.composer.name
            ), default='N')
            if yn.lower()[0] == 'y':
                curr_headers.composer = composer_prompt(db)
        elif field in ["dedication", "subtitle", "subsubtitle", "poet",
                       "meter", "arranger", "tagline", "copyright"]:
            print("{} is {}".format(field, getattr(curr_headers, field, "blank")))
            new = prompt(f"Enter value for {field} or press enter to leave unchanged: ")
            if len(new) > 0:
                setattr(curr_headers, field, new)
        elif "mutopia" in field:
            curr_headers.mutopiaheaders = mutopia_prompt(db, curr_headers)
        # Logistical commands
        elif field[0] == 'h':
            print(help)
        elif field[0] == 'p':
            print(curr_headers)
        elif field[0] == 'd':
            print("Saving headers")
            return curr_headers
        else:
            print(INVALID)


def composer_prompt(db):
    composers = db_interface.explore_table(db.table("composers"),
                                           search=("name", ""))
    composer_completer = WordCompleter(composers)
    comp = prompt("Enter Composer: ", completer=composer_completer)
    matches = []
    for item in composers:
        if comp in item:
            matches.append(item)
    if matches:
        load = prompt(f"{comp} is in the database, would you like to load it? "
                      "[Y/n] ", default='Y')
        if load.lower()[0] == 'y':
            if len(matches) > 1:
                for num, match in enumerate(matches):
                    print(f"{num}. {match}")
                while 1:
                    choice = prompt("Please enter the number of the "
                                    "matching composer or N if none match: ")
                    if len(choice) == 0:
                        continue
                    if choice[0].isdigit():
                        match = matches[int(choice[0])]
                        break
                    elif choice[0].lower() == 'n':
                        return info.Composer(comp)
            else:
                match = matches[0]
            return info.Composer.load_from_db(match, db)
    # TODO: add guessing of mutopianame etc.
    return info.Composer(comp)


def mutopia_prompt(db, curr_headers):
    licenses = mutopia._get_licenses()
    license_completer = WordCompleter(licenses)
    mu_headers = curr_headers.mutopiaheaders
    if mu_headers is None:
        source = prompt("Enter the source: ")
        style = prompt("Enter the style: ")
        print(license_ for license_ in licenses)
        license = prompt("Enter the license: ", completer=license_completer)
        while 1:
            try:
                mu_headers = info.MutopiaHeaders(source=source,
                                                 style=style, license=license)
                break
            except exceptions.MutopiaError as err:
                if "style" in str(err):
                    style = prompt(
                        f"Style {style} not valid. Enter valid style: ")
                if "license" in str(err):
                    print("Invalid license")
                    print(license_ for license_ in licenses)
                    license = prompt("Enter valid license: ",
                                     completer=license_completer)
    help = (
        "You may enter any of the following data or leave blank. "
        "Anything required and "
        "not collected will be filled with defaults or predictions:\n"
        "maintainer\tmaintainerEmail\n"
        "maintainerWeb\tmutopiatitle\n"
        "mutopiapoet\tmutopiaopus\n"
        "date\t\tmoreinfo\n"
        "You can also change the source, style, or license"
        "Type \"done\" to save and return to the previous screen."
    )
    field_completer = WordCompleter(["maintainer", "maintainerEmail", "maintainerWeb", "mutopiatitle",
                                     "mutopiapoet", "mutopiaopus", "date", "moreinfo",
                                     "source", "style", "license", "done"])
    print(help)
    while 1:
        command = prompt("Mutopia Headers> ", completer=field_completer)
        if len(command) == 0:
            continue
        elif command.lower() == "done":
            return mu_headers
        elif command in ["maintainer", "maintainerEmail", "maintainerWeb",
                         "mutopiatitle", "mutopiapoet", "mutopiaopus", "date",
                         "moreinfo", "style", "license", "source"
                         ]:
            print("{} is {}".format(command, getattr(mu_headers, command, "blank")))
            new = prompt(f"Enter value for {command} or press enter to leave unchanged: ")
            if len(new) > 0:
                setattr(mu_headers, command, new)
        else:
            print(INVALID)

