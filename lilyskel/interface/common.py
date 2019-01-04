import tempfile
from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Validator, ValidationError
from titlecase import titlecase

from lilyskel import lynames, db_interface, info, yaml_interface
from lilyskel.lynames import VALID_CLEFS, normalize_name, Instrument, Ensemble


def instruments_with_indexes(instrumentlist):
    """Print a list of instruments numbered by their position in the list."""
    for idx, instrument in enumerate(instrumentlist):
        print(f"{idx}: {instrument.part_name()}")


class InsensitiveCompleter(Completer):
    """Complete without caring about case."""

    def __init__(self, word_list):

        self._word_list = set(word_list)

    def get_completions(self, document, complete_event):
        start = - len(document.text)
        for word in self._word_list:
            if document.text.lower() in word.lower():
                yield Completion(word, start_position=start)


class YNValidator(Validator):
    """Validates Yes/No responses in prompt_toolkit"""

    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if text.lower()[0] not in 'yn':
            raise ValidationError(message="Response must be [y]es or [n]o",
                                  cursor_position=0)


def answered_yes(answer):
    if answer.lower()[0] == 'y':
        return True
    return False


def manual_instrument(name, number, db=None):
    """
    Manually create an instrument by entering all the information.

    :param name: name of the instrument
    :param number: A Number associated with the instrument (e.g. Violin 2)
    :param db: Optional, database to add instrument to.
    :return:
    """
    print("Please enter instrument information (press enter for default).")
    insinfo = {}
    if number:
        insinfo['number'] = number
    insinfo['name'] = name
    insinfo['abbr'] = prompt("Abbreviation: ") or None
    while True:
        clef = prompt("Clef: ", completer=WordCompleter(VALID_CLEFS)).lower() or None
        if clef in VALID_CLEFS or clef is None:
            break
        print("invalid clef")
    insinfo['transposition'] = prompt("Transposition [enter for none]: ") or None
    if confirm('Is it a keyboard (grand staff) instrument?'):
        insinfo['keyboard'] = True
    else:
        insinfo['keyboard'] = False
    insinfo['midi'] = prompt("Midi instrument name: ").lower() or None
    insinfo['family'] = normalize_name(prompt("Instrument family: ")) or None
    new_ins = lynames.Instrument.load(insinfo)
    if db is not None:
        if confirm("Would you like to add this instrument to the database for "
                   "easy use next time? "):
            new_ins.add_to_db(db)
    return new_ins


def reorder_instruments(curr_instruments):
    """
    Dialog to remove and add instruments at certain indexes.
    :param curr_instruments: initial list of instruments
    :return: The list of instruments in the new order
    """
    while True:
        instruments_with_indexes(curr_instruments)
        tmp_instruments = [instrument for instrument in curr_instruments]
        old_idx = prompt("Enter the index of the instrument to move or [enter] to finish: ",
                         validator=IndexValidator(len(tmp_instruments) - 1)) or None
        if old_idx is None:
            break
        move_instrument = tmp_instruments.pop(int(old_idx))
        instruments_with_indexes(tmp_instruments)
        new_idx = prompt(f"Enter the index to insert {move_instrument.part_name()}: ",
                         validator=IndexValidator(len(tmp_instruments), allow_empty=False))
        tmp_instruments.insert(int(new_idx), move_instrument)
        print("New instrument order: ")
        instruments_with_indexes(tmp_instruments)
        correct = prompt("Is this correct? [Y/n] ", default='Y', validator=YNValidator())
        if answered_yes(correct):
            curr_instruments = [instrument for instrument in tmp_instruments]
    return curr_instruments


def create_ensemble(name, db, instruments_to_add=[]):
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


class IndexValidator(Validator):
    """Validates indexes of lists."""

    def __init__(self, max_len, allow_empty=True):
        self.max = max_len
        self.allow_empty = allow_empty

    def validate(self, document):
        text = document.text
        if not text and self.allow_empty:
            return
        try:
            idx = int(text)
        except ValueError:
            raise ValidationError(message="Input must be number",
                                  cursor_position=0)
        if idx > self.max:
            raise ValidationError(message="Index out of range",
                                  cursor_position=0)


def create_instrument(instruments, db, instrument_names_standardized):
    """
    Dialog for creating instruments
    :param instruments: instrument names for completion
    :param db: database to load or insert instruments
    :param instrument_names_standardized: standardized versions of instrument names
    for checking
    :return: new instrument object
    """
    ins_name_input = prompt("Enter the full instrument name: ",
                            completer=InsensitiveCompleter(instruments))
    while True:
        number = prompt("If the instrument has a number associated (e.g. Violin 2), "
                        "enter it or press [enter] to continue. ") or None
        if number is None:
            break
        if number.isdigit():
            number = int(number)
            break
        print("Invalid number")
    if '_'.join(ins_name_input.lower().split()) in \
            instrument_names_standardized:
        load = prompt(f"{ins_name_input} is in the database, would you like to load it? "
                      "[Y/n] ", default='Y', validator=YNValidator())
        if answered_yes(load):
            return lynames.Instrument.load_from_db(
                normalize_name(ins_name_input), db, number=number)
    return manual_instrument(number=number, db=db, name=ins_name_input)


BOLD = "\033[1m"
END = "\033[0m"
INVALID = "Command not recognized. Please try again."


class AppState:
    def __init__(self, db=None, piece=None, config_file_path=None, pathsave=None, mutopia_headers=None):
        self.db = db
        self.piece = piece
        self.config_file_path = config_file_path
        self.pathsave = pathsave
        self.mutopia_headers = mutopia_headers


TEMP = tempfile.gettempdir()
PATHSAVE = Path(TEMP, "lilyskel_path")


def save_config(piece, config_path, mutopia_headers):
    if mutopia_headers:
        piece.hedaers.add_mutopia_headers(mutopia_headers,
                                          instruments=piece.instruments)
    yaml_interface.write_config(config_path, piece)
