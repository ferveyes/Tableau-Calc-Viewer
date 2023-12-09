from textwrap import dedent

from setuptools import find_packages
from setuptools import setup


setup(
    name="Tableau-Calc-Viewer",
    package_dir={"": "src"},
    py_modules=dedent("""
        calc_viewer
        field_utility
        main
        sg_utility
        tab_document
    """).split(),
    packages=find_packages(where="src")
)
