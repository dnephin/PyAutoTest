try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = 0, 6

setup(
    name            ='yapyautotest',
    version         ='.'.join(str(i) for i in version),
    description     ='Automatically run tests when files are modified.',
    author          ='Daniel Nephin',
    author_email    ='dnephin@gmail.com',
    url             ='https://github.com/dnephin/PyAutoTest',
    packages        =['yapyautotest'],
    install_requires=['watchdog >= 0.8.3 '],
    entry_points={
        'console_scripts': [
            'pyautotest = yapyautotest.autotest:main',
        ],
    },
)
