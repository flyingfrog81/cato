from distutils.core import setup
from distutils import dir_util
import os

data_dir = os.path.join(os.path.expanduser("~"), ".cato")
lic_dir = os.path.join(data_dir, "licenses")
dir_util.mkpath(data_dir, verbose=True)

setup(name = "cato",
        version = "1.0",
        author = "Marco Bartolini",
        author_email = "marco.bartolini@gmail.com",
        description = "Cato is a command line tool which facilitates source code licensing",
        data_files = [
            (lic_dir, [os.path.join("licenses", l) for l in os.listdir("licenses")]),
            (data_dir, ['cato.cfg']),
            ],
        py_modules = ['cato'],
        scripts = ['cato'],
        )
