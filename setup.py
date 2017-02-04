from setuptools import setup

setup(
    name='logging-formatter-anticrlf',
    version='1.0',
    packages=['anticrlf', 'anticrlf.tests'],
    url='https://github.com/darrenpmeyer/logging-formatter-anticrlf',
    license='BSD 2-clause',
    author='Darren P Meyer',
    author_email='darren@darrenpmeyer.com',
    description='Python logging Formatter for CRLF Injection (CWE-93) prevention',
)
