#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.find_aliases -- find role aliases

org.theseed.aurora.find_aliases is a command that parses an old roles.in.subsystems file to create the role alias list

@author:     Bruce Parrello

@copyright:  2025 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2025-01-24'
__updated__ = '2025-01-24'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2025 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="inDir", help="path to folder with roles.in.subsystems file", metavar="inDir")

        # Process arguments
        args = parser.parse_args()

        inDir = args.inDir
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        # Get the input and output file names.
        inFile = inDir + "/roles.in.subsystems"
        outFile = inDir + "/roles.aliases"

        # This dictionary will map each role ID to a list of role names. An alias is a role ID with
        # multiple role names attached. The first found is generally the primary.
        role_map = {}

        with open(inFile, "r") as inStream:
            for line in inStream:
                # role ID is first field, role name is third
                fields = line.rstrip().split("\t")
                roleId = fields[0]
                roleName = fields[2]
                nameList = role_map.get(roleId)
                if nameList == None:
                    nameList = []
                    role_map[roleId] = nameList
                # Now we have the name list for the role ID. If the role ID is new, the
                # list will be a new empty list.
                nameList.append(roleName)

        # Now we run through the dictionary, writing role IDs with multiple names.
        with open(outFile, "w") as outStream:
            for roleId, nameList in role_map.items():
                if len(nameList) > 1:
                    for name in nameList:
                        outStream.write(f"{roleId}\tx\t{name}\n")

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'org.theseed.aurora.find_aliases_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
