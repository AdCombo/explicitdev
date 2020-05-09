from unittest.mock import NonCallableMock

import pytest

from . import mock


class Test:
    pass

def _test():
    pass


class Test_patch_imported:
    @pytest.fixture
    def mock_patch(self):
        patcher = mock.patch('tests.utils.mock.patch', autospec=True)
        result: NonCallableMock = patcher.start()
        yield result
        patcher.stop()

    def test_module(self, mock_patch):
        mock.patch_imported('test', mock)

        mock_patch.assert_called_once_with('tests.utils.mock.test', autospec=True)

    def test_class(self, mock_patch):
        mock.patch_imported('test', Test)

        mock_patch.assert_called_once_with('tests.utils.test_mock.test', autospec=True)

    def test_other_object_types(self):
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            mock.patch_imported('test', 'test')

    def test_function(self, mock_patch):
        mock.patch_imported('test', _test)

        mock_patch.assert_called_once_with('tests.utils.test_mock.test', autospec=True)

