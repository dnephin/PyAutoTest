from pyautotest import importutil


class FileFilter(object):
    """Determine if the changed file should be tested or not."""

    @classmethod
    def should_test(cls, filename):
        """Return True if the file should be tested.

        >>> FileFilter.should_test('file.py')
        True
        >>> FileFilter.should_test('/home/user/code/file.py')
        True
        >>> FileFilter.should_test('rel/path/file.py')
        True
        >>> FileFilter.should_test('adir')
        False
        >>> FileFilter.should_test('/abs/dir')
        False
        >>> FileFilter.should_test('config,yaml')
        False
        """
        return filename.endswith('.py')


filter_map = {
    'python':       FileFilter
}


from_config = importutil.from_config_factory(
        'file_filter', 'get_filter', filter_map)