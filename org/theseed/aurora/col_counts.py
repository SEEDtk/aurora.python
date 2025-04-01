#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- Count different values in columns

 is a command to read a tab-delimited file and count the unique values in each column

@author:     Bruce Parrello

@copyright:  2025 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com
@deffield    updated: 03/18/2025
'''

import sys
import os
import pandas as pd

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2025-03-18'
__updated__ = '2025-03-18'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def count_unique_values(file_path):
    try:
        # Read the tab-delimited file
        # sep='\t' specifies tab as the delimiter
        df = pd.read_csv(file_path, sep='\t')

        # Get column names
        columns = df.columns

        # Dictionary to store results
        unique_counts = {}

        # Count unique values for each column
        for column in columns:
            # nunique() counts unique values, dropna=False includes NaN as a value
            count = df[column].nunique(dropna=False)
            unique_counts[column] = count

            # Get the unique values themselves (optional display)
            unique_values = df[column].unique()

            print(f"\nColumn: {column}")
            print(f"Number of unique values: {count}")
            print(f"Unique values: {unique_values}")

        return unique_counts

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

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
        parser.add_argument(dest="file_path", help="path to source file", metavar="path")

        # Process arguments
        args = parser.parse_args()

        file_path = args.file_path
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        results = count_unique_values(file_path)

        if results:
            print("\nSummary of unique value counts:")
            for column, count in results.items():
                print(f"{column}: {count} unique values")
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