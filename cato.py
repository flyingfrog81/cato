# coding=utf-8

#
#
#    Copyright (C) 2012  Marco Bartolini, marco.bartolini@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
This module implements the necessary routines used to embed license
informations into source code project files.
The package installation also installs a command line utility along with the
license files in textual format in a hidden directory inside the user home.

@author: Marco Bartolini
@contact: marco.bartolini@gmail.com
@version: 1.0
"""

import os
import getpass
import datetime
import re

class Cato(object):
    def __init__(self):
        """
        Default constructor sets default values for cato options.
        """
        self.home_path = os.path.expanduser("~")
        self.cato_dir = os.path.join(self.home_path, ".cato")
        self.license_dir = os.path.join(self.cato_dir, "licenses")
        self.end_phrase = "END OF TERMS AND CONDITIONS"

        self.comment_syntax = {"c" : "//",
                "cpp" : "//", 
                "cc" : "//", 
                "h" : "//",
                "hpp" : "//",
                "py" : "#",
                "java" : "//",
                "f" : "!",
                "rb" : "#",
                "default" : "*",
                }

        self.license_tags = {"<year>" : str(datetime.datetime.now().year),
                "<owner>" : getpass.getuser(),
                "<email>" : getpass.getuser() + "@example.com",
                }

        self.eol = "\n"
        self.loaded = False

    def parse_license(self, lic_name):
        """
        Parse a license file and split it into the full flagged license to 
        be included into a \"LICENSE\" file and an embedded version to be
        included at the beginning of each source file. It also substitute the 
        license tags in the license text.
        @type lic_name: string
        @param lic_name: license file name key
        @return: (full_licensem, embedded_license) 
        """
        licenses = {}
        for license_file in os.listdir(self.license_dir):
            licenses[license_file[:license_file.rfind(".")]] = \
                os.path.abspath(os.path.join(self.license_dir, license_file))
        try:
            with open(licenses[lic_name], "rt") as f:
                text = f.read()
        except KeyError:
            raise KeyError("License " + lic_name + " not found in " +
                    self.license_dir)
        for tag, substitution in self.license_tags.iteritems():
            pattern = re.compile(tag)
            text = re.subn(pattern, substitution, text)[0]
        license_parts = text.split(self.end_phrase) 
        extended_license = license_parts[0]
        if len(license_parts) == 1:
            embedded_license = license_parts[0].split(self.eol)
        else:
            embedded_license = license_parts[1].split(self.eol)
        return (extended_license, embedded_license)

    def patch_file(self, filename, embedded_license):
        """
        Embed the license in the given source code file. The license is inserted
        where the first empty line is found. If no empty line is present no license
        is embedded. 
        @param filename: file path
        @param embedded_license: the embedded license as obtained by
        L{parse_license} function
        @return: True if a license has been embedded
        """
        extension = filename.split(".")[-1]
        comment = self.comment_syntax.get(extension, self.comment_syntax["default"])
        embedded = False
        with open(filename, "rt") as input:
            with open(filename + ".cato", "wt") as output:
                for input_line in input:
                    output.write(input_line)
                    if not embedded and input_line.strip() == "":
                        for embed_line in embedded_license:
                            output.write(comment + embed_line + self.eol)
                        embedded = True
        os.rename(filename + ".cato", filename)
        return embedded

    def patch_dir(self, dirname, extended_license):
        """
        Insert a license file into a directory naming it \"LICENSE\".
        @param dirname: the target directory path
        @param extended_license: the license text as obtained by L{parse_license}
        function
        """
        with open(os.path.join(dirname, "LICENSE"), "wt") as license_file:
            license_file.write(extended_license)

def command_line_util(args):
    """
    Function that parses command line options and invokes cato methods on
    selected files. Use --help for online help.
    """
    from optparse import OptionParser #for compatibility with python2.5
    from ConfigParser import SafeConfigParser
    import os
    import fnmatch

    cato_licenser = Cato()

    # Parsing configuration file options
    scp = SafeConfigParser()
    scp.read(os.path.join(cato_licenser.cato_dir, "cato.cfg"))
    if 'Cato' in scp.sections():
        if 'owner' in scp.options('Cato'):
            cato_licenser.license_tags['<owner>'] = scp.get('Cato', 'owner')
        if 'email' in scp.options('Cato'):
            cato_licenser.license_tags['<email>'] = scp.get('Cato', 'email')
        if 'end_phrase' in scp.options('Cato'):
            cato_licenser.end_phrase = scp.get('Cato', 'end_phrase')
    if 'Comments' in scp.sections():
        for c in scp.options('Comments'):
            cato_licenser.comment_syntax[c] = scp.get('Comments', c)

    # Parsing command line options
    op = OptionParser()
    op.add_option("--list", action="store_true", default=False,
            dest="lic_list", help="Lists available licenses and quit")
    op.add_option("-l", "--license", dest="license", help="The license name, use --list to list all licenses available")
    op.add_option("-o", "--owner", dest="owner", help="the copyright owner")
    op.add_option("-e", "--email", dest="email", help="email contact of the copyright owner")
    op.add_option("-y", "--year", dest="year", help="the copyright year, defaults to current year")
    op.add_option("-d", "--directory", dest="directory", help="a target directory where to find sources and add a LICENSE file")
    op.add_option("-r", action="store_true", default="False", dest="recursive",
            help="only with -d. If set recursively parses directory tree")
    op.add_option("-c", "--comment", dest="comment", help="overrides comment syntax")
    op.set_usage("cato -l gpl-3.0 -o \"John Doe\" -e john@doe.com -y 2012 *.py")
    op.set_description('''
cato is free software for applying licenses to your source code
files. You can customize cato changing the cato.cfg file that you
find in ~/.cato/ and adding license textual files in
~/cato/licenses/.\n
License files can contain <owner> and <email>
textual tags which will be replaced with cato informations.\n
Embedded license versions will be applied on the first empty line of
each source file scanned, if no empty line is found, no license is
applied.\n
In its normal behaviour cato apply the license to the files given as
arguments on the command line, while using -d option it scans the
given directory for file extensions specified as command line
arguments. If -r is provided in conjunction with -d, all the
directory tree is scanned starting from the supplied dir.
            ''')
    options, args = op.parse_args(args)

    # scan license directory and populate licenses dictionary
    licenses = []
    for lic_file in os.listdir(cato_licenser.license_dir):
        licenses.append(lic_file[:lic_file.rfind('.')])

    # list available licenses
    if options.lic_list:
        for l in licenses:
            print l
        return

    # overrides config file options
    if options.owner:
        cato_licenser.license_tags['<owner>'] = options.owner
    if options.year:
        cato_licenser.license_tags['<year>'] = options.year
    if options.email:
        cato_licenser.license_tags['<email>'] = options.email
    if options.comment:
        cato_licenser.comment_syntax = {'default': options.comment} 

    #extracts license infomrations
    if not options.license:
        license = licenses[0] #default license
    else:
        license = options.license
    (extended_lic, embedded_lic) = cato_licenser.parse_license(license)

    # Apply the license to given sources
    if options.directory:
        dir = options.directory
        cato_licenser.patch_dir(dir, extended_lic)
        if options.recursive:
            for root, dirs, files in os.walk(dir):
                for f in files:
                    match = False
                    for a in args:
                        if fnmatch.fnmatch(f, "*." + a):
                            match = True
                    if match:
                        print "Applying license to file: " + f
                        cato_licenser.patch_file(os.path.join(root, f), embedded_lic)
        else:
            root = os.path.abspath(dir)
            for f in os.listdir(root):
                if os.path.isfile(os.path.join(root, f)):
                    match = False
                    for a in args:
                        if fnmatch.fnmatch(f, "*." + a):
                            match = True
                    if match:
                        print "Applying license to file: " + f
                        cato_licenser.patch_file(os.path.join(root, f), embedded_lic)
    else:
        for f in args:
            print "Applying license to file: " + f
            cato_licenser.patch_file(f, embedded_lic)
