import tempfile
from pathlib import Path
from types import FunctionType
from typing import List, Any

from click import Context
from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter, Completer
from prompt_toolkit.shortcuts import confirm, radiolist_dialog
from tinydb import TinyDB
from titlecase import titlecase

from lilyskel import lynames, db_interface, yaml_interface
from lilyskel.info import Piece, MutopiaHeaders
from lilyskel.interface.custom_validators_completers import (InsensitiveCompleter, YNValidator, IndexValidator,
                                                             IsNumberValidator)
from lilyskel.lynames import VALID_CLEFS, normalize_name, Instrument, Ensemble


def instruments_with_indexes(instrumentlist):
    """Print a list of instruments numbered by their position in the list."""
    for idx, instrument in enumerate(instrumentlist):
        print(f"{idx}: {instrument.part_name()}")


def answered_yes(answer) -> bool:
    if answer.lower()[0] == 'y':
        return True
    return False


def manual_instrument(name: str, number: int, db=None) -> lynames.Instrument:
    """
    Manually create an instrument by entering all the information.

    :param name: name of the instrument
    :param number: A Number associated with the instrument (e.g. Violin 2)
    :param db: Optional, database to add instrument to.
    :return:
    """
    new_instrument_info = dict()
    new_instrument_info['number'] = number or None
    new_instrument_info['name'] = name
    new_instrument_info['abbr'] = prompt("Enter Abbreviation: ") or None
    while True:
        clef = prompt("Clef: ", completer=WordCompleter(VALID_CLEFS)).lower() or None
        if clef in VALID_CLEFS or clef is None:
            break
        print("invalid clef")
    new_instrument_info['transposition'] = prompt("Enter Transposition (or nothing): ") or None
    new_instrument_info['keyboard'] = confirm('Is it a keyboard (grand staff) instrument?')
    new_instrument_info['midi'] = prompt("Enter midi instrument name (or nothing): ").lower() or None
    new_instrument_info['family'] = normalize_name(prompt("Enter instrument family (or nothing): ")) or None
    new_ins = lynames.Instrument.load(new_instrument_info)
    if db and confirm("Would you like to add this instrument to the database for "
                      "easy use next time?"):
        new_ins.add_to_db(db)
    return new_ins


def reorder_instruments(curr_instruments) -> List[Instrument]:
    """
    Dialog to remove and add instruments at certain indexes.
    :param curr_instruments: initial list of instruments
    :return: The list of instruments in the new order
    """
    remove_index = radiolist_dialog(title="Reorder Instruments",
                                    text="Select instrument to move",
                                    values=[(index, instrument.part_name) for index, instrument in
                                            enumerate(curr_instruments)])
    if remove_index is None:
        return curr_instruments
    tmp_instruments = [instrument for instrument in curr_instruments]
    instrument_to_move = tmp_instruments.pop(remove_index)
    dialog_values = [(index, instrument.part_name) for index, instrument in enumerate(tmp_instruments)]
    # add extra option at end for inserting as last instrument
    dialog_values.append((len(tmp_instruments), 'Insert as Last Instrument'))
    insert_index = radiolist_dialog(title="Reorder Instruments",
                                    text=f"Select position to insert {instrument_to_move.part_name()}. It will go "
                                    f"before the selected instrument",
                                    values=dialog_values)
    if insert_index is None:
        return curr_instruments
    tmp_instruments.insert(int(insert_index), instrument_to_move)
    print_formatted_text("New instrument order: ")
    for instrument in tmp_instruments:
        print_formatted_text(HTML(f'<b>{instrument.part_name()}</b>'))
    if confirm("Is this new order correct?"):
        return tmp_instruments
    return curr_instruments


def create_ensemble(name: str, db: TinyDB, instruments_to_add: List[lynames.Instrument] = []) -> Ensemble:
    """
    Create an ensemble from new or old instruments

    :param name: The name of the ensemble
    :param db: the database to add the ensemble to and load instruments from.
    :param instruments_to_add: (Optional) existing instrument objects to add to
    the ensemble

    :return: ensemble object created by the dialog
    """
    instrument_names = db_interface.explore_table(db.table("instruments"),
                                                  search=("name", ""))
    instruments = [titlecase(' '.join(name.split('_')))
                   for name in instrument_names]
    ins_list = []
    new_ens = Ensemble(name)
    for ins in instruments_to_add:
        if isinstance(ins, Instrument):
            ins_list.append(ins)
            continue
        ins_name = ins
        num = None
        for group in ins.split():
            if group.isdigit():
                num = int(group)
                ins_name = ins.replace(f" {group}", '')
        if normalize_name(ins_name) in instrument_names:
            ins_list.append(Instrument.load_from_db(normalize_name(ins_name), db,
                                                    number=num))
        else:
            print(f"{ins_name} not in db")
    if not ins_list:
        print("You will need to create some instruments to add to the ensemble.")
        ins_list.append(create_instrument(instruments, db, instrument_names))
    prompt_help = ("You can:\n"
                   f"{BOLD}reorder{END}, {BOLD}add{END}, {BOLD}delete{END}, {BOLD}print{END}"
                   f"\nor {BOLD}done{END} if you are satisfied with the instruments.")
    print(prompt_help)
    instruments_with_indexes(ins_list)
    while True:
        choice = prompt("Ensemble> ", completer=WordCompleter(['reorder', 'add', 'delete', 'continue', 'print']), )
        if len(choice) == 0:
            continue
        elif choice.lower()[0] == 'r':
            ins_list = reorder_instruments(ins_list)
        elif choice.lower()[0] == 'a':
            ins_list.append(create_instrument(instruments, db, instrument_names))
        elif choice.lower()[0:2] == 'de':
            while True:
                instruments_with_indexes(ins_list)
                del_idx = prompt("Enter the number of the instrument to delete or [enter] to "
                                 "finish: ") or None
                if del_idx is None:
                    break
                elif del_idx.isdigit():
                    ins_list.pop(int(del_idx))
                else:
                    print("Invalid index")
        elif choice.lower()[0] == 'p':
            print(name + ':')
            instruments_with_indexes(ins_list)
        elif choice.lower()[0:2] == 'do':
            break
    for ins in ins_list:
        new_ens.add_instrument_from_obj(ins)
    print(new_ens)
    good = prompt("Save? ", validator=YNValidator(), default='Y')
    if not answered_yes(good):
        return ins_list
    add_to_db = prompt("Add to database for future use? ", validator=YNValidator(), default='Y')
    if answered_yes(add_to_db):
        new_ens.add_to_db(db)
    return new_ens


def create_instrument(obj) -> lynames.Instrument:
    """
    Dialog for creating instruments

    :param obj: context AppState object
    :return: new instrument object
    """
    normalized_instrument_names = return_state_data('normalized_instrument_names', obj, get_normalized_instrument_names)
    completer = obj.completers.get('instruments', generate_completer('instruments', obj, make_instrument_completer))
    ins_name_input = prompt("Enter the full instrument name: ",
                            completer=completer)
    number = prompt("Enter Number (e.g. Violin 2) or [enter] for no number: ", validator=IsNumberValidator())
    number = int(number) if number else None
    load_instrument_message = f"{ins_name_input} is in the database, would you like to load it?"
    if '_'.join(ins_name_input.lower().split()) in normalized_instrument_names and confirm(load_instrument_message):
        return lynames.Instrument.load_from_db(
            normalize_name(ins_name_input), obj.db, number=number)
    return manual_instrument(number=number, db=obj.db, name=ins_name_input)


BOLD = "\033[1m"
END = "\033[0m"
INVALID = "Command not recognized. Please try again."


class AppState:
    def __init__(self, db=None, piece=None, config_file_path=None, pathsave=None, mutopiaheaders=None, is_repl=False,
                 completers={}, data: dict = {}):
        self.db = db
        self.piece = piece
        self.config_file_path = config_file_path
        self.pathsave = pathsave
        self.mutopiaheaders = mutopiaheaders
        self.is_repl = is_repl
        self.completers = completers
        self.data = {}


TEMP = tempfile.gettempdir()
PATHSAVE = Path(TEMP, "lilyskel_path")


def return_state_data(key: str, obj: AppState, generate_data: FunctionType):
    def add_to_state_data():
        """Add arbitrary data to app state object"""
        data = generate_data(obj.db)
        obj.data[key] = data
        return data

    # get data from state dict, or generate and add to dict
    return obj.data.get(key, add_to_state_data())


def save_config(piece: Piece, config_path: Path, mutopiaheaders: MutopiaHeaders):
    if mutopiaheaders:
        piece.headers.add_mutopia_headers(mutopiaheaders,
                                          instruments=piece.instruments)
    yaml_interface.write_config(config_path, piece)


def save_non_interactive(ctx: Context):
    if not ctx.obj.is_repl:
        print_formatted_text(ctx.obj.piece.html())
        ask_to_save(ctx)


def ask_to_save(ctx: Context):
    if confirm(f'Would you like to save to {ctx.obj.config_file_path}?'):
        save_piece(ctx.obj)


def save_piece(obj: AppState):
    piece = obj.piece or Piece()
    config_path = obj.config_file_path or Path('./piece.yml')
    mutopiaheaders = obj.mutopiaheaders
    save_config(piece, config_path, mutopiaheaders)


def generate_completer(name: str, obj: AppState, get_completer: FunctionType) -> Completer:
    new_completer = get_completer(obj)
    obj.completers[name] = new_completer
    return new_completer


def get_normalized_instrument_names(db_):
    return db_interface.explore_table(db_.table("instruments"),
                                      search=("name", ""))


def get_instrument_names(obj):
    normalized_instrument_names = return_state_data('normalized_instrument_names',
                                                    obj,
                                                    get_normalized_instrument_names)
    return [titlecase(' '.join(name.split('_')))
            for name in normalized_instrument_names]


def make_instrument_completer(obj):
    instrument_names = get_instrument_names(obj)
    return InsensitiveCompleter(instrument_names)
