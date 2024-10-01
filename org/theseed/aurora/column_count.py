#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.column_count -- Count values in a column

org.theseed.aurora.column_count is a Short utility that counts how many times each value occurs in an input file column.
The positional parameters should be the column index (1-based) and the input file name.

@author:     Bruce Parrello

@copyright:  2024 Fellowship for Interpretation of Genomes. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import math

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-10-01'
__updated__ = '2024-10-01'

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


def parseRecord(line):
    ''' Return the fields of the record. '''
    recordString = line.strip("\n")
    retVal = recordString.split("\t")
    return retVal

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
  Copyright 2024 organization_name. All rights reserved.

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
        parser.add_argument('-m', '--min', type=int, help="minimum output count [default: 0]", dest="minOut", default=0)
        parser.add_argument('-M', '--max', type=int, help="maximum output count (0 = no max) [default: 0]", dest="maxOut", default=0)
        parser.add_argument(dest="col", type=int, help="column index (1-based) to count", metavar="col")
        parser.add_argument(dest="path", help="path to file)", metavar="path")

        # Process arguments
        args = parser.parse_args()

        col = args.col - 1
        path = args.path
        verbose = args.verbose
        minOut = args.minOut
        maxOut = args.maxOut
        if maxOut == 0:
            maxOut = math.inf

        if verbose > 0:
            print("Verbose mode on")
        # The counts will go in here.
        counters = {}

        with open(path, "r") as inStream:
            # Skip the header line.
            line = inStream.readline()
            for line in inStream:
                fields = parseRecord(line)
                colText = fields[col]
                # Skip empty and blank values.
                if colText:
                    oldCount = counters.get(colText, 0)
                    counters[colText] = oldCount + 1
        print("genus\tcount")
        for genus in counters.keys():
            count = counters[genus]
            if count >= minOut and count <= maxOut:
                print(f"{genus}\t{count}")
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
        profile_filename = 'org.theseed.aurora.column_count_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
