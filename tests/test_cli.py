from click.testing import CliRunner
from pathlib import Path
from unittest import mock

from lilyskel.interface.cli import cli


def test_lilyskel_init(tmpdir_factory, monkeypatch):
    folder = tmpdir_factory.mktemp("test_lilyskel_init_")
    test_name1 = "test"
    full_path1 = Path(folder, test_name1 + '.yaml')
    runner = CliRunner()
    result = runner.invoke(cli, ['init', test_name1, '-p', str(folder)])
    assert result.exit_code == 0
    assert full_path1.exists()

    mock_prompt = mock.MagicMock()
    mock_prompt.return_value = 'Y'

    test_name2 = "test2"
    full_path2 = Path(folder, test_name2 + '.yaml')
    with full_path2.open('w') as test2:
        test2.write("This should be deleted.")

    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.cli.prompt", mock_prompt)
        result = runner.invoke(cli, ['init', test_name2, '-p', str(folder)])
        assert result.exit_code == 0

    with full_path2.open('r') as test2:
        assert "This should be deleted." not in test2.read()
