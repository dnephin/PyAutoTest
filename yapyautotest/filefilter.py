from yapyautotest import importutil


class FileFilter(object):
    """Determine if the changed file should be tested or not."""

    def __init__(self, ext='.py'):
        self.ext = ext

    def should_test(self, filename):
        """Return True if the file should be tested.

        >>> FileFilter().should_test('file.py')
        True
        >>> FileFilter().should_test('/home/user/code/file.py')
        True
        >>> FileFilter().should_test('rel/path/file.py')
        True
        >>> FileFilter().should_test('adir')
        False
        >>> FileFilter().should_test('/abs/dir')
        False
        >>> FileFilter().should_test('config,yaml')
        False
        >>> FileFilter('.rb').should_test('what.rb')
        True
        """
        return filename.endswith(self.ext)

    def __repr__(self):
        return "FileFilter(%r)" % (self.ext)


filter_map = {
    'python':       FileFilter(),
    'ruby':         FileFilter('rb')
}


from_config = importutil.from_config_factory(
        'file_filter', 'get_filter', filter_map)
