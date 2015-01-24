#!/usr/bin/env/python
"""
Yaposib is a python binding to OSI, the Open Solver Interface from
COIN-OR. It intends to give access to various solvers through
python. Yaposib was created in order to be integrated in pulp-or
(http://code.google.com/p/pulp-or).
"""
from __future__ import with_statement
from distutils.core import setup, Extension
import subprocess
import sys

def pkgconfig(*packages, **kw):
    """Finds a package using pkg-config"""
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    for token in subprocess.check_output(".\pkg-config --libs --cflags %s" %
                                         ' '.join(packages),
                                         shell=True).split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    return kw

def yaposib_extension():
    """Returns yaposib extension properly configured"""
    solvers = {
            "Cbc": "osi-cbc",
            "Clp": "osi-clp",
            "Cpx": "osi-cplex",
            "Dylp": "osi-dylp",
            "Fmp": "osi-fortmp",
            "Glpk": "osi-glpk",
            "Grb": "osi-gurobi",
            "Msk": "osi-mosek",
            "Osl": "osi-osl",
            "Spx": "osi-soplex",
            "Sym": "osi-sym",
            "Vol": "osi-vol",
            "Xpr": "osi-xpress"
            }
    kw = {
            # python2.7 wants PY_FORMAT_LONG_LONG to be defined
            "define_macros": [("PY_FORMAT_LONG_LONG", "I64"),
                              ("Sym", None),
                              ("Clp", None)],
            "include_dirs": ['C:\\Program Files (x86)\\boost_1_55_0\\boost_1_55_0',
                             'C:\\Program Files (x86)\\COIN-OR\\1.7.4\\win32-msvc9\\include\\coin'],
            "library_dirs": ['C:\\Python27\\libs',
                             'C:\\Program Files (x86)\\COIN-OR\\1.7.4\\win32-msvc9\\lib',
                             'C:\\Program Files (x86)\\COIN-OR\\1.7.4\\win32-msvc9\\lib\\intel'],
            # TODO: find a way to detect boost_python
            "libraries": [ "boost_python-vc90-mt-1_55",
                           "libboost_python-vc90-mt-1_55",
                           "libOsi",
                           "libCoinUtils",
                           "libOsiClp",
                           "libOsiSym",
                           "libSym",
                           "libCgl",
                           "libClp",
                           "libcoinglpk",
                           "mkl_intel_c",
                           "mkl_sequential",
                           "mkl_core"]
            }

    return Extension("yaposib._yaposib",
            sources = [
                "yaposib/CArrays.cpp",
                "yaposib/Col.cpp",
                "yaposib/Row.cpp",
                "yaposib/Obj.cpp",
                "yaposib/Problem.cpp",
                "yaposib/Binding.cpp"
                ],
            language = 'c++',
            **kw
            )

setup(name="yaposib",
      version="0.3.2",
      description= __doc__,
      long_description = open("README.md").read(),
      license = open("COPYING").read(),
      keywords = ["Optimization", "Linear Programming", "Operations Research"],
      author="Christophe-Marie Duquesne",
      author_email="chmd@chmd.fr",
      url="https://code.google.code/p/yaposib/",
      classifiers = ["Development Status :: 3 - Alpha",
                     "Environment :: Console",
                     "Intended Audience :: Science/Research",
                     "License :: OSI Approved",
                     "Natural Language :: English",
                     "Topic :: Scientific/Engineering :: Mathematics",
      ],
      packages = ['yaposib', 'yaposib.test'] ,
      ext_modules = [ yaposib_extension() ],
      package_data = { "" : [ "lib/*" ] },
      scripts = [ "scripts/yaposib-config", "scripts/yaposib-solve" ]
      )
