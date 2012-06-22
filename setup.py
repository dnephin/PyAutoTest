from distutils.core import setup


setup(
    name            ='PyAutoTest',
    version         =0.1,
    description     ='Automatically run tests when files are modified.',
    author          ='Daniel Nephin',
    author_email    ='dnephin@gmail.com',
    url             ='https://github.com/dnephin/PyAutoTest',
    packages        =['pyautotest'],
    install_requires=['watchdog'],
    scripts         =['bin/pyautotest']
)