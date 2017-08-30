"""Tests db interaction functions."""
import os
from pathlib import Path
import unittest
from unittest import mock
from lyskel import db_interface

home = os.path.join(os.path.expanduser('~'))
here = Path(__file__)
basedir = here.parents[1]
srcdir = Path(basedir, 'lyskel')


class TestPathify(unittest.TestCase):
    """Tests the pathify function."""
    def test_is_path(self):
        """Test that it stays a Path object."""
        self.assertEqual(
            db_interface.pathify(Path('/tmp', 'test', 'dir')),
            Path('/tmp', 'test', 'dir')
        )

    def test_is_str(self):
        """Test that we get a path object from a string."""
        self.assertEqual(
            db_interface.pathify('/tmp/test/dir'),
            Path('/tmp', 'test', 'dir')
        )

        self.assertEqual(
            db_interface.pathify('c:/tmp/test/dir'),
            Path('c:/tmp', 'test', 'dir')
        )


class TestDBFunctions(unittest.TestCase):
    """Test the database interaction."""
    @mock.patch('lyskel.db_interface.os.makedirs')
    @mock.patch('lyskel.db_interface.Path.exists')
    @mock.patch('lyskel.db_interface.TinyDB')
    def test_init_db(self, mock_db, mock_exists, mock_makedirs):
        """Test database initialization."""
        # test default no directories
        mock_exists.return_value = False
        db_interface.init_db(),
        mock_db.assert_called_once_with(
            Path(home, '.local', 'lyskel', 'db.json'))
        mock_makedirs.assert_called_once_with(
            Path(home, '.local', 'lyskel'))

        # test without missing directories
        mock_makedirs.reset_mock()
        mock_db.reset_mock()
        mock_exists.return_value = True
        db_interface.init_db(),
        mock_db.assert_called_once_with(
            Path(home, '.local', 'lyskel', 'db.json'))
        mock_makedirs.assert_not_called()

        # test custom
        mock_makedirs.reset_mock()
        mock_db.reset_mock()
        mock_exists.return_value = False
        db_interface.init_db('/one/two/three.json'),
        mock_db.assert_called_once_with(
            Path('/one', 'two', 'three.json'))
        mock_makedirs.assert_called_once_with(Path('/one', 'two'))

    @mock.patch('lyskel.db_interface.os.makedirs')
    @mock.patch('lyskel.db_interface.shutil')
    def test_bootstrap_db(self, mock_shutil, mock_makedirs):
        """Tests bootstraping the database with the default."""
        # test default db path
        db_interface.bootstrap_db()
        mock_makedirs.assert_called_once_with(
            Path(home, '.local', 'lyskel'), exist_ok=True
        )
        mock_shutil.copy2.assert_called_once_with(
            Path(srcdir, 'default_db.json'),
            Path(home, '.local', 'lyskel', 'db.json')
        )
