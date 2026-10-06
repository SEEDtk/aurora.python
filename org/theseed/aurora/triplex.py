'''
This program will take a table of data and convert it into a set of triples.
The input table should be in a tab-delimited format, with the first column containing m-values,
the second containing s-values, the first row containing y-values, and the individual cells containing 
x-values that, when combined with the m-value and s-value in that row, produce
the y-value in the corresponding column header. The output will be a set of tuples (m, s, x, y) representing the relationships in the 
input table.

The command-line parameters are the name of the input table file and the name of the output file.

@author:     Bruce Parrello

@copyright:  2026 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com

'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2026-03-10'
__updated__ = '2026-03-10'

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
  Copyright 2026 Fellowship for Interpretation of Genomes. All rights reserved.

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
        parser.add_argument(dest="in_path", help="path to input file", metavar="in_path")
        parser.add_argument(dest="out_path", help="path to output file", metavar="out_path")

        # Process arguments
        args = parser.parse_args()

        in_path = args.in_path
        verbose = args.verbose
        out_path = args.out_path

        if verbose > 0:
            print("Verbose mode on")

        with open(in_path, 'r') as infile, open(out_path, 'w') as outfile:
            # Get the header line of the input file, containing the y-values.
            header = infile.readline()
            y_values = header.strip().split(sep="\t")
            # Write a header line to the output file.
            outfile.write("m\ts\tn\tx\ty\n")
            # Now loop through the data lines, writing triples.
            for line in infile:
                parts = line.strip().split(sep="\t")
                m = parts[0]
                s = parts[1]
                n = parts[2]
                for i in range(3, len(parts)):
                    x = parts[i]
                    y = y_values[i]
                    outfile.write(f"{m}\t{s}\t{n}\t{x}\t{y}\n")
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