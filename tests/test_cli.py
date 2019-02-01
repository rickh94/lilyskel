import atexit
import functools
import inspect
import os
from pathlib import Path
from unittest import mock

import click
import pytest
from click.testing import CliRunner

from lilyskel.interface import create_commands
from lilyskel.interface.cli import cli


@pytest.fixture
def run():
    runner = CliRunner()
    return functools.partial(runner.invoke, cli=cli)


def test_lilyskel_init(tmpdir_factory, monkeypatch, run):
    """Test initialization of a yaml file"""
    atexit.register(os.remove, "/tmp/lilyskel_path")
    folder = tmpdir_factory.mktemp("test_lilyskel_init_")
    test_name1 = "test"
    full_path1 = Path(folder, test_name1 + ".yaml")
    result = run(args=["init", test_name1, "-p", str(folder)])
    assert result.exit_code == 0
    assert full_path1.exists()

    mock_confirm1 = mock.MagicMock()
    mock_confirm1.return_value = True

    mock_confirm2 = mock.MagicMock()
    mock_confirm2.return_value = False

    test_name2 = "test2"
    full_path2 = Path(folder, test_name2 + ".yaml")
    with full_path2.open("w") as test2:
        test2.write("This should be deleted.")

    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.cli.confirm", mock_confirm1)
        result = run(args=["init", test_name2, "-p", str(folder)])
        assert result.exit_code == 0
        assert Path(
            folder, test_name2 + ".yaml.bak"
        ).exists(), "check file was backed up"

    with full_path2.open("r") as test2:
        assert "This should be deleted." not in test2.read()

    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.cli.confirm", mock_confirm2)
        result = run(args=["init", test_name2, "-p", str(folder)])
        assert result.exit_code == 1


def test_lilyskel_build_successful(monkeypatch, tmp_path, run, good_beethoven_file):
    """Test lilyskel build calls appropriate code, more of an integration test"""
    # beethoven_file = tmp_path / "beethoven.yml"
    # with beethoven_file.open("w") as bf:
    #     bf.write(good_beethoven)

    result = run(args=["build", "-f", str(good_beethoven_file), "-t", str(tmp_path)])
    assert result.exit_code == 0

    defs_file = tmp_path / "defs.ily"
    flute1_dir = tmp_path / "flute1"
    violin2_dir = tmp_path / "violin2"
    violin2_file = violin2_dir / "violin2_2.ily"

    assert defs_file.exists()
    assert flute1_dir.exists()
    assert violin2_dir.exists()
    assert violin2_file.exists()


@pytest.fixture
def generic_edit_run(good_beethoven_file, livedb_file, run):
    def _edit(*args):
        return run(
            args=["edit", "-f", str(good_beethoven_file), "-d", str(livedb_file), *args]
        )

    return _edit


def test_edit_repl_called(
    monkeypatch, generic_edit_run, good_beethoven_file, livedb_file
):
    """Test edit repl is called when edit is called without commands"""
    edit_repl = mock.MagicMock("edit_repl")
    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.edit_commands._edit_repl", edit_repl)
        result = generic_edit_run()
        assert result.exit_code == 0
        print(result.stdout)
        edit_repl.assert_called()


def test_edit_print(monkeypatch, generic_edit_run):
    """Test printing current piece object"""
    print_formatted_text_mock = mock.MagicMock()
    monkeypatch.setattr(
        "lilyskel.interface.edit_commands.print_formatted_text",
        print_formatted_text_mock,
    )
    result = generic_edit_run("print")
    assert result.exit_code == 0
    print_formatted_text_mock.assert_called()


def test_edit_language(monkeypatch, generic_edit_run):
    """Test edit language calls generated code"""
    language_callback = mock.MagicMock()
    with monkeypatch.context() as m:
        m.setattr(
            "lilyskel.interface.edit_commands.language.callback", language_callback
        )
        result = generic_edit_run("language")

        assert result.exit_code == 0
        language_callback.assert_called()


def test_create_prompt_command(monkeypatch):
    """Test creating a prompt command"""
    test_command = create_commands.create_prompt_command(
        'Test', 'test', 'test help'
    )
    assert isinstance(test_command, click.Command)
    assert test_command.name == 'test'
    assert test_command.help == 'test help'
    callback_source = inspect.getsource(test_command.callback)
    assert 'ctx.obj' in callback_source
    assert 'prompt' in callback_source
    assert 'Enter' in callback_source

# def test_edit_done(monkeypatch, generic_edit_run):
#     """Test done raises exit repl extension"""
#     with pytest.raises(click_repl.exceptions.ExitReplException):
#         result = generic_edit_run("done")
#         print(result.stdout)

# def test_edit_headers(monkeypatch, generic_edit_run):
#     """Test edit headers with no options opens repl"""
#     monkeypatch.setattr
