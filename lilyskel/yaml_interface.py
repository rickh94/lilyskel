"""Export data to/import data from yaml file."""
from pathlib import Path
from ruamel.yaml import YAML
from lilyskel.info import Piece

yaml = YAML()


def write_config(filepath: Path, piece: Piece):
    piece_data = piece.dump()
    yaml.dump(piece_data, filepath)


def read_config(filepath: Path):
    piece_data = yaml.load(filepath)
    if not piece_data:
        raise ValueError("No data in file.")
    return Piece.load(piece_data)
