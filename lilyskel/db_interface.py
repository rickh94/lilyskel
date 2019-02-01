"""Methods for dealing with tinydb database."""
import os
import shutil
from pathlib import Path

from tinydb import Query, TinyDB

from . import exceptions

here = Path(__file__).parents[0]
def_path = Path(os.path.expanduser("~"), ".local", "share", "lilyskel", "db.json")


def init_db(path=None) -> TinyDB:
    """
    Initializes the database.
    :param path: (optional) the path of the database.
    :return: TinyDB of common instruments and composers
    """
    db_path = path or def_path
    db_path = Path(db_path)
    os.makedirs(db_path.parents[0], exist_ok=True)
    return TinyDB(db_path)


def bootstrap_db(path=None):
    """
    Bootstraps the database from included defaults.
    :param path: (optional) the destination of the database.
    """
    if path is None:
        path = def_path
    path = Path(path)
    os.makedirs(path.parents[0], exist_ok=True)
    # grab the included default database
    # TODO: refactor to use importlib.resources
    default = Path(here, "default_db.json")
    shutil.copy2(default, path)


def explore_db(db: TinyDB) -> list:
    """
    Explore what tables are available in the database.
    :param db: a TinyDB instance.
    """
    if not isinstance(db, TinyDB):
        raise ValueError("'db' must be a TinyDB instance.")
    tables = db.tables()
    if "_default" in tables:
        tables.remove("_default")
    return list(tables)


def explore_table(table, search=None) -> list:
    """
    Explore a table in the database.

    :param table: the tinydb table object to search.
    :param search: (optional) a tuple of (field, search_term) to search for in the
        table.
    :return: results of the search
    """
    founditems = []
    if search is None:
        items = table.all()
    else:
        if not isinstance(search, tuple):
            raise TypeError("search must be a tuple (field, value)")
        field, term = search
        q = Query()
        # Search[field]: look specified field, lambda val: return the value
        # from the db if the term is found in it.
        try:
            items = table.search(q[field].test(lambda val: term in val))
        except AttributeError as err:
            raise TypeError("table may not be a tinydb table ", err)
    for item in items:
        if "name" in item:
            founditems.append(item["name"])
        elif "word" in item:
            founditems.append(item["word"])
    return founditems


def load_name_from_table(
    name: str, db: TinyDB, table_name: str, extra_searches=None
) -> dict:
    """
    Load data with specified 'name' from the specified 'db' table.

    :param: name: the name of the item to be retrieved.
    :param: db: a TinyDB object
    :param: table_name: the name of the table to search
    :param: extra_searches: an additional filter in case of
        multiple of the same name

    :return: dict of data from database
    """
    q = Query()
    # get an object matching name from the db.
    db_table = db.table(table_name)
    data = db_table.get(q.name == name)
    if data is None:
        raise exceptions.DataNotFoundError(
            f"'{name}' is not in the '{table_name}' table."
        )
    return data
