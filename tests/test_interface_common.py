from unittest.mock import MagicMock

import pytest

from lilyskel.interface.common import manual_instrument


@pytest.fixture
def mock_add_to_db():
    m = MagicMock()
    return m


@pytest.fixture
def mock_ins(mock_add_to_db):
    m = MagicMock()
    m.add_to_db = mock_add_to_db
    return m


@pytest.fixture
def mock_instrument_load(mock_ins):
    m = MagicMock()
    m.return_value = mock_ins
    return m


@pytest.fixture
def mock_instrument_class(mock_instrument_load):
    m = MagicMock()
    m.load = mock_instrument_load
    return m


def test_manual_instrument_defaults(
    monkeypatch, mock_instrument_load, mock_ins, mock_instrument_class, mock_add_to_db
):
    """Test manually creating a new interface"""
    mock_prompt = MagicMock()
    mock_prompt.side_effect = ["t.", "", "", "", ""]
    mock_confirm = MagicMock()
    mock_confirm.side_effect = [False, False]

    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.common.prompt", mock_prompt)
        m.setattr("lilyskel.interface.common.confirm", mock_confirm)
        m.setattr("lilyskel.interface.common.lynames.Instrument", mock_instrument_class)
        new_ins = manual_instrument("Test", None)

        assert new_ins == mock_ins

        mock_add_to_db.assert_not_called()
        mock_instrument_load.assert_called_once_with(
            {
                "clef": "treble",
                "name": "Test",
                "abbr": "t.",
                "number": None,
                "transposition": None,
                "midi": None,
                "family": None,
                "keyboard": False,
            }
        )


def test_manual_instrument_attributes(
    mockdb,
    monkeypatch,
    mock_instrument_load,
    mock_ins,
    mock_instrument_class,
    mock_add_to_db,
):
    """Test manual instrument entering values"""
    data = {
        "name": "Test",
        "abbr": "t.",
        "clef": "bass",
        "transposition": "c bb",
        "number": 2,
        "midi": "test",
        "keyboard": False,
        "family": "test",
    }
    mock_prompt = MagicMock()
    mock_prompt.side_effect = [
        data["abbr"],
        data["clef"],
        data["transposition"],
        data["midi"],
        data["family"],
    ]
    mock_confirm = MagicMock()
    mock_confirm.side_effect = [data["keyboard"], True]

    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.common.prompt", mock_prompt)
        m.setattr("lilyskel.interface.common.confirm", mock_confirm)
        m.setattr("lilyskel.interface.common.lynames.Instrument", mock_instrument_class)
        new_ins = manual_instrument(data["name"], data["number"], db=mockdb)

        assert new_ins == mock_ins

        mock_instrument_load.assert_called_once_with(data)
        assert mock_confirm.call_count == 2
        mock_add_to_db.assert_called_once_with(mockdb)
