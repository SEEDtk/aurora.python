#!/usr/local/bin/python3
# encoding: utf-8
'''
 -- Find alias prefixes

 scans the CoreSEED directories and counts the different alias prefixes used

@author:     Bruce Parrello

@copyright:  2025 Bruce Parrello, Ph.D. All rights reserved.

@contact:    brucep.mobile@gmail.com

'''

import sys
import os
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2025-05-12'
__updated__ = '2025-05-12'

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
        parser.add_argument(dest="path", help="path to CoreSEED data directory", metavar="path")

        # Process arguments
        args = parser.parse_args()

        path = args.path
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
        # We will put the counts in here.
        counts = {}
        # Loop through the organisms.
        orgdir = path + "/Organisms"
        genome_dirs = [genome_dir.name for genome_dir in os.scandir(orgdir) if genome_dir.is_dir()]
        for genome_dir in genome_dirs:
            print(f"Processing genome {genome_dir}.", file=sys.stderr)
            featdir = orgdir + "/" + genome_dir + "/Features"
            type_dirs = [type_dir.name for type_dir in os.scandir(featdir) if type_dir.is_dir()]
            for type_dir in type_dirs:
                tbl_file = featdir + "/" + type_dir + "/tbl"
                with open(tbl_file, "r") as tbl_stream:
                    for line in tbl_stream:
                        fields = line.split("\t")
                        for i in range(2, len(fields)):
                            alias = fields[i]
                            m = re.match("([^:|]+)[:|]", alias)
                            if m:
                                alias_type = m.group(1)
                                if alias_type in counts.keys():
                                    counts[alias_type] += 1
                                else:
                                    counts[alias_type] = 1
        for alias_type in counts.keys():
            print(f"{alias_type}\t{counts[alias_type]}")
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