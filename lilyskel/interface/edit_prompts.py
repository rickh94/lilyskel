import bs4
import os
import requests
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from titlecase import titlecase

from lilyskel import info, yaml_interface, db_interface, mutopia, exceptions, lynames
from lilyskel.interface import common
from lilyskel.interface.common import YNValidator, InsensitiveCompleter, IndexValidator, create_instrument, \
    instruments_with_indexes, reorder_instruments, answered_yes, INVALID, BOLD, END

TEMPO_WORDS = []


def edit_prompt(piece, config_path, db, path_save):
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
        f"{BOLD}language:{END} set the region language for lilypond\n"
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
            save = prompt("Save file before exiting? ", default='Y', validator=YNValidator())
            if save:
                new_piece = info.Piece.init_version(
                    headers=infodict['headers'],
                    instruments=infodict['instruments'],
                    language=infodict.get('language', None),
                    opus=infodict["opus"],
                    movements=infodict.get('movements', None)
                )
                yaml_interface.write_config(config_path, new_piece)
            try:
                os.remove(path_save)
            except FileNotFoundError:
                pass
            raise SystemExit(0)
        elif command.lower().strip() == "help":
            print(prompt_help)
        elif "header" in command.lower():
            if "headers" not in infodict:
                infodict["headers"] = None
            infodict["headers"] = header_prompt(infodict["headers"], db)
        elif command.lower()[0] == 'i':
            if "instruments" not in infodict:
                infodict["instruments"] = []
            infodict["instruments"] = existing_instruments(infodict["instruments"], db, instrument_prompt)
        elif command.lower()[0] == 'e':
            if "instruments" not in infodict:
                infodict["instruments"] = []
            infodict["instruments"] = existing_instruments(infodict["instruments"], db, ensemble_prompt)
        elif command.lower()[0] == 'm':
            if "movements" not in infodict:
                infodict["movements"] = []
            infodict["movements"] = movement_prompt(infodict["movements"])
        elif command.lower()[0] == 'l':
            infodict["language"] = prompt("Enter Lilypond Language: ",
                                          completer=WordCompleter(info.get_valid_languages()),
                                          validator=LanguageValidator())
        elif command.lower()[0] == 'p':
            print(infodict)
        else:
            print(INVALID)


class LanguageValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in info.get_valid_languages():
            raise ValidationError(message="Invalid language", cursor_position=0)


def header_prompt(curr_headers, db):
    prompt_help = (
        "You may edit any of the following headers:\n"
        "title\t\tcomposer\n"
        "dedication\tsubtitle\n"
        "subsubtitle\tpoet\n"
        "meter\t\tarranger\n"
        "tagline\t\tcopyright\n"
        "You may also enter \"mutopia\" to enter headers for submission"
        "to the mutopia project.\n"
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
        elif field[0] == 'save':
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


def instrument_prompt(curr_instruments, db_):
    """
    Prompt for creating instruments in the score.
    :param curr_instruments: list of existing instruments
    :param db_: database to laod to/from
    :return:
    """
    prompt_help = (
        "Options:\n"
        f"{BOLD}print{END} instruments\n"
        f"{BOLD}create{END} a new instrument\n"
        f"{BOLD}delete{END} an instrument\n"
        f"{BOLD}reorder{END} instruments\n"
        f"{BOLD}help{END} to view this message\n"
        f"{BOLD}done{END} to save and return to main prompt"
    )
    command_completer = WordCompleter(['create', 'delete', 'reorder', 'help', 'done', 'print'])
    instrument_names = db_interface.explore_table(db_.table("instruments"),
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
        elif command.lower()[0] == 'p':
            for ins in curr_instruments:
                print(ins.part_name(key=True))
        elif command.lower()[0] == 'c':
            new_ins = create_instrument(instruments, db_, instrument_names)
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


def print_movements(mov_list):
    for mov in mov_list:
        print(f"{mov.num}. {mov.tempo} in {mov.key.note} {mov.key.mode}")


def get_tempo_words():
    global TEMPO_WORDS
    if TEMPO_WORDS:
        return TEMPO_WORDS
    wiki = requests.get('https://en.wikipedia.org/wiki/Tempo')
    wiki_soup = bs4.BeautifulSoup(wiki.text, "html.parser")
    tempos = []
    for title in ['Basic_tempo_markings', 'French_tempo_markings',
                  'German_tempo_markings']:
        title = wiki_soup.find(id=title)
        tempos_soup = title.find_next('ul')
        tempos_temp = []
        for item in tempos_soup.find_all('i'):
            tempos_temp.extend(titlecase(item.text).split(' '))
        tempos.extend(tempos_temp)
    TEMPO_WORDS = tempos
    return TEMPO_WORDS


class ModeValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in info.get_allowed_modes():
            raise ValidationError(message="Invalid mode", cursor_position=0)


class NoteValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in info.get_allowed_notes():
            raise ValidationError(message="Invalid note", cursor_position=0)


def movement_prompt(curr_movements):
    if curr_movements:
        print("Movements in piece: ")
        print_movements(curr_movements)
    prompt_help = (
        "Options:\n"
        f"{BOLD}print{END} movements\n"
        f"{BOLD}create{END} a new movement\n"
        f"{BOLD}edit{END} a movement\n"
        f"{BOLD}delete{END} a movement\n"
        f"{BOLD}help{END} to view this message\n"
        f"{BOLD}done{END} to save and return to main prompt"
    )
    print(prompt_help)
    command_completer = WordCompleter(['create', 'delete', 'print', 'edit', 'help', 'done'])
    tempo_completer = InsensitiveCompleter(get_tempo_words())
    mode_completer = WordCompleter(info.get_allowed_modes())
    while True:
        command = prompt("Movements> ", completer=command_completer)
        if len(command) == 0:
            continue
        elif command.lower()[0] == 'h':
            print(prompt_help)
        elif command.lower()[0] == 'p':
            print_movements(curr_movements)
        elif command.lower()[0] == 'c':
            new_mov_num = len(curr_movements) + 1
            new_mov_tempo = prompt("Enter tempo (optional): ", completer=tempo_completer)
            new_mov_time = prompt("Enter time signature (optional): ")
            new_mov_key_note = prompt("Enter key note: ", validator=NoteValidator())
            new_mov_key_mode = prompt("Enter key mode: ", completer=mode_completer, validator=ModeValidator())
            new_mov_key = info.KeySignature(note=new_mov_key_note, mode=new_mov_key_mode)
            curr_movements.append(info.Movement(num=new_mov_num, tempo=new_mov_tempo, time=new_mov_time,
                                                key=new_mov_key))
        elif command.lower()[0] == 'e':
            print_movements(curr_movements)
            mov_num = int(prompt("Enter movement number to edit: ", validator=IndexValidator(
                len(curr_movements), allow_empty=False)))
            working_mov = curr_movements[mov_num-1]
            curr_movements[mov_num-1].tempo = prompt("Enter tempo (optional): ", completer=tempo_completer,
                                                     default=working_mov.tempo)
            curr_movements[mov_num-1].time = prompt("Enter time signature (optional): ", default=working_mov.time)
            new_key_note = prompt("Enter key note: ", validator=NoteValidator(),
                                                        default=working_mov.key.note)
            new_key_mode = prompt("Enter key mode: ", completer=mode_completer,
                                                        validator=ModeValidator(), default=working_mov.key.mode)
            new_key = info.KeySignature(note=new_key_note, mode=new_key_mode)
            curr_movements[mov_num-1].key = new_key
        elif command.lower()[0:2] == 'de':
            print_movements(curr_movements)
            mov_num = int(prompt("Enter movement number to delete: ", validator=IndexValidator(
                len(curr_movements), allow_empty=False)))
            delete_index = mov_num - 1
            curr_movements.pop(delete_index)
            for i in range(delete_index, len(curr_movements)):
                curr_movements[i].num = curr_movements[i].num - 1
        elif command.lower()[0:2] == 'do':
            return curr_movements
        else:
            print(INVALID)