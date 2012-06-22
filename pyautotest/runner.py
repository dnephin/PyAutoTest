import logging
import os.path
import subprocess

log = logging.getLogger(__name__)

# TODO: support imports
def from_config(config):
    """
    >>> c = {'test_runner_name': 'file'}
    >>> from_config(c) # doctest: +ELLIPSIS
    <class 'runner.FileTestRunner'>

    >>> from_config({})
    Traceback (most recent call last):
        ...
    ValueError: Unknown Test Runner: None
    """
    name = config.get('test_runner_name')
    if name not in test_runner_map:
        raise ValueError("Unknown Test Runner: %s" % name)
    return test_runner_map[name]


class FileTestRunner(object):
    """A test runner which runs a test file using `command`.
    """

    default_command = ['python']

    def __init__(self, file_filter, test_mapper, command=None):
        self.file_filter        = file_filter
        self.test_mapper        = test_mapper
        self.command            = command or ['python']

    def run(self, filename):
        if not self.file_filter.should_test(filename):
            log.info("Ignoring not testable file: %s", filename)
            return

        test_filename = self.test_mapper.get_test_filename(filename)
        if not os.path.isfile(test_filename):
            log.warn("Missing test for %s. Expected at %s",
                filename, test_filename)
            return

        test_name = self.get_test_name(test_filename)
        self.run_test(test_name)

    def run_test(self, test_name):
        subprocess.call(self.command + [test_name])

    def get_test_name(self, filename):
        return filename


class ModuleRunner(FileTestRunner):

    default_command = ['testify', '-v', '--summary']

    def get_test_name(self, filename):
        return '.'.join(filename.split(os.path.sep))[:-len('.py')]


test_runner_map = {
    'file':         FileTestRunner,
    'module':       ModuleRunner,
}
