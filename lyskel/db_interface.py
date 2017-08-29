from tinydb import TinyDB, Query
from lyskel import lynames


def create_instrument(dbtable, name, clef, abbr, transposition=None,
                      keyboard=False, midi=None):
    data = {
        'name': name,
        'abbr': abbr,
        'clef': clef,
        'transposition': transposition,
        'keyboard': keyboard,
        'midi': midi,
    }
    dbtable.insert(data)


def find_instrument(dbtable, name):
    Instrument = Query()
    return dbtable.get(Instrument.name == name)


if __name__ == '__main__':
    db = TinyDB('/tmp/tmptestdb.json')
    ins_table = db.table('instruments')
    create_instrument(ins_table, 'violin', 'treble', 'Vln.', midi='violin')
