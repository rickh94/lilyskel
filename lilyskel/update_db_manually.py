from pathlib import Path
import better_exceptions
import click
from tinydb import TinyDB
from titlecase import titlecase
from lilyskel.lynames import Instrument
from lilyskel.lynames import Ensemble
from lilyskel.lynames import normalize_name
from lilyskel.info import Composer
from lilyskel.exceptions import MutopiaError
from lilyskel import db_interface
from lilyskel.cli import InsensitiveCompleter, instruments_with_indexes, \
    manual_instrument, YNValidator, reorder_instruments

from prompt_toolkit import prompt


db = TinyDB(Path("/home/rick/repositories/lilyskel/lilyskel/default_db.json"))


@click.group()
def cli():
    pass


@cli.command()
def instrument():
    name = input("Instrument Name (lower): ")
    abbr = input("Instrument Abbreviation: ")
    clef = input("Instrument clef: ") or "treble"
    if ' ' in clef:
        clef = clef.split()
    transposition = input("Transposition: ") or None
    keyboard = bool(input("Keyboard? ")) or False
    midi = input("Midi instrument name: ")
    family = input("Instrument family: ")
    mutopianame = input("Mutopia name: ") or None
    new_ins = Instrument(
        name=name,
        abbr=abbr,
        clef=clef,
        transposition=transposition,
        keyboard=keyboard,
        midi=midi,
        family=family,
        mutopianame=mutopianame
    )
    print(new_ins)
    add = input("Correct? [y/N] ")
    if add[0].lower() == 'y':
        new_ins.add_to_db(db)
    return


@cli.command()
@click.argument("name", required=True)
def composer(name):
    # name = input("Composer full name: ")
    newcomp = Composer(name)
    try:
        mutopianame = input(
            f"Assumed Mutopia Name is {newcomp.get_mutopia_name(guess=True)}"
            " Is this correct? [Y/n] "
        ) or "Y"
        if mutopianame[0].lower() == 'n':
            newcomp.mutopianame = input("Enter correct Mutopia Name: ")
    except MutopiaError:
        newcomp.mutopianame = input("Enter correct Mutopia Name: ")
    shortname = input(f"Assumed short name is {newcomp.get_short_name()}"
                      " Correct? [Y/n] ") or "Y"
    if shortname[0].lower() == 'n':
        newcomp.shortname = input("Enter correct short name: ")
    newcomp.add_to_db(db)
    newrec = db_interface.explore_table(
        db.table("composers"), search=("shortname", newcomp.shortname))
    print(newrec)


@cli.command()
@click.argument("name", required=True)
def table(name):
    db.table(name)
    print(name in db.tables() or "Failed")


@cli.command()
@click.argument("table")
@click.argument("infile")
def addfromfile(table, infile):
    """
    Adds data to a table from the lines of a file
    :param table:
    :param infile:
    :return:
    """
    with open(infile, "r") as data:
        items = data.readlines()
    table_obj = db.table(table)
    for item in items:
        table_obj.insert({"word": item.strip()})

    print(table_obj.all())


@cli.command()
@click.argument("name", required=True)
@click.option("-i", "--instrument", multiple=True)
def ensemble(name, instrument):
    instrument_names = db_interface.explore_table(db.table("instruments"),
                                                  search=("name", ""))
    instruments = [titlecase(' '.join(name.split('_')))
                   for name in instrument_names]
    ins_list = []
    new_ens = Ensemble(name)
    for ins in instrument:
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
    done = False
    if ins_list:
        instruments_with_indexes(ins_list)
        more_ins = prompt("Any more instruments? ", validator=YNValidator(), default='N')
        if more_ins.lower()[0] == 'n':
            done = True
    if not done:
        ins_list = db_instrument_prompt(instruments, ins_list)
        instruments_with_indexes(ins_list)
    reorder = prompt("Would you like to reorder the instruments? ", default='N',
                     validator=YNValidator())
    if reorder.lower()[0] == 'y':
        ins_list = reorder_instruments(ins_list)
    for ins in ins_list:
        new_ens.add_instrument_from_obj(ins)
    print(new_ens)
    yn = prompt("Add to database? ", validator=YNValidator(), default='Y')
    if yn.lower()[0] == 'y':
        new_ens.add_to_db(db)


def db_instrument_prompt(instruments, ins_list):
    ins_completer = InsensitiveCompleter(instruments)
    while True:
        new_ins_name = prompt("Enter an instrument, blank to finish: ", completer=ins_completer)
        if len(new_ins_name) == 0:
            break
        ins_number = prompt("Enter associated number (e.g. Violin 2) or [enter] for none: ") or None
        load = 'N'
        if new_ins_name in instruments:
            load = prompt(f"{new_ins_name} is in the database, load it? ", default='Y',
                          validator=YNValidator())
        if load.lower()[0] == 'y':
            new_ins = Instrument.load_from_db(normalize_name(new_ins_name),
                                              db, number=ins_number)
        else:
            new_ins = manual_instrument(new_ins_name, ins_number, db)
        ins_list.append(new_ins)
    return ins_list


@cli.command()
@click.argument("table", required=True)
@click.argument("field", required=True)
@click.argument("term", required=True)
def search(table, field, term):
    print(db_interface.explore_table(db.table(table), search=(field, term)))


if __name__ == '__main__':
    cli()
