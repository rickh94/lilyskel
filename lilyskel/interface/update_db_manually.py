import better_exceptions
import click
from titlecase import titlecase
from prompt_toolkit import prompt


from lilyskel.info import Composer
from lilyskel.exceptions import MutopiaError
from lilyskel import db_interface
from lilyskel.interface.common import *


@click.group()
@click.option("-p", "--db-path", help="alternate database location")
@click.pass_context
def db(ctx, db_path):
    """Directly interface with the database."""
    if not ctx.obj:
        ctx.obj = {}
    ctx.obj['DB'] = db_interface.init_db(db_path)


@db.group()
def add():
    """Add something to the database"""
    pass


@add.command()
@click.pass_context
def instrument(ctx):
    """Add an instrument to the database"""
    db_ = ctx.obj['DB']
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
        new_ins.add_to_db(db_)
    return


@add.command()
@click.option("--name", prompt="Composer name: ")
@click.pass_context
def composer(ctx, name):
    """Add composer to the database."""
    db_ = ctx.obj['DB']
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
    newcomp.add_to_db(db_)
    newrec = db_interface.explore_table(
        db_.table("composers"), search=("shortname", newcomp.shortname))
    print(newrec)


@add.command()
@click.argument("table")
@click.argument("infile")
@click.pass_context
def fromfile(ctx, table, infile):
    """
    Adds data to a table from the lines of a file
    :param table:
    :param infile:
    :return:
    """
    db_ = ctx.obj['DB']
    with open(infile, "r") as data:
        items = data.readlines()
    table_obj = db_.table(table)
    for item in items:
        table_obj.insert({"word": item.strip()})

    print(table_obj.all())


@add.command()
@click.argument("name", required=True)
@click.option("-i", "--instrument", multiple=True)
@click.pass_context
def ensemble(ctx, name, instrument):
    """Add an ensemble to the database"""
    db_ = ctx.obj['DB']
    new_ens = create_ensemble(name, db_, instrument)
    print(new_ens)
    yn = prompt("Add to database? ", validator=YNValidator(), default='Y')
    if yn.lower()[0] == 'y':
        new_ens.add_to_db(db_)


class IsNumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            return
        if not text.isdigit():
            raise ValidationError(message="Must be integer")
        try:
            int(text)
        except ValueError as err:
            raise ValidationError(message=err)


def db_instrument_prompt(instruments, ins_list, db_):
    ins_completer = InsensitiveCompleter(instruments)
    while True:
        new_ins_name = prompt("Enter an instrument, blank to finish: ", completer=ins_completer)
        if len(new_ins_name) == 0:
            break
        ins_number = prompt("Enter associated number (e.g. Violin 2) or [enter] for none: ",
                            validator=IsNumberValidator()) or None
        if ins_number:
            ins_number = int(ins_number)
        load = 'N'
        if new_ins_name in instruments:
            load = prompt(f"{new_ins_name} is in the database, load it? ", default='Y',
                          validator=YNValidator())
        if load.lower()[0] == 'y':
            new_ins = Instrument.load_from_db(normalize_name(new_ins_name),
                                              db_, number=ins_number)
        else:
            new_ins = manual_instrument(new_ins_name, ins_number, db_)
        ins_list.append(new_ins)
    return ins_list


@db.command()
@click.argument("table", required=True)
@click.argument("field", required=True)
@click.argument("term", required=True)
@click.pass_context
def search(ctx, table, field, term):
    """Search the database"""
    db_ = ctx.obj['DB']
    print(db_interface.explore_table(db_.table(table), search=(field, term)))


if __name__ == '__main__':
    cli()
