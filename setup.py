""" Runner of the setup method with configuration given in setup.cfg """
import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import find_packages
from setuptools import setup


if __name__ == '__main__':
    # The use_scm_version option indicates that we want to use the
    # setuptools_scm package to set the version automatically based on git
    # tags, which will produce version strings such as 0.13 for a stable
    # release, or 0.16.0.dev113+g3d1a8747 for a developer version.
    
    setup(
        name="pyfavor",
        version='1.0.0',
        description='Python package for creating files for analysis of bursts with efavor',
        author='Tomasz Janus',
        author_email='tomasz.k.janus@gmail.com',
        #url='https://github.com/tomjanus/reemission',
        packages=find_packages("."),
        py_modules=[splitext(basename(path))[0] for path in glob('pyfavor/*.py')],
        include_package_data=True,
        #packages=["pyfavor"],
        #package_dir={"pyfavor":"pyfavor"},
        #exclude_package_data={
        #    'reemission.examples': [
        #        ".shx", ".shp", ".prj", ".dbf", "cpg", "pdf", ".qmd", ".geojson", 
        #        ".html", ".csv", ".tex", ".xlsx"
        #    ]
        #},
        zip_safe=False
    )
# use_scm_version=True,
# setup_requires=['setuptools_scm']
