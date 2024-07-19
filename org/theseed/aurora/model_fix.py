#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.model_fix -- Fix FIG IDs in a model seed dump

org.theseed.aurora.model_fix is a command-line utility that fixes the problem with modelseed dumps replacing
the vertical bar in a FIG ID with " or ".

@author:     Bruce Parrello

@copyright:  2024 Fellowship for Interpretation of Genomes

@deffield    updated: 07/19/2024
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-07-19'
__updated__ = '2024-07-19'

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
    '''source is the source directory, target is the destination directory.'''

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
        parser.add_argument(dest="source", help="path to source folder [default: %(default)s]", metavar="source", default="model")
        parser.add_argument(dest="target", help="path to new target folder [default: %(default)s]", metavar="target", default="model_fixed")

        # Process arguments
        args = parser.parse_args()

        source = args.source
        target = args.target
        verbose = args.verbose

        if not os.path.exists(target):
            print(f"Creating directory {target}.")
            os.mkdir(target)

        if verbose > 0:
            print("Verbose mode on")

        inFiles = os.listdir(source)
        print(f"{len(inFiles)} files found in directory {source}.")
        print(f"New files will be created in {target}.")
        for inBase in inFiles:
            inFile = os.path.join(source, inBase)
            with open(inFile) as inStream:
                lines = inStream.readlines()
            outFile = os.path.join(target, inBase)
            print(f"Copying {len(lines)} lines from {inFile} to {outFile}.")
            with open(outFile, "w") as outStream:
                for line in lines:
                    line2 = line.replace("fig or ", "fig|")
                    outStream.write(line2)
        return 0
    except KeyboardInterrupt:
        print("Interrupted!")
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
        profile_filename = 'org.theseed.aurora.model_fix_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())