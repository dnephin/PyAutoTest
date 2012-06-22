try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = 0, 2

setup(
    name            ='PyAutoTest',
    version         ='.'.join(str(i) for i in version),
    description     ='Automatically run tests when files are modified.',
    author          ='Daniel Nephin',
    author_email    ='dnephin@gmail.com',
    url             ='https://github.com/dnephin/PyAutoTest',
    packages        =['pyautotest'],
    install_requires=['watchdog'],
    scripts         =['bin/pyautotest']
)