from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from titlecase import titlecase

from lilyskel import db_interface, info, lynames
from lilyskel.interface import common
from lilyskel.interface.common import BOLD, END, answered_yes
from lilyskel.interface.custom_validators_completers import (InsensitiveCompleter,
                                                             YNValidator)

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
        f"{BOLD}ensemble:{END}\tadd an ensemble to the score\n"
    )
    command_list = [
        "header",
        "instrument",
        "ensemble",
        "movement",
        "print",
        "quit",
        "help",
    ]
    command_completer = WordCompleter(command_list)
    infodict = {}
    if isinstance(piece, info.Piece):
        infodict = {
            "headers": piece.headers,
            "instruments": piece.instruments,
            "opus": piece.opus,
            "movements": piece.movements,
            "mutopia_headers": piece.headers.mutopiaheaders,
            "language": piece.language,
        }
    if "opus" not in infodict:
        infodict["opus"] = prompt(
            "Please enter an opus or catalog number or the piece: "
        )
    print(prompt_help)
    while 1:
        if len(command) == 0:
            continue


def ensemble_prompt(curr_instruments, db_):
    """
    Prompt for creating ensembles.

    :param curr_instruments: Current list of instruments.
    :param db_: database to load to/from
    :return: lynames.Ensemble object
    """
    ensemble_names = db_interface.explore_table(
        db_.table("ensembles"), search=("name", "")
    )
    ensembles = [titlecase(" ".join(name.split("_"))) for name in ensemble_names]
    ensemble_name = prompt(
        "Please enter a name for the ensemble: ",
        completer=InsensitiveCompleter(ensembles),
    )
    ensemble_name_normal = lynames.normalize_name(ensemble_name)
    new_ens = None
    if ensemble_name_normal in ensemble_names:
        load = prompt(
            f"{ensemble_name} is in the database, would you like to load it? " "[Y/n] ",
            default="Y",
            validator=YNValidator(),
        )
        if answered_yes(load):
            return lynames.Ensemble.load_from_db(ensemble_name, db_)
    while True:
        new_ens = common.create_ensemble(ensemble_name, db_, curr_instruments)
        if isinstance(new_ens, lynames.Ensemble):
            break
        else:
            retry = prompt(
                f"No new ensemble was created. Try again? ",
                validator=YNValidator(),
                default="Y",
            )
            if not answered_yes(retry):
                break
    return new_ens
