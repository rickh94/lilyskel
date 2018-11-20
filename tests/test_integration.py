import prompt_toolkit
import pytest
from pathlib import Path
from unittest import mock

import lilyskel


def test_create_from_prompt(monkeypatch, tmpdir_factory, defaultdb,
                            prompt_commands, good_beethoven):
    tmp_config = tmpdir_factory.mktemp('test_create_from_prompt')
    test_piece = None
    test_config_path = Path(tmp_config, 'beethoven_5.yaml')
    with test_config_path.open('w') as config_file:
        config_file.write('')
    test_path_save = Path('/tmp/nonexistent')
    mock_prompt = mock.Mock()
    mock_prompt.side_effect = prompt_commands
    # mock_prompt.side_effect = [
    #     'Op. 67',
    #     'ensemble',
    #     'Classical Orchestra',
    #     'Flute',
    #     '1',
    #     'Y',
    #     'add',
    #     'Flute',
    #     '2',
    #     'Y',
    #     'done',
    #     'Y',
    #     'N',
    #     'header',
    #     'Ludwig van Beethoven',
    #     'Y',
    #     'Symphony No. 5',
    #     'done',
    #     'quit',
    #     'N'
    # ]
    # with mock.patch('lilyskel.interface.edit_prompts.prompt', mock_prompt):
    with pytest.raises(SystemExit):
        with monkeypatch.context() as m:
            m.setattr('lilyskel.interface.edit_prompts.prompt', mock_prompt)
            m.setattr('lilyskel.interface.common.prompt', mock_prompt)
            lilyskel.interface.edit_prompts.edit_prompt(test_piece, test_config_path, defaultdb, test_path_save)
            with test_config_path.open('r') as config_file:
                test_config_data = config_file.read()
            # print(test_config_data)
            # assert 'title: Symphony No. 5' in test_config_data
            assert good_beethoven == test_config_data
