import shutil
import os
from pathlib import Path
import click
import tempfile
from tinydb import Query
from titlecase import titlecase
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from lilyskel import yaml_interface, info, db_interface, mutopia, exceptions, lynames
from lilyskel.interface.common import instruments_with_indexes, InsensitiveCompleter, YNValidator, manual_instrument, \
    reorder_instruments, IndexValidator
from lilyskel.lynames import normalize_name
from .update_db_manually import db

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
    """Create the configuration file and set the directory"""
    if ".yaml" not in filename:
        filename = filename + ".yaml"
    filepath = Path(path, filename)
    if filepath.exists():
        overwrite = prompt("File exists. Overwrite? ", validator=YNValidator(),
                           default='N')
        if overwrite.lower()[0] == 'n':
            raise SystemExit(1)
        shutil.copy2(filepath, Path(str(filepath) + ".bak"))
    filepath.open("w").close()
    with open(PATHSAVE, "w") as savepath:
        savepath.write(str(filepath.absolute()))


@cli.command()
@click.option("-f", "--file-path", required=False,
                help="Path to yaml config file for project.")
@click.option("-d", "--db-path", required=False, default=None,
              help="Path to tinydb.")
def edit(file_path, db_path):
    """Create and edit piece information"""
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
                           "Would you like to copy the included one? ",
                           default='Y', validator=YNValidator())
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
    prompt_help = (
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
    command_list = ['header', 'instrument', 'ensemble', 'movement', 'print',
                    'quit', 'help']
    command_completer = WordCompleter(command_list)
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
    print(prompt_help)
    while 1:
        # DEBUG LINE
        print(infodict)
        try:
            ps1 = infodict["headers"].title
        except (AttributeError, KeyError, TypeError):
            ps1 = "Untitled"
        command = prompt(f"{ps1}> ", completer=command_completer)
        if len(command) == 0:
            continue
        if command[0].lower() == 'q':
            try:
                os.remove(PATHSAVE)
            except FileNotFoundError:
                pass
            raise SystemExit(0)
        elif command.lower().strip() == "help":
            print(prompt_help)
        elif "header" in command.lower():
            if "headers" not in infodict:
                infodict["headers"] = None
            infodict["headers"] = edit_header(infodict["headers"], db)
        elif command.lower()[0] == 'i':
            if "instruments" not in infodict:
                infodict["instruments"] = []
            infodict["instruments"] = edit_instruments(infodict["instruments"], db)
        elif command.lower()[0] == 'p':
            print(infodict)
        else:
            print(INVALID)


def edit_header(curr_headers, db):
    prompt_help = (
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
    print(prompt_help)
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
            yn = prompt("Current composer is {}. Would you like to change "
                        "it? ".format(curr_headers.composer.name), default='N',
                        validator=YNValidator())
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
            print(prompt_help)
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
    comp = prompt("Enter Composer: ", completer=InsensitiveCompleter(composers))
    matches = []
    for item in composers:
        if comp in item:
            matches.append(item)
    if matches:
        load = prompt(f"Would you like to load {comp} from the database? ",
                      default='Y', validator=YNValidator())
        if load.lower()[0] == 'y':
            if len(matches) > 1:
                for num, match in enumerate(matches):
                    print(f"{num}. {match}")
                choice = prompt("Please enter the number of the "
                                "matching composer or press [enter] if none match: ",
                                validator=IndexValidator(len(matches) - 1, allow_empty=True))
                if choice:
                    found = matches[int(choice[0])]
            else:
                found = matches[0]
            try:
                return info.Composer.load_from_db(found, db)
            except NameError:
                pass
    new_comp = info.Composer(comp)
    guess_short_name = new_comp.get_short_name()
    try:
        guess_mutopia_name = new_comp.get_mutopia_name(guess=True)
    except AttributeError:
        guess_mutopia_name = ''
    new_comp.shortname = prompt("Enter the abbreviated name of the composer: ",
                                default=guess_short_name)
    new_comp.mutopianame = prompt("Enter the mutopia formatted name of the composer "
                                  "or [enter] for none: ", default=guess_mutopia_name)
    while True:
        add_to_db = prompt("Would you like to add this composer to the database for easy usage next time? ",
                           default='Y')
        if len(add_to_db) > 0:
            break
    if add_to_db.lower()[0] == 'y':
        new_comp.add_to_db(db)
    return new_comp


def mutopia_prompt(db, curr_headers):
    licenses = mutopia._get_licenses()
    license_completer = WordCompleter(licenses)
    mu_headers = curr_headers.mutopiaheaders
    if mu_headers is None:
        source = prompt("Enter the source: ")
        style = prompt("Enter the style: ")
        print(license_ for license_ in licenses)
        license_ = prompt("Enter the license: ", completer=license_completer)
        while 1:
            try:
                mu_headers = info.MutopiaHeaders(source=source,
                                                 style=style, license=license_)
                break
            except exceptions.MutopiaError as err:
                if "style" in str(err):
                    style = prompt(
                        f"Style {style} not valid. Enter valid style: ")
                if "license" in str(err):
                    print("Invalid license")
                    print(license_ for license_ in licenses)
                    license_ = prompt("Enter valid license: ",
                                     completer=license_completer)
    prompt_help = (
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
    print(prompt_help)
    while 1:
        command = prompt("Mutopia Headers> ", completer=field_completer)
        if len(command) == 0:
            continue
        elif command.lower() == "done":
            return mu_headers
        elif command.lower() in ["maintainer", "maintainerEmail", "maintainerWeb",
                         "mutopiatitle", "mutopiapoet", "mutopiaopus", "date",
                         "moreinfo", "style", "license", "source"
                         ]:
            print("{} is {}".format(command, getattr(mu_headers, command, "blank")))
            new = prompt(f"Enter value for {command} or press enter to leave unchanged: ")
            if len(new) > 0:
                setattr(mu_headers, command, new)
        elif command[0].lower() == 'h':
            print(prompt_help)
        else:
            print(INVALID)


def edit_instruments(curr_instruments, db):
    if curr_instruments:
        print("These instruments are currently in the score: ")
        for ins in curr_instruments:
            print(ins)
    else:
        print("No instruments currently in score.")
    prompt_help = (
        "Options:\n"
        f"{BOLD}create{END} a new instrument\n"
        f"{BOLD}delete{END} an instrument\n"
        f"{BOLD}reorder{END} instruments\n"
        f"{BOLD}help{END} to view this message\n"
        f"{BOLD}done{END} to save and return to main prompt"
    )
    command_completer = WordCompleter(['create', 'delete', 'reorder', 'help', 'done'])
    instrument_names = db_interface.explore_table(db.table("instruments"),
                                                  search=("name", ""))
    instruments = [titlecase(' '.join(name.split('_')))
                   for name in instrument_names]
    print(prompt_help)
    while True:
        # DEBUG LINE
        print(curr_instruments)
        command = prompt("Instruments> ", completer=command_completer)
        if len(command) == 0:
            continue
        elif command.lower()[0] == 'c':
            new_ins = create_instrument(instruments, db)
            curr_instruments.append(new_ins)
        elif command.lower()[0:2] == 'de':
            while True:
                instruments_with_indexes(curr_instruments)
                del_idx = prompt("Enter the number of the instrument to delete or [enter] to "
                                 "finish: ") or None
                if del_idx is None:
                    break
                elif del_idx.isdigit():
                    curr_instruments.pop(int(del_idx))
                else:
                    print("Invalid index")
        elif command.lower()[0] == 'r':
            curr_instruments = reorder_instruments(curr_instruments)
        elif command.lower()[0] == 'h':
            print(prompt_help)
        elif command.lower()[0:2] == 'do':
            return curr_instruments


def create_instrument(instruments, db):
    ins_name_input = prompt("Enter the full instrument name: ",
                            completer=InsensitiveCompleter(instruments))
    while True:
        number = prompt("If the instrument has a number associated (e.g. Violin 2), "
                        "enter it or press [enter] to continue. ")or None
        if number is None:
            break
        if number.isdigit():
            number = int(number)
            break
        print("Invalid number")
    q = Query()
    matches = db.table('instruments').search(q['name'].test(lambda val: normalize_name(ins_name_input) in val))
    if matches:
        load = prompt(f"{ins_name_input} is in the database, would you like to load it? "
                      "[Y/n] ", default='Y', validator=YNValidator())
        if load.lower()[0] == 'y':
            if len(matches) < 2:
                return lynames.Instrument.load_from_db(normalize_name(ins_name_input), db, number=number)
            else:
                for num, ins in enumerate(matches):
                    # print(ins)
                    print(f"{num}: {ins['name']}, clef: {ins['clef']}, "
                          f"transposition: {ins['transposition']}")
                choice = prompt("Please enter the number of the "
                                "matching instrument or press [enter] if none match: ",
                                validator=IndexValidator(len(matches) - 1, allow_empty=True))
                if choice:
                    new_ins = matches[int(choice)]
                    if number:
                        new_ins['number'] = number
                    return lynames.Instrument.load(new_ins)
    return manual_instrument(number=number, db=db, name=ins_name_input)


# adding commands from other files
cli.add_command(db)
