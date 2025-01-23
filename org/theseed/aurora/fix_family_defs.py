#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.fix_family_defs -- fix protein family definitions

org.theseed.aurora.fix_family_defs is a small script that copies the local.family.defs file, adds headers, and fixes the family IDs

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
__date__ = '2024-12-18'
__updated__ = '2024-12-18'

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
        parser.add_argument(dest="genus", help="genus ID for the families in the definition file", metavar="genus")
        parser.add_argument(dest="in_file", help="source file for the family definitions", metavar="input_def_file")
        parser.add_argument(dest="out_file", help="output file", metavar="out_file")

        # Process arguments
        args = parser.parse_args()

        genus = args.genus
        verbose = args.verbose
        in_file = args.in_file
        out_file = args.out_file

        if verbose > 0:
            print("Verbose mode on")

        with open(in_file, 'r') as in_stream, open(out_file, 'w') as out_stream:
            out_stream.write("family_id\tname\n")
            lCount = 0
            for line in in_stream:
                fields = parseRecord(line)
                fam_idx = fields[0]
                fam_id = "PLF_" + genus + "_" + fam_idx.rjust(8, '0')
                out_stream.write(fam_id + "\t" + fields[1] + "\n")
                lCount += 1
        print(f"{lCount} lines converted")
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
        profile_filename = 'org.theseed.aurora.fix_family_defs_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
