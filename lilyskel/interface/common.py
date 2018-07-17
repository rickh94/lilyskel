from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from titlecase import titlecase

from lilyskel import lynames, db_interface
from lilyskel.lynames import VALID_CLEFS, normalize_name, Instrument, Ensemble


def instruments_with_indexes(instrumentlist):
    for idx, instrument in enumerate(instrumentlist):
        print(f"{idx}: {instrument.part_name()}")


class InsensitiveCompleter(Completer):
    def __init__(self, word_list):

        self._word_list = word_list

    def get_completions(self, document, complete_event):
        start = - len(document.text)
        for word in self._word_list:
            if document.text.lower() in word.lower():
                yield Completion(word, start_position=start)


class YNValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Respose Required", cursor_position=0)
        if text.lower()[0] not in 'yn':
            raise ValidationError(message="Response must be [y]es or [n]o",
                                  cursor_position=0)


def manual_instrument(name, number, db):
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
    insinfo['transposition'] = prompt("Transposition: ") or None
    keyboard_res = prompt("Is it a keyboard (grand staff) instrument? [y/N] ", default='N')
    insinfo['keyboard'] = False
    try:
        if keyboard_res.lower()[0] == 'y':
            insinfo['keyboard'] = True
    except IndexError:
        pass
    insinfo['midi'] = prompt("Midi instrument name: ").lower() or None
    insinfo['family'] = normalize_name(prompt("Instrument family: ")) or None
    new_ins = lynames.Instrument.load(insinfo)
    while True:
        add_to_db = prompt("Would you like to add this instrument to the database for"
                           "easy use next time? ", default='Y')
        if len(add_to_db) > 0:
            break
    if add_to_db.lower()[0] == 'y':
        new_ins.add_to_db(db)
    return new_ins


def reorder_instruments(curr_instruments):
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
        while True:
            correct = prompt("Is this correct? [Y/n] ", default='Y', validator=YNValidator())
            if len(correct) > 0:
                break
        if correct.lower()[0] == 'y':
            curr_instruments = [instrument for instrument in tmp_instruments]
    return curr_instruments


def create_ensemble(name, db, instruments_to_add):
    instrument_names = db_interface.explore_table(db.table("instruments"),
                                                  search=("name", ""))
    instruments = [titlecase(' '.join(name.split('_')))
                   for name in instrument_names]
    ins_list = []
    new_ens = Ensemble(name)
    for ins in instruments_to_add:
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
        ins_list.append(create_instrument(instruments, db, instrument_names))
    while True:
        instruments_with_indexes(ins_list)
        more_ins = prompt("Any more instruments? ", validator=YNValidator(), default='N')
        if more_ins.lower()[0] == 'n':
            break
        ins_list.append(create_instrument(instruments, db, instrument_names))
    instruments_with_indexes(ins_list)
    reorder = prompt("Would you like to reorder the instruments? ", default='N',
                     validator=YNValidator())
    if reorder.lower()[0] == 'y':
        ins_list = reorder_instruments(ins_list)
    for ins in ins_list:
        new_ens.add_instrument_from_obj(ins)
    return new_ens


class IndexValidator(Validator):
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
    if '_'.join(ins_name_input.lower().split()) in instrument_names_standardized:
        while True:
            load = prompt(f"{ins_name_input} is in the database, would you like to load it? "
                          "[Y/n] ", default='Y')
            if len(load) > 0:
                break
        if load.lower()[0] == 'y':
            return lynames.Instrument.load_from_db(normalize_name(ins_name_input), db, number=number)
    return manual_instrument(number=number, db=db, name=ins_name_input)