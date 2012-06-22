PyAutoTest
==========


PyAutoTest is a tool for python developers. It automatically runs unit tests 
when a file is modified.  It supports any unit test framework and test naming 
schema (with extension).

PyAutoTest can be configured by specifying command line arguments, or by creating
a .pyautotest file in your project root.  Alternative files can be specified
using the `-c` option.

See `.pyautotest` in this repo for an example configuration.

Requires `watchdog` (http://pypi.python.org/pypi/watchdog).
