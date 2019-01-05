from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from titlecase import titlecase

from lilyskel import info, db_interface, mutopia, lynames
from lilyskel.interface import common
from lilyskel.interface.common import (answered_yes, INVALID, BOLD, END)
from lilyskel.interface.custom_validators_completers import (InsensitiveCompleter, YNValidator, IndexValidator, LicenseValidator,
                                                             StyleValidator, ModeValidator, NoteValidator)
from lilyskel.interface.movement_commands import get_tempo_words

TEMPO_WORDS = []


def edit_prompt(piece, config_path, db, path_save):
    """
    edit_prompt is the prompt for editing the configuration in the command line
    :param piece: the data from the piece currently being worked on
    :param config_path: The path to the configuration file being worked on.
    :return:
    """
    prompt_help = (
        "\nYou can now add score information. Available modes are:\n"
        f"{BOLD}mutopia:{END}\tAdd information for submitting to the mutopia project\n"
        f"{BOLD}ensemble:{END}\tadd an ensemble to the score\n"
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
            "mutopia_headers": piece.headers.mutopiaheaders,
            "language": piece.language
        }
    if "opus" not in infodict:
        infodict["opus"] = prompt(
            "Please enter an opus or catalog number or the piece: ")
    print(prompt_help)
    while 1:
        # DEBUG LINE
        # print(infodict)
        try:
            ps1 = infodict["headers"].title
        except (AttributeError, KeyError, TypeError):
            ps1 = "Untitled"
        command = prompt(f"{ps1}> ", completer=command_completer)
        if len(command) == 0:
            continue
        elif command.lower()[0] == 'i':
            if "instruments" not in infodict:
                infodict["instruments"] = []
            infodict["instruments"] = existing_instruments(infodict["instruments"], db, instrument_prompt)
        elif command.lower()[0] == 'e':
            if "instruments" not in infodict:
                infodict["instruments"] = []
            infodict["instruments"] = existing_instruments(infodict["instruments"], db, ensemble_prompt)
        elif command.lower()[0:2] == 'mo':
            if "movements" not in infodict:
                infodict["movements"] = []
            infodict["movements"] = movement_prompt(infodict["movements"])
        elif command.lower()[0:2] == 'mu':
            if "mutopia_headers" not in infodict:
                infodict["mutopia_headers"] = None
            infodict['mutopia_headers'] = mutopia_prompt(infodict["mutopia_headers"])


def mutopia_prompt(curr_mutopia_headers):
    licenses = mutopia.get_licenses()
    styles = mutopia.get_styles()
    license_completer = WordCompleter(licenses)
    style_completer = WordCompleter(styles)
    mu_headers = curr_mutopia_headers
    if mu_headers is None:
        source = prompt("Enter the source: ")
        style = prompt("Enter the style: ", completer=style_completer, validator=StyleValidator())
        for license_ in licenses:
            print(license_)
        license_ = prompt("Enter the license: ", completer=license_completer, validator=LicenseValidator())
        mu_headers = info.MutopiaHeaders(source=source, style=style, license=license_)
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
        elif command.lower() == 'maintaineremail':
            print("maintainerEmail is {}".format(getattr(mu_headers, 'maintainerEmail', "blank")))
            new = prompt(f"Enter value for maintainerEmail or press [enter] to leave unchanged: ")
            if len(new) > 0:
                setattr(mu_headers, 'maintainerEmail', new)
        elif command.lower() == 'maintainerweb':
            print("maintainerWeb is {}".format(getattr(mu_headers, 'maitainerWeb', "blank")))
            new = prompt(f"Enter value for maintainerWeb or press [enter] to leave unchanged: ")
            if len(new) > 0:
                setattr(mu_headers, 'maintainerWeb', new)
        elif command.lower() in ["maintainer", "mutopiatitle", "mutopiapoet", "mutopiaopus", "date",
                         "moreinfo", "style", "license", "source"
                         ]:
            print("{} is {}".format(command, getattr(mu_headers, command, "blank")))
            new = prompt(f"Enter value for {command} or press [enter] to leave unchanged: ")
            if len(new) > 0:
                setattr(mu_headers, command, new)
        elif command[0].lower() == 'h':
            print(prompt_help)
        else:
            print(INVALID)


def existing_instruments(curr_instruments, db_, prompt_choice):
    """Deals with existing instruments/ensembles"""
    if isinstance(curr_instruments, lynames.Ensemble):
        print('Instruments have been entered as an ensemble: ')
        print(curr_instruments.pretty_name())
        for ins in curr_instruments.instruments:
            print(ins.part_name())
        while True:
            print(f"You can:\n{BOLD}break{END} the ensemble\n"
                  f"{BOLD}create{END} a new ensemble or\n"
                  f"{BOLD}edit{END} the ensemble or\n"
                  f"be {BOLD}done{END} and change nothing")
            choice = prompt('>')
            if choice.lower()[0] == 'b':
                return instrument_prompt(curr_instruments.instruments, db_)
            if choice.lower()[0] == 'c':
                return ensemble_prompt([], db_)
            if choice.lower()[0] == 'e':
                return ensemble_prompt(curr_instruments.instruments, db_)
            if choice.lower()[0] == 'd':
                return curr_instruments
            else:
                print(INVALID)
    elif curr_instruments:
        print("These instruments are currently in the score: ")
        for ins in curr_instruments:
            print(ins.part_name())
    else:
        print("No instruments currently in score.")
    return prompt_choice(curr_instruments, db_)


def ensemble_prompt(curr_instruments, db_):
    """
    Prompt for creating ensembles.

    :param curr_instruments: Current list of instruments.
    :param db_: database to load to/from
    :return: lynames.Ensemble object
    """
    ensemble_names = db_interface.explore_table(db_.table("ensembles"),
                                                search=("name", ""))
    ensembles = [titlecase(' '.join(name.split('_')))
                 for name in ensemble_names]
    ensemble_name = prompt("Please enter a name for the ensemble: ",
                           completer=InsensitiveCompleter(ensembles))
    ensemble_name_normal = lynames.normalize_name(ensemble_name)
    new_ens = None
    if ensemble_name_normal in ensemble_names:
        load = prompt(f"{ensemble_name} is in the database, would you like to load it? "
                      "[Y/n] ", default='Y', validator=YNValidator())
        if answered_yes(load):
            return lynames.Ensemble.load_from_db(ensemble_name, db_)
    while True:
        new_ens = common.create_ensemble(ensemble_name, db_, curr_instruments)
        if isinstance(new_ens, lynames.Ensemble):
            break
        else:
            retry = prompt(f"No new ensemble was created. Try again? ", validator=YNValidator(),
                           default='Y')
            if not answered_yes(retry):
                break
    return new_ens

