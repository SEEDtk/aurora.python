#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.core_genome_check -- check a genome list against a GTO directory

org.theseed.aurora.core_genome_check is a command that compares a headerless list of genome IDs to a GTO directory. We use it to insure
the genome list's entries are still valid

@author:     Bruce Parrello

@copyright:  2025 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com
@deffield    updated: Updated
'''

import sys
import os
import glob
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2025-01-25'
__updated__ = '2025-01-25'

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
        parser.add_argument(dest="listFile", help="path to genome list file", metavar="listFile")
        parser.add_argument(dest="gtoDir", help="path to GTO directory", metavar="gtoDir")

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        listFile = args.listFile
        gtoDir = args.gtoDir

        if verbose > 0:
            print("Verbose mode on")

        # Get the genome IDs from the GTO directory.
        genomeSet = set()
        for f in glob.glob(gtoDir + "/*.gto"):
            m = re.search("(\\d+\\.\\d+)\\.gto", f)
            if m != None:
                genomeId = m.group(1)
                genomeSet.add(genomeId)
        print(str(len(genomeSet)) + " genome IDs found in " + gtoDir + ".")
        # Now run through the list file checking the genome IDs.
        with open(listFile, "r") as inStream:
            for line in inStream:
                genomeId = line.partition("\t")[0]
                if not (genomeId in genomeSet):
                    print(f"{genomeId} was not found.")
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
        profile_filename = 'org.theseed.aurora.core_genome_check_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
