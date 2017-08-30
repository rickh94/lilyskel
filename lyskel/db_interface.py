"""Methods for dealing with tinydb database."""
from pathlib import Path
import os
import shutil
from tinydb import TinyDB, Query

here = Path(__file__).parents[0]
def_path = Path(os.path.expanduser('~'), '.local', 'lyskel', 'db.json')


def pathify(in_path):
    """Normalize paths as Path objects."""
    return Path(in_path)


def init_db(path=def_path):
    """
    Initializes the database.
    """
    path = pathify(path)
    if not path.parents[0].exists():
        os.makedirs(path.parents[0])
    return TinyDB(path)


def bootstrap_db(path=def_path):
    """
    Bootstraps the database from included defaults.
    """
    path = pathify(path)
    os.makedirs(path.parents[0], exist_ok=True)
    # grab the included default database
    default = Path(here, 'default_db.json')
    shutil.copy2(default, path)


def explore_db(db):
    """Explore what tables are available in the database."""
    tables = db.tables()
    if '_default' in tables:
        tables.remove('_default')

    return list(tables)


def explore_table(table, name_search=None):
    """Explore a table in the database."""
    founditems = []
    if name_search is None:
        items = table.all()
    else:
        Search = Query()
        items = table.search(Search.name == name_search)

    for item in items:
        try:
            founditems.append(item['name'])
        except KeyError:
            pass

    return founditems
