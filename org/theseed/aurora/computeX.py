'''
This program will take a table of data and apply a formula to attempt to comput the y-values
based on the various input variables.

The command-line parameters are the name of the input table file and the name of the output file.
The output file will contain the input values, the computed y-values, the actual y-value, and the error
between the two.

@author:     Bruce Parrello

@copyright:  2026 Fellowship for Interpretation of Genomes. All rights reserved.

@contact:    brucep.mobile@gmail.com

'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import math

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

def compute_y(m, s, n, x):
    nf = float(n)
    xf = float(x) / nf
    sf = float(s)
    mf = float(m)
    return y_hat(mf, sf, nf, xf)
    
def y_hat(m, s, n, x):
    """Approximate y from m, s, n, and x.

    Logistic quadratic in the logs. Inputs must be positive.
    Returns a value in (0, 1).
    """
    lm = math.log(m)
    ls = math.log(s)
    lx = math.log(x)
    ln = math.log(n)
    z = (
        3.205097903369
        + 0.990568374872 * lm
        + 0.769299408350 * ls
        + 1.130071993073 * lx
        + 0.341357726413 * ln
        + 0.394510691461 * lm * lm
        + 0.230855956966 * ls * ls
        + 0.011678610565 * lx * lx
        - 0.431887341070 * lm * ls
        - 0.506886406325 * lm * lx
        - 0.062683263122 * ls * lx
        - 0.056870021462 * ln * lx
    )
    return 1.0 / (1.0 + math.exp(-z))

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
            outfile.write("name\tm\ts\tn\tx\ty\ty0\terror\n")
            # Now loop through the data lines, writing results including computed y-values and errors.
            for line in infile:
                parts = line.strip().split(sep="\t")
                name = parts[0]
                m = parts[1]
                s = parts[2]
                n = parts[3]
                for i in range(4, len(parts)):
                    x = parts[i]
                    y = y_values[i]
                    y0 = compute_y(m, s, n, x)  # Assuming compute_y is the function to compute y-values
                    error = float(y) - float(y0)
                    outfile.write(f"{name}\t{m}\t{s}\t{n}\t{x}\t{y}\t{y0}\t{error}\n")
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