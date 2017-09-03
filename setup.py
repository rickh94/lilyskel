from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='lyskel',
    version='0.1',

    description='Generate a file/directory skeleton for lilypond projects',
    long_description=long_description,
    url='https://github.com/rickh94/lyskel',

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
    ],
    tests_require=['pytest', 'pytest-cov'],
    package=find_packages(),

    )
