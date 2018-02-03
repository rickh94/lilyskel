from setuptools import setup, find_packages
from lilyskel import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='lilyskel',
    version=__version__,

    description='Generate a file/directory skeleton for lilypond projects',
    long_description=long_description,
    url='https://github.com/rickh94/lililyskel',

    author='Rick Henry',
    author_email='fredericmhenry@gmail.com',

    license='MIT',
    python_requires='>=3.6',
    setup_requires=['pytest-runner'],
    install_requires=[
        'num2words',
        'tinydb',
        'attrs',
        'titlecase',
        'bs4',
        'requests',
        'fuzzywuzzy[speedup]',
        'jinja2',
        'ruamel.yaml',
        'click',
        'prompt-toolkit',
    ],
    tests_require=['pytest', 'pytest-cov'],
    package=find_packages(),
)
