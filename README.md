PyAutoTest
==========


PyAutoTest is a tool for python developers. It automatically runs the appropriate unit tests 
when a file is modified.  If the modified file is a test file, then it will be run.  PyAutoTest supports any unit test framework and test naming schema (with extension).  

PyAutoTest can be configured by specifying command line arguments, or by creating
a .pyautotest file in your project root.  Alternative files can be specified
using the `-c` option.

See `.pyautotest` in this repo for an example configuration.


Install
-------

    pip install yapyautotest


Configuration
-------------

The PyAutoTest configuration file is a yaml file which supports the following
configuration options.

* `path` - the directory to watch for file modifications

* `basepath` - the base path of your code repository (defaults to `path`)

* `no_recursive` - disables recursive monitoring of directories

* `test_mapper_name` - use a default mapper for mapping code filenames to their test filenames. Available options are:
    * `standard` - replaces the top level package with the name `tests`. See `test_package_name` if your test package has a different name.

                File:
                    package/runner/stuff.py
                Would be mapped to:
                    tests/runner/stuff_test.py

    * `doctest` - expects the tests to exist in the modified file.

* `test_package_name` - override the default package name with this name when mapping files to their tests. Example:

            test_package_name:  "test/units"

* `test_mapper_module` - if the standard test mappers do not support your naming schema, you can create your own.  To have PyAutoTest use this module, it should include a `get_mapper()` function, and set this option to the module name (including package names).  The module must also be in your `$PYTHONPATH`. See `pyautotest.mapper` for the expected interface. Example:

            test_mapper_module: "myproject.testing.custompyautotestmapper"

* `test_runner_name` - the name of the test runner used to run the tests. If you'd like to customize the command used to run tests, see the `command` configuration options.  Avaiable options are:
    * `file` - run the file using `python`
    * `unittest` - run the test using `python -m unittest`
    * `doctest` - run the test using `python -m doctest`
    * `testify` - run the test using `testify`
    * `unittest2` - run the test using `unit2`
    * `pytest` - run the test using `py.test`

* `command` - the command used by the `test_runner` to execute the test.  If you'd like to specify command line options, (such as -v) or you want to specify a path to an alternative executable, you can use this configuration options. Note that this should be a list.

            command: ["/usr/bin/mytestit", '-v']

* `test_runner_module` - if the standard test runners do not work for you, you can create a module for running tests. This module must have a `get_runner()` function, and must be on your python path. See `test_mapper_module` for more details and `pyautotest.runner` for the expected interface.

* `file_filter_module` - by default PyAutoTest will only try to run tests for files which end in `.py`.  If you'd like to change this behavior, you can create a module with a `get_filter()`, which returns a FileFilter object.  See `test_mapper_module` for more details, and see `pyautotest.filefiler` for the expected interface.


