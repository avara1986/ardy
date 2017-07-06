# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os
import shutil
import unittest
from tempfile import mkdtemp

from mock import patch, mock_open

# App imports
from ardy.core.build.build import Build, pip
from tests.utils import touch

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))


class BuildTest(unittest.TestCase):
    EXAMPLE_PROJECT = "myexamplelambdaproject"

    DIST_FOLDER = "dist"

    def setUp(self):
        self.build = Build(path=TESTS_PATH)

    def test_mkdir(self):
        fake_folder = "fake_folder_{}".format(self.build.timestamp())

        self.assertFalse(os.path.exists(os.path.join(TESTS_PATH, fake_folder)))
        self.assertTrue(self.build.mkdir(fake_folder))
        self.assertTrue(os.path.exists(os.path.join(TESTS_PATH, fake_folder)))
        self.assertFalse(self.build.mkdir(fake_folder))

        shutil.rmtree(os.path.join(TESTS_PATH, fake_folder))

    def test_read(self):
        fake_file = "fake_file_{}".format(self.build.timestamp())
        mock_read = mock_open()

        with patch('ardy.core.build.build.open', mock_read, create=False):
            self.build.read(fake_file)

        self.assertEqual(mock_read.call_count, 1)

    def test_create_artefact(self):
        # create source
        fake_src = os.path.join(self.EXAMPLE_PROJECT, "fake_folder_{}".format(self.build.timestamp()))
        self.build.mkdir(fake_src)
        fake_src_aux = os.path.join("subfake_folder_{}".format(self.build.timestamp()))
        for i in range(0, 4):
            folder = os.path.join(fake_src, fake_src_aux)
            self.build.mkdir(folder)
            touch(os.path.join(TESTS_PATH, folder, "test1"))
            touch(os.path.join(TESTS_PATH, folder, "test2"))
            fake_src_aux = os.path.join(fake_src_aux, fake_src_aux)

        # Set destination
        fake_zip = "fake_zip_{}.zip".format(self.build.timestamp())
        dest_folder = os.path.join(self.EXAMPLE_PROJECT, self.DIST_FOLDER)
        self.build.mkdir(dest_folder)
        fake_dest_file = os.path.join(dest_folder, fake_zip)

        # Run
        result = self.build.create_artefact(fake_src, dest_folder, fake_zip)

        # Test result
        fake_dest_file = os.path.join(TESTS_PATH, fake_dest_file)
        self.assertEqual(result, fake_dest_file)
        self.assertTrue(os.path.isfile(fake_dest_file))

        # remove
        os.remove(fake_dest_file)
        shutil.rmtree(os.path.join(TESTS_PATH, fake_src))

    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run(self, create_artefact_mock, copytree_mock, pip_install_mock):
        zip_file = self.build.run(self.EXAMPLE_PROJECT)

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertEqual(zip_file, create_artefact_mock.return_value)

    @patch.object(pip, "main")
    def test_pip_install_to_target(self, pip_install_mock):
        self.build.set_src_path(self.EXAMPLE_PROJECT)
        zip_file = self.build.pip_install_to_target(path=mkdtemp(prefix='aws-lambda'), requirements="requirements.txt")

        self.assertTrue(pip_install_mock.called)


if __name__ == '__main__':
    unittest.main()
