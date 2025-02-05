#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- Check Virus List

 is a command to compare genome IDs in a tab-delimited file to subdirectory names to list which ones still
 need to be downloaded


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
__date__ = '2025-02-05'
__updated__ = '2025-02-05'

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
        parser.add_argument(dest="in_file", help="tab-delimited file of genome IDs", metavar="in_file")
        parser.add_argument(dest="out_file", help="output file for missing genomes", metavar="out_file")
        parser.add_argument(dest="paths", help="paths to folder(s) with subdirectories [default: %(default)s]", metavar="path", nargs='+')


        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        in_file = args.in_file
        out_file = args.out_file

        if verbose > 0:
            print("Verbose mode on")

        # First we read all the genome IDs from the incoming folders into a set.
        current_dirs = {}
        for inpath in paths:
            for subdir in os.listdir(inpath):
                full_path = os.path.join(inpath, subdir)
                if (os.path.isdir(full_path)):
                    current_dirs[subdir] = inpath
        n = len(current_dirs)
        print(f"{n} subdirectories found in all folders.")
        with open(in_file, "r") as inStream, open(out_file, "w") as outStream:
            # Copy the header line
            line = inStream.readline()
            line = line.rstrip()
            print(line + "\tsource", file=outStream)
            missCount = 0
            foundCount = 0
            for line in inStream:
                line = line.rstrip()
                genomeId = line.partition("\t")[0]
                if genomeId in current_dirs:
                    foundCount += 1
                    print(line + "\t" + current_dirs[genomeId], file=outStream)
                else:
                    missCount += 1
                    print(line + "\t", file=outStream)
        print(f"{foundCount} genomes found, {missCount} missing.")
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