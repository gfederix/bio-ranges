#!/usr/bin/env python3
import setuptools
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bioRanges",
    version="0.0.1",
    author="Fyodor P. Goncharov",
    author_email="gfederix@gmail.com",
    description=("A quick and dirty implementation"
                 "of IRanges, GRanges, GRangesList and  rtracklayer"
                 "functionality from R for own needs."
                 "Help and bug reports are welcomed."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gfederix/bio-ranges",
    license="LGPL3+",
    install_requires=['numpy',
                      'pandas',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest', 'Cython',
    ],
    # extras_require={
    #     'tests':['pytest', 'cython', 'Cython',]
    # },
    ext_modules=cythonize(["**/*.pyx"], compiler_directives={
      'embedsignature': True,
      'boundscheck' : False,
      'wraparound' : False}),
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        "Programming Language :: Python :: 3",
        "OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
