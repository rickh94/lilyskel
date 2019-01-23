from pathlib import Path
from unittest import mock

import pytest

import lilyskel


@pytest.mark.xfail
def test_create_from_prompt(
    monkeypatch, tmpdir_factory, defaultdb, prompt_commands, good_beethoven
):
    tmp_config = tmpdir_factory.mktemp("test_create_from_prompt")
    test_piece = None
    test_config_path = Path(tmp_config, "beethoven_5.yaml")
    with test_config_path.open("w") as config_file:
        config_file.write("")
    test_path_save = Path("/tmp/nonexistent")
    mock_prompt = mock.Mock()
    mock_prompt.side_effect = prompt_commands
    test_config_data = ""
    with monkeypatch.context() as m:
        m.setattr("lilyskel.interface.edit_prompts.prompt", mock_prompt)
        m.setattr("lilyskel.interface.common.prompt", mock_prompt)
        with pytest.raises(SystemExit):
            lilyskel.interface.edit_prompts.edit_prompt(
                test_piece, test_config_path, defaultdb, test_path_save
            )
        with test_config_path.open("r") as config_file:
            test_config_data = config_file.read()
    assert "title: Symphony No. 5" in test_config_data
    assert "Jane Smith" in test_config_data
    assert "janesmith@example.com" in test_config_data
    # print(test_config_data)
    assert good_beethoven == test_config_data
