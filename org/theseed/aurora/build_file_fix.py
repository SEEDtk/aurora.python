#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- Java Build File Fix

 is a simple program that converts a build.xml file to machine-portable format

The principle is simple.  We add a line for the environment variable accessor and then
we replace the value of the HOME variable everywhere with "${env.HOME}".

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
__date__ = '2025-02-03'
__updated__ = '2025-02-03'

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
        parser.add_argument(dest="path", help="paths to build file, which will be updated in place", metavar="path")

        # Process arguments
        args = parser.parse_args()

        path = args.path
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        print(f"Reading {path}.")
        with open(path, "r") as inStream:
            lines = inStream.readlines()
        n = len(lines)
        print(f"{n} data lines read")
        # Get the prefix we will find in the build file.
        oldPrefix = os.environ['HOME']
        oldPrefix = oldPrefix.replace("\\", "/")
        # Now loop through the input lines, writing them back. When we find the first "<property" line,
        # we add the environment property. When we find any "zipfileset" line, we replace the file string.
        line_count = 0
        added = 0
        replaced = 0
        with open(path, "w") as outStream:
            propAdded = False
            for line in lines:
                line_count += 1
                if not propAdded:
                    # We still have to add the property line. Check here if we are in the right section.
                    pos = line.find("<property")
                    if pos >= 0:
                        envLine = line[0:pos] + "<property environment=\"env\" />"
                        print(envLine, file=outStream)
                        propAdded = True
                        added += 1
                # Check for a zipfileset line.
                pos = line.find("<zipfileset")
                if pos >= 0:
                    line = line.replace(oldPrefix, "${env.HOME}", 1)
                    replaced += 1
                # Note that there is already a "\n" at the end, so we suppress the ending character.
                print(line, file=outStream, end='')
        print(f"All done. {line_count} lines read, {added} added, {replaced} replacements made.")
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
        profile_filename = '_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())