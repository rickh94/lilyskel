import click
from prompt_toolkit import print_formatted_text
from prompt_toolkit.shortcuts import confirm, input_dialog
from tinydb import Query

from lilyskel.info import Composer
from lilyskel.exceptions import MutopiaError
from lilyskel.interface import sub_repl
from lilyskel.interface.common import *


@click.group(invoke_without_command=True)
@click.option("-p", "--db-path", help="alternate database location")
@click.pass_context
def db(ctx, db_path):
    """Directly interface with the database."""
    if not ctx.obj:
        ctx.obj = AppState()
    ctx.obj.db = db_interface.init_db(db_path)
    # print('invoked db')
    _db_repl(ctx)


@db.group(invoke_without_command=True)
@click.pass_context
def add(ctx):
    """Add something to the database."""
    _add_repl(ctx)


@add.command()
@click.pass_context
def instrument(ctx):
    """Add an instrument to the database."""
    db_ = ctx.obj.db
    name = prompt("Instrument Name: ")
    manual_instrument(name, None, db_)


@add.command()
@click.option("--name", prompt="Composer name: ")
@click.pass_context
def composer(ctx, name):
    """Add composer to the database."""
    db_ = ctx.obj.db
    newcomp = Composer(name)
    try:
        if not confirm(f"Assumed Mutopia Name is {newcomp.get_mutopia_name(guess=True)}"
                       " Is this correct? "):
            newcomp.mutopianame = prompt("Enter correct Mutopia Name: ")
    except MutopiaError:
        newcomp.mutopianame = prompt("Enter correct Mutopia Name: ")
    if not confirm(f"Assumed short name is {newcomp.get_short_name()}"
                   " Correct? [Y/n] "):
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
    db_ = ctx.obj.db
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
    db_ = ctx.obj.db
    new_ens = create_ensemble(name, db_, instrument)
    print(new_ens)


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
    db_ = ctx.obj.db
    print(db_interface.explore_table(db_.table(table), search=(field, term)))


@db.command()
@click.argument("table", required=True)
@click.argument("field", default="name")
@click.argument("search_term")
@click.pass_context
def delete(ctx, table, field, search_term):
    """Find and delete an item from a table"""
    table = ctx.obj.db.table(table)
    if not search_term:
        search_term = prompt(f"Enter a search term for table {table}")
    q = Query()
    try:
        items = table.search(q[field].test(lambda val: search_term in val))
    except AttributeError as err:
        print("Invalid table or db.")
    for num, item in enumerate(items):
        print(f"{num}: {item}")
    while True:
        choice = prompt("Type number to delete or [enter] to finish: ", validator=IndexValidator(len(items)))
        if not choice:
            return
        table.remove(doc_ids=[items[int(choice)].doc_id])


_db_repl = sub_repl.create(db, {'message': 'lilyskel:db> '})
_add_repl = sub_repl.create(add, {'message': 'lilyskel:db:add> '})
