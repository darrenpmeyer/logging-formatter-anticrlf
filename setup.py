from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='logging-formatter-anticrlf',
    version='1.2',
    packages=['anticrlf'],
    url='https://github.com/darrenpmeyer/logging-formatter-anticrlf',
    license='BSD 2-clause',
    author='Darren P Meyer',
    author_email='darren@darrenpmeyer.com',
    description='Python logging Formatter for CRLF Injection (CWE-93 / CWE-117) prevention',
    long_description=long_description,
    long_description_content_type='text/x-rst'
)
