#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Extract protein distance results

 is a script that runs through the list files in a distance-correlation directory extracting a single protein's results

@author:     Bruce Parrello

@copyright:  2025 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com

'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2025-03-10'
__updated__ = '2025-03-10'

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
        parser.add_argument(dest="path", help="paths to folder with source files", metavar="path")
        parser.add_argument(dest="prot", help="name of protein whose results are desired", metavar="roleName")

        # Process arguments
        args = parser.parse_args()

        path = args.path
        verbose = args.verbose
        prot = args.prot

        if verbose > 0:
            print("Verbose mode on")

        # Set up the output file.
        outFile = os.path.join(path, prot + ".plist.tbl")
        with open(outFile, "w") as outStream:
            print("file\tgenome1\tgenome2\thammers\tDNA", file=outStream)
            for reportFile in os.listdir(path):
                if reportFile.endswith(".list.tbl"):
                    # Here we have a distance list report. Extract the file title.
                    fileTitle = reportFile.removesuffix(".list.tbl")
                    # Open this file.
                    print(f"Processing {reportFile}.")
                    outCount = 0
                    with open(os.path.join(path, reportFile), "r") as inReport:
                        # Skip the header.
                        line = inReport.readline()
                        # Read the data lines, extracting the ones for our protein.
                        for line in inReport:
                            if line.startswith(prot):
                                # NOTE the dataPart starts with a tab after the prefix is removed.
                                dataPart = line.removeprefix(prot)
                                outStream.write(fileTitle + dataPart)
                                outCount += 1
                        print(f"{outCount} lines output.")
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