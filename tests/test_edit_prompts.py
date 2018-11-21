import pytest
from pathlib import Path
from unittest import mock
import lilyskel

BOLD = "\033[1m"
END = "\033[0m"
INVALID = "Command not recognized. Please try again."
EDIT_PROMPT_HELP = (
    "\nYou can now add score information. Available modes are:\n"
    f"{BOLD}header:{END}\t\tadd title, composer, etc.\n"
    f"{BOLD}mutopia:{END}\tAdd information for submitting to the mutopia project\n"
    f"{BOLD}instrument:{END}\tadd/remove/re-order individual instruments "
    "in the score\n"
    f"{BOLD}ensemble:{END}\tadd an ensemble to the score\n"
    f"{BOLD}movement:{END}\tadd/remove movements (including time, key, "
    f"and tempo info\n"
    f"{BOLD}language:{END}\tset the region language for lilypond\n"
    f"{BOLD}print:{END}\t\t print the current state of the score info.\n"
    f"{BOLD}save:{END}\t\t save current state to config file\n"
    f"{BOLD}quit:{END}\t\twrite out file and exit\n"
    f"{BOLD}help:{END}\t\tprint this message\n"
)

HEADER_PROMPT_HELP = (
    "You may edit any of the following headers:\n"
    "title\t\tcomposer\n"
    "dedication\tsubtitle\n"
    "subsubtitle\tpoet\n"
    "meter\t\tarranger\n"
    "tagline\t\tcopyright\n"
    "Enter \"print\" to print the current headers and \"done\" to finish"
    "and return to the main prompt."
)


def test_edit_prompt_empty_config(monkeypatch, tmpdir_factory, defaultdb):
    path_save = Path(tmpdir_factory.mktemp("pathsave_not_needed"), 'lilyskel_path')
    config_path1 = Path(tmpdir_factory.mktemp('config_path1'), 'test1.yaml')
    mock_prompt1 = mock.MagicMock()
    mock_prompt1.side_effect = [
        'Op. 1',
        '',
        'print',
        'language',
        'english',
        'mutopia',
        'movements',
        'instrument',
        'ensemble',
        'header',
        'help',
        'not a real command',
        'save',
        'quit',
        'N'
    ]
    mock_print_info = mock.MagicMock()
    mock_mutopia_prompt = mock.MagicMock()
    mock_movement_prompt = mock.MagicMock()
    mock_ensemble_prompt = mock.MagicMock()
    mock_existing_instruments = mock.MagicMock()
    mock_existing_instruments.return_value = []
    mock_instrument_prompt = mock.MagicMock()
    mock_header_prompt = mock.MagicMock()
    mock_save_config = mock.MagicMock()
    mock_print = mock.MagicMock()
    with monkeypatch.context() as m:
        m.setattr('lilyskel.interface.edit_prompts.prompt', mock_prompt1)
        m.setattr('lilyskel.interface.edit_prompts.print_piece_info', mock_print_info)
        m.setattr('lilyskel.interface.edit_prompts.movement_prompt', mock_movement_prompt)
        m.setattr('lilyskel.interface.edit_prompts.mutopia_prompt', mock_mutopia_prompt)
        m.setattr('lilyskel.interface.edit_prompts.existing_instruments', mock_existing_instruments)
        m.setattr('lilyskel.interface.edit_prompts.ensemble_prompt', mock_ensemble_prompt)
        m.setattr('lilyskel.interface.edit_prompts.instrument_prompt', mock_instrument_prompt)
        m.setattr('lilyskel.interface.edit_prompts.header_prompt', mock_header_prompt)
        m.setattr('lilyskel.interface.edit_prompts.save_config', mock_save_config)
        m.setattr('builtins.print', mock_print)

        with pytest.raises(SystemExit):
            lilyskel.interface.edit_prompts.edit_prompt(None, config_path1, defaultdb, path_save)

        mock_prompt1.assert_any_call("Enter Lilypond Language: ", completer=mock.ANY, validator=mock.ANY)
        mock_mutopia_prompt.assert_called_once_with(None)
        mock_movement_prompt.assert_called_once_with([])
        mock_existing_instruments.assert_any_call([], mock.ANY, mock_ensemble_prompt)
        mock_existing_instruments.assert_any_call([], mock.ANY, mock_instrument_prompt)
        mock_header_prompt.assert_any_call(None, mock.ANY)
        mock_save_config.assert_called()
        mock_print.assert_any_call("Exiting")
        mock_print.assert_any_call(EDIT_PROMPT_HELP)
        mock_print.assert_any_call("Saved")
        mock_print.assert_any_call(INVALID)


def test_header_prompt(monkeypatch, defaultdb):
    mock_composer_prompt = mock.MagicMock()
    test_composer = lilyskel.info.Composer("Test Composer")
    mock_composer_prompt.return_value = test_composer
    mock_prompt = mock.MagicMock()
    mock_headers = mock.MagicMock()
    test_headers = lilyskel.info.Headers(title="new title",
                                         composer=test_composer)
    mock_headers.return_value = test_headers
    mock_prompt.side_effect = [
        "new title",
        "title",
        "new title 2",
        "dedication",
        "test dedication",
        "subtitle",
        "test subtitle",
        "subsubtitle",
        "test subsubtitle",
        "poet",
        "test poet",
        "meter",
        "test meter",
        "arranger",
        "test arranger",
        "tagline",
        "test tagline",
        "copyright",
        "test copyright",
        "help",
        "print",
        "not valid",
        "done"
    ]
    mock_print = mock.MagicMock()
    with monkeypatch.context() as m:
        m.setattr('lilyskel.interface.edit_prompts.composer_prompt', mock_composer_prompt)
        m.setattr('lilyskel.interface.edit_prompts.prompt', mock_prompt)
        m.setattr('lilyskel.info.Headers', mock_headers)
        m.setattr('builtins.print', mock_print)

        lilyskel.interface.edit_prompts.header_prompt(None, defaultdb)

        mock_composer_prompt.assert_called()
        mock_prompt.assert_any_call("Enter Title: ", completer=mock.ANY)
        mock_headers.assert_any_call(title="new title", composer=test_composer)
        mock_print.assert_any_call(INVALID)
        mock_print.assert_any_call(test_headers)
        mock_print.assert_any_call(HEADER_PROMPT_HELP)
        # check that headers attributes were set correctly
        assert test_headers.title == "new title 2"
        assert test_headers.dedication == "test dedication"
        assert test_headers.subtitle == "test subtitle"
        assert test_headers.subsubtitle ==  "test subsubtitle"
        assert test_headers.poet == "test poet"
        assert test_headers.meter == "test meter"
        assert test_headers.arranger == "test arranger"
        assert test_headers.tagline == "test tagline"
        assert test_headers.copyright == "test copyright"


