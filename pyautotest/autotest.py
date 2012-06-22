"""Run a test file when either the source or test file is modified."""
import logging
import os
import time
import optparse
import yaml

from pyautotest import filefilter, mapper, runner

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


log = logging.getLogger(__name__)


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--path',
        help='The file path to watch for file modifications.')
    parser.add_option('-b', '--basepath',
        help='The base path for the repository, defaults to current dir.')
    parser.add_option('--no-recursive', default=None, action='store_true',
        help='Do not recurse into sub-directories.')
    parser.add_option('--test-mapper',
        help='The test mapper to use. Defaults to %s' %
             config_defaults['test_mapper_name'])
    parser.add_option('--test-runner',
        help='The test runner to use. Defaults to %s' %
             config_defaults['test_runner_name'])
    parser.add_option('-o', '--command', action='append',
        help='Command used to run the tests. Use multiple times if the command'
            ' requires arguments.')
    parser.add_option('-c', '--config', default='.pyautotest',
        help='Config file to use. Defaults to %default in the basepath dir.')
    parser.add_option('-v', '--verbose', action='store_true')
    opts, args = parser.parse_args()

    if opts.basepath:
        opts.config = os.path.join(opts.basepath, opts.config)
    return opts, args


class ConfigException(ValueError):
    pass


class Config(dict):
    """A configuration for auto test."""
    valid_keys = [
        'path',
        'basepath',
        'no_recursive',
        'test_mapper_name',
        'test_mapper_module',
        'test_runner_name',
        'test_runner_module',
        'command',
        'test_package_name',
        'file_filter_name'
    ]

    def update(self, d=None, **fields):
        """Override update to only set undefined fields.
        >>> c = Config(a=1); c.update(a=2); c['a']
        1
        >>> c = Config(); c.update(a=2); c['a']
        2
        >>> c = Config(); c.update({'a': 3}); c
        {'a': 3}
        >>> c = Config(a=None); c.update(a=4); c['a']
        4
        """
        fields = fields or d
        for key, value in fields.iteritems():
            if key in self and self[key]:
                continue
            self[key] = value

    def validate(self):
        """
        >>> Config({'what': 'something'}).validate()
        Traceback (most recent call last):
        ConfigException: Unexpected entry in config: what: something
        >>> Config({}).validate()

        >>> c = {'test_runner_name': 'a', 'test_runner_module': 'b'}
        >>> Config(c).validate()
        Traceback (most recent call last):
        ConfigException: You may only use one test runner. Got: a and b
        """
        for key, value in self.iteritems():
            if key not in Config.valid_keys:
                msg = "Unexpected entry in config: %s: %s"
                raise ConfigException(msg % (key, value))

        both = self.get('test_runner_name'), self.get('test_runner_module')
        if all(both):
            msg = "You may only use one test runner. Got: %s and %s"
            raise ConfigException(msg % both)

        both = self.get('test_mapper_name'), self.get('test_mapper_module')
        if all(both):
            msg = "You may only use one test mapper. Got: %s and %s"
            raise ConfigException(msg % both)


def setup_logging(opts):
    root_logger         = logging.getLogger()
    handler             = logging.StreamHandler()
    level               = logging.DEBUG if opts.verbose else logging.WARN
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


config_defaults = {
    'path':             '.',
    'no_recursive':     'False',
    'test_mapper_name': 'standard',
    'test_runner_name': 'file',
    'file_filter_name': 'python',
}


def get_config(opts):
    """Look for a config file, or setup a config from opts."""
    config = Config(
        path            =opts.path,
        basepath        =opts.basepath,
        no_recursive    =opts.no_recursive,
        test_mapper_name=opts.test_mapper,
        test_runner_name=opts.test_runner,
        command         =opts.command)

    if os.path.exists(opts.config):
        with open(opts.config, 'r') as fh:
            config.update(yaml.load(fh))

    config.validate()
    config.update(config_defaults)
    config['path']      = os.path.abspath(config['path'])
    basepath            = config.get('basepath') or config['path']
    config['basepath']  = os.path.abspath(basepath)

    return config


class FileModifiedMonitor(FileSystemEventHandler):
    """Monitor a filesystem for files that are modified."""

    def __init__(self, test_runner):
        super(FileModifiedMonitor, self).__init__()
        self.test_runner = test_runner

    def on_modified(self, event):
        if event.is_directory:
            return
        self.test_runner.run(event.src_path)


def main():
    opts, _         = parse_args()
    setup_logging(opts)

    config          = get_config(opts)
    file_filter     = filefilter.FileFilter
    mapper_class    = mapper.from_config(config)
    runner_class    = runner.from_config(config)
    test_mapper     = mapper_class(
                        config['basepath'], config.get('test_package_name'))
    test_runner     = runner_class(file_filter, test_mapper, config['command'])
    event_handler   = FileModifiedMonitor(test_runner)
    observer        = Observer()

    observer.schedule(
            event_handler, path=config['path'], recursive=not opts.no_recursive)
    observer.start()

    try:
        while True:
            time.sleep(999)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()