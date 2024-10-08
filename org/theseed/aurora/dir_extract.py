#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.dir_extract -- extract sample lines from an SRA map file

org.theseed.aurora.dir_extract is a command that looks at samples in a directory and extracts the corresponding lines from an SRA map file


@author:     Bruce Parrello

@copyright:  2024 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-07-27'
__updated__ = '2024-07-27'

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
        parser.add_argument(dest="inDir", help="folder containing sample directories", metavar="inDir")
        parser.add_argument(dest="sraMap", help="file containing sra Map", metavar="sraMap.tbl")
        parser.add_argument(dest="outFile", help="output file for extracted data", metavar="outFile.tbl")

        # Process arguments
        args = parser.parse_args()

        inDir = args.inDir
        verbose = args.verbose
        sraMapFile = args.sraMap
        outFile = args.outFile

        if verbose > 0:
            print("Verbose mode on")

        # Get the list of samples to keep.
        sampleSet = set()
        for sampleDir in os.listdir(inDir):
            sampleSet.add(sampleDir)
        print(f"{len(sampleSet)} samples found in {inDir}.")

        # Open the input and output files.  The input header is transferred
        # unchanged.
        outCount = 0
        inCount = 0
        with open(outFile, 'w') as outStream, open(sraMapFile, 'r') as inStream:
            line = inStream.readline()
            outStream.write(line)
            # Now loop through the data lines.
            for line in inStream:
                inCount += 1
                lineFields = line.split("\t")
                if lineFields[2] in sampleSet:
                    # Here the line is for a sample we care about.
                    outStream.write(line)
                    outCount += 1
        print(f"{inCount} lines read.  {outCount} lines written.")
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
        profile_filename = 'org.theseed.aurora.dir_extract_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
