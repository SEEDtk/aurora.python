#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.aurora_log_calc -- Compute token counts from aurora logs

org.theseed.aurora.aurora_log_calc is a simple script that reads the main aurora*.log files and summarizes the token counts

@author:     Bruce Parrello

@copyright:  2024 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@mgail.com
@deffield    updated: Updated
'''

import sys
import os
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-07-24'
__updated__ = '2024-07-24'

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

  Created by Bruce Parrello on %s.
  Copyright 2024 Fellowship for Interpretation of Genomes. All rights reserved.

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
        parser.add_argument(dest="path", help="path to folder with log files [default: %(default)s]", metavar="path")

        # Process arguments
        args = parser.parse_args()

        logDir = args.path
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        # Loop through the log files.
        i = 0
        done = False
        total = 0
        while (not done):
            i += 1
            file = os.path.join(logDir, "aurora" + str(i) + ".log")
            found = 0
            if not os.path.exists(file):
                done = True
            else:
                lCount = 0
                with open(file, "r") as logStream:
                    for line in logStream:
                        lCount += 1
                        m = re.search(r'(\d+) (?:total tokens generated in database|tokens produced so far)\.', line)
                        if m:
                            # Here we have a line with token data.
                            found = int(m.group(1))
                    print(f"{found} tokens recorded in {lCount} lines of {file}.")
                    total += found
        print(f"{total} tokens total for project.")
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
        profile_filename = 'org.theseed.aurora.aurora_log_calc_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
