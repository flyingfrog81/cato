from distutils.core import setup
from distutils import dir_util
import os

data_dir = os.path.join(os.path.expanduser("~"), ".cato")
lic_dir = os.path.join(data_dir, "licenses")
dir_util.mkpath(data_dir, verbose=True)

setup(name = "cato",
        version = "1.0.1",
        author = "Marco Bartolini",
        author_email = "marco.bartolini@gmail.com",
        description = "Cato is a command line tool which facilitates source code licensing",
        license="gpl",
        url = "https://github.com/flyingfrog81/cato",
        download_url = "https://github.com/flyingfrog81/cato/zipball/master",
        data_files = [
            (lic_dir, [os.path.join("licenses", l) for l in os.listdir("licenses")]),
            (data_dir, ['cato.cfg']),
            ],
        py_modules = ['cato'],
        scripts = ['cato'],
        classifiers = [
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Natural Language :: English",
            "Programming Language :: Python",
            "Topic :: Software Development :: Documentation",
            "Topic :: Utilities",
            ],
        long_description = """
CATO
====

This module implements the necessary routines used to embed license
informations into source code project files.
The package installation also installs a command line utility along with the
license files in textual format in a hidden directory inside the user home.


LICENSE
=======

Cato license terms can be found in the LICENSE file distributed with the 
package.

INSTALLATION
============

after downloading the package::

    $ cd cato
    $ python setup.py install

or via pypi automatic installation::

    $ pip install cato

DOCUMENTAION
============

Developer documentation is distributed in html format along with the package,
and can be obtained running epydoc on the source code files::

    Usage: cato -l gpl-3.0 -o "John Doe" -e john@doe.com -y 2012 filename.py

Cato is free software for applying licenses to your source code files. You
can customize cato changing the cato.cfg file that you find in ~/.cato/ and
adding license textual files in ~/cato/licenses/.  License files can contain
<owner> and <email> textual tags which will be replaced with cato
informations.  Embedded license versions will be applied on the first empty
line of each source file scanned, if no empty line is found, no license is
applied.  In its normal behaviour cato apply the license to the files given as
arguments on the command line, while using -d option it scans the given
directory for file extensions specified as command line arguments. If -r is
provided in conjunction with -d, all the directory tree is scanned starting
from the supplied dir.

Options::
  -h, --help            show this help message and exit
  --list                Lists available licenses and quit
  -l LICENSE, --license=LICENSE
                        The license name, use --list to list all licenses
                        available
  -o OWNER, --owner=OWNER
                        the copyright owner
  -e EMAIL, --email=EMAIL
                        email contact of the copyright owner
  -y YEAR, --year=YEAR  the copyright year, defaults to current year
  -d DIRECTORY, --directory=DIRECTORY
                        a target directory where to find sources and add a
                        LICENSE file
  -r                    only with -d. If set recursively parses directory tree
  -c COMMENT, --comment=COMMENT
                        overrides comment syntax""",
        )
