import os.path
from pyautotest import importutil


class DocTestMapper(object):
    """Map modified files to their test name."""

    def __init__(self, _):
        pass

    def get_test_filename(self, filename):
        return filename


class StandardMapper(object):
    """Expects that tests are located in a matching directory structure as
    source where the top level package is tests, and the file names have
    _test.py.

    Example:
        File:
            package/runner/stuff.py
        Is tested by:
            tests/runner/stuff_test.py
    """

    default_test_package = 'tests'
    test_file_extension = '_test.py'

    def __init__(self, basepath, test_package=None):
        self.basepath       = basepath
        self.test_package   = test_package or self.default_test_package

    def strip_basepath(self, filename):
        """
        >>> m = StandardMapper('/base')
        >>> m.strip_basepath('/base/filename.py')
        'filename.py'
        >>> m.strip_basepath('/base/more/filename.py')
        'more/filename.py'

        >>> m = StandardMapper('/base/more')
        >>> m.strip_basepath('/base/more/filename.py')
        'filename.py'
        """
        return filename[len(self.basepath):].lstrip(os.path.sep)

    def swap_base_package(self, filename):
        """
        >>> m = StandardMapper('/base')
        >>> m.swap_base_package('package/file.py')
        'tests/file.py'
        >>> m.swap_base_package('package/more/file.py')
        'tests/more/file.py'
        """
        path_parts    = filename.split(os.path.sep)
        path_parts[0] = self.test_package
        return os.path.sep.join(path_parts)

    def is_testfile(self, filename):
        """
        >>> m = StandardMapper('/base')
        >>> m.is_testfile('tests/somefile.py')
        True
        >>> m.is_testfile('package/somefile.py')
        False
        """
        return filename.startswith(self.test_package + os.path.sep)

    def replace_extension(self, filename):
        """
        >>> m = StandardMapper('/base')
        >>> m.replace_extension('package/somefile.py')
        'package/somefile_test.py'
        """
        return filename[:-len('.py')] + self.test_file_extension

    def get_test_filename(self, filename):
        """Map the filename to the name of the test for that file. Performs:
            - removes base path
            - swap the package name for 'tests'
            - replaces file extension of '.py' with '_test.py'

        >>> m = StandardMapper('/base')
        >>> m.get_test_filename('/base/package/more/file.py')
        'tests/more/file_test.py'
        >>> m.get_test_filename('/base/tests/more/file_test.py')
        'tests/more/file_test.py'
        """
        filename = self.strip_basepath(filename)
        if self.is_testfile(filename):
            return filename

        filename = self.swap_base_package(filename)
        return self.replace_extension(filename)


mapper_name_map = {
    'doctest':      DocTestMapper,
    'standard':     StandardMapper,
}

from_config = importutil.from_config_factory(
        'test_mapper', 'get_mapper', mapper_name_map)
