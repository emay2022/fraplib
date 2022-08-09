# fraplib

[![License](https://img.shields.io/pypi/l/fraplib.svg?color=green)](https://github.com/emay2022/fraplib/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/fraplib.svg?color=green)](https://pypi.org/project/fraplib)
[![Python Version](https://img.shields.io/pypi/pyversions/fraplib.svg?color=green)](https://python.org)
[![CI](https://github.com/emay2022/fraplib/actions/workflows/ci/badge.svg)](https://github.com/emay2022/fraplib/actions)
[![codecov](https://codecov.io/gh/emay2022/fraplib/branch/master/graph/badge.svg)](https://codecov.io/gh/emay2022/fraplib)

Functions for calculating and displaying frap experiment data. Supports processing .czi experiment files from Zeiss microscopes (either single files or for all the files in a directory). Extracts information from the metadata such as the coordinates and geometry of the bleached region and pixel scaling in physical units.

Important note: this library is under development and is frequently not backward compatible.

Dependencies
------------
czifile
numpy
symfit
matplotlib
