"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from outhouse import __version__

setup(
    name='outhouse',
    version=__version__,
    description='A no-nonsense dependency injection manager.',
    author='Sander Evers',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.7',
    entry_points={},
    url = 'https://github.com/sanderevers/outhouse',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)