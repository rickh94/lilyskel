from pathlib import Path
from tinydb import TinyDB
from lilyskel.lynames import Instrument


db = TinyDB(Path("/home/rick/repositories/lilyskel/lilyskel/default_db.json"))


def add_instrument():
    name = input("Instrument Name (lower): ")
    abbr = input("Instrument Abbreviation: ")
    clef = input("Instrument clef: ") or "treble"
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
    add = input("Correct? [y/N]")
    if add[0].lower() == 'y':
        new_ins.add_to_db(db)
    return

if __name__ == '__main__':
    add_instrument()